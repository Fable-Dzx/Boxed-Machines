package com.boxedmachines.blockentity;

import com.boxedmachines.block.BoxedMachineBlock;
import com.boxedmachines.screen.BoxedMachineScreenHandler;
import com.boxedmachines.util.MachineType;
import net.minecraft.block.BlockState;
import net.minecraft.block.entity.BlockEntity;
import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.block.entity.HopperBlockEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.Inventories;
import net.minecraft.inventory.SimpleInventory;
import net.minecraft.inventory.SidedInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.registry.RegistryWrapper;
import net.minecraft.screen.NamedScreenHandlerFactory;
import net.minecraft.screen.ScreenHandler;
import net.minecraft.text.Text;
import net.minecraft.util.collection.DefaultedList;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;
import org.jetbrains.annotations.Nullable;

/**
 * 盒装机器的方块实体。
 * - 内部 27 槽位用于存储产出物
 * - 每 ticksPerCycle 刻自动产出一轮
 * - 自动向相邻容器（箱子、漏斗等）推送物品
 * - 右键打开 GUI 手动取物
 */
public class BoxedMachineBlockEntity extends BlockEntity implements NamedScreenHandlerFactory, SidedInventory {

    private static final int INVENTORY_SIZE = 27; // 3行 x 9列
    private static final int PUSH_INTERVAL = 20; // 每 20 刻尝试推送一次
    private static final int[] ACCESSIBLE_SLOTS = new int[INVENTORY_SIZE];

    static {
        for (int i = 0; i < INVENTORY_SIZE; i++) ACCESSIBLE_SLOTS[i] = i;
    }

    private final MachineType machineType;
    private final DefaultedList<ItemStack> inventory;
    private int ticksSinceLastCycle = 0;
    private int ticksSinceLastPush = 0;

    public BoxedMachineBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state, MachineType machineType) {
        super(type, pos, state);
        this.machineType = machineType;
        this.inventory = DefaultedList.ofSize(INVENTORY_SIZE, ItemStack.EMPTY);
    }

    // ===== Tick 逻辑 =====

    public void tick(net.minecraft.world.World world, BlockPos pos, BlockState state) {
        if (world.isClient) return;

        ticksSinceLastCycle++;
        ticksSinceLastPush++;

        // 产出一轮
        if (ticksSinceLastCycle >= machineType.getTicksPerCycle()) {
            ticksSinceLastCycle = 0;
            produceItems();
        }

        // 自动推送
        if (ticksSinceLastPush >= PUSH_INTERVAL) {
            ticksSinceLastPush = 0;
            pushItemsToAdjacent(world, pos, state);
        }
    }

    private void produceItems() {
        for (MachineType.Output output : machineType.getOutputs()) {
            ItemStack toAdd = new net.minecraft.item.ItemStack(output.item(), output.count());
            // 尝试堆叠到现有槽位
            boolean added = false;
            for (int i = 0; i < INVENTORY_SIZE; i++) {
                ItemStack slot = inventory.get(i);
                if (slot.isEmpty()) {
                    inventory.set(i, toAdd.copy());
                    added = true;
                    break;
                } else if (ItemStack.areItemsEqual(slot, toAdd)
                        && slot.getCount() + toAdd.getCount() <= slot.getMaxCount()) {
                    slot.increment(toAdd.getCount());
                    added = true;
                    break;
                }
            }
            // 如果堆叠失败，找空槽位
            if (!added) {
                for (int i = 0; i < INVENTORY_SIZE; i++) {
                    if (inventory.get(i).isEmpty()) {
                        inventory.set(i, toAdd.copy());
                        break;
                    }
                }
            }
        }
        markDirty();
    }

    private void pushItemsToAdjacent(net.minecraft.world.World world, BlockPos pos, BlockState state) {
        Direction facing = state.get(BoxedMachineBlock.FACING);
        // 向正面和下方推送
        Direction[] directions = {facing, Direction.DOWN, Direction.UP, Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST};

        for (Direction dir : directions) {
            BlockPos targetPos = pos.offset(dir);
            BlockEntity targetBE = world.getBlockEntity(targetPos);

            if (targetBE instanceof net.minecraft.inventory.Inventory targetInv) {
                for (int i = 0; i < INVENTORY_SIZE; i++) {
                    ItemStack slot = inventory.get(i);
                    if (slot.isEmpty()) continue;

                    ItemStack toTransfer = slot.copy();
                    toTransfer.setCount(1);

                    // 尝试向目标容器插入
                    if (insertIntoInventory(targetInv, toTransfer, dir.getOpposite())) {
                        slot.decrement(1);
                        if (slot.isEmpty()) {
                            inventory.set(i, ItemStack.EMPTY);
                        }
                        markDirty();
                        return; // 每 tick 只推送一个物品，避免过快
                    }
                }
            }
        }
    }

    private boolean insertIntoInventory(net.minecraft.inventory.Inventory inv, ItemStack stack, Direction side) {
        int[] slots;
        if (inv instanceof SidedInventory sided) {
            slots = sided.getAvailableSlots(side);
        } else {
            slots = new int[inv.size()];
            for (int i = 0; i < inv.size(); i++) slots[i] = i;
        }

        for (int slot : slots) {
            if (inv instanceof SidedInventory sided && !sided.canInsert(slot, stack, side)) continue;

            ItemStack existing = inv.getStack(slot);
            if (existing.isEmpty()) {
                inv.setStack(slot, stack.copy());
                inv.markDirty();
                return true;
            } else if (ItemStack.areItemsEqual(existing, stack)
                    && existing.getCount() < existing.getMaxCount()) {
                int transfer = Math.min(stack.getCount(), existing.getMaxCount() - existing.getCount());
                existing.increment(transfer);
                inv.markDirty();
                return true;
            }
        }
        return false;
    }

    // ===== NamedScreenHandlerFactory =====

    @Override
    public Text getDisplayName() {
        return Text.translatable("block.boxedmachines." + machineType.getBlockId());
    }

    @Nullable
    @Override
    public ScreenHandler createMenu(int syncId, PlayerInventory playerInventory, PlayerEntity player) {
        return new BoxedMachineScreenHandler(syncId, playerInventory, this);
    }

    // ===== Inventory 接口 =====

    @Override
    public int size() { return INVENTORY_SIZE; }

    @Override
    public boolean isEmpty() {
        for (ItemStack stack : inventory) {
            if (!stack.isEmpty()) return false;
        }
        return true;
    }

    @Override
    public ItemStack getStack(int slot) { return inventory.get(slot); }

    @Override
    public ItemStack removeStack(int slot, int amount) {
        ItemStack result = Inventories.splitStack(inventory, slot, amount);
        if (!result.isEmpty()) markDirty();
        return result;
    }

    @Override
    public ItemStack removeStack(int slot) {
        return Inventories.removeStack(inventory, slot);
    }

    @Override
    public void setStack(int slot, ItemStack stack) {
        inventory.set(slot, stack);
        if (stack.getCount() > getMaxCountPerStack()) {
            stack.setCount(getMaxCountPerStack());
        }
        markDirty();
    }

    @Override
    public boolean canPlayerUse(PlayerEntity player) {
        return true;
    }

    @Override
    public void clear() {
        inventory.clear();
        markDirty();
    }

    // ===== SidedInventory =====

    @Override
    public int[] getAvailableSlots(Direction side) {
        return ACCESSIBLE_SLOTS;
    }

    @Override
    public boolean canInsert(int slot, ItemStack stack, Direction dir) {
        return false; // 不允许从外部插入，只允许取出
    }

    @Override
    public boolean canExtract(int slot, ItemStack stack, Direction dir) {
        return true; // 允许漏斗从任意面提取
    }

    // ===== NBT 序列化 =====

    @Override
    protected void writeNbt(NbtCompound nbt, RegistryWrapper.WrapperLookup registryLookup) {
        super.writeNbt(nbt, registryLookup);
        Inventories.writeNbt(nbt, inventory, registryLookup);
        nbt.putInt("TicksSinceLastCycle", ticksSinceLastCycle);
    }

    @Override
    protected void readNbt(NbtCompound nbt, RegistryWrapper.WrapperLookup registryLookup) {
        super.readNbt(nbt, registryLookup);
        Inventories.readNbt(nbt, inventory, registryLookup);
        ticksSinceLastCycle = nbt.getInt("TicksSinceLastCycle");
    }

    public MachineType getMachineType() {
        return machineType;
    }
}
