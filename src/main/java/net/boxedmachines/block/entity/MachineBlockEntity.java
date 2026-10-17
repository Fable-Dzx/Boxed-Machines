package net.boxedmachines.block.entity;

import net.boxedmachines.ModBlockEntities;
import net.boxedmachines.machine.MachineSpec;
import net.minecraft.block.BlockState;
import net.minecraft.block.entity.BlockEntity;
import net.minecraft.entity.ItemEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.inventory.Inventory;
import net.minecraft.item.ItemStack;
import net.minecraft.storage.ReadView;
import net.minecraft.storage.WriteView;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

/**
 * 盒装机器方块实体：按设定间隔自动产出物品，存于内部槽位，右键一键收取。
 */
public class MachineBlockEntity extends BlockEntity {

    private static final int SLOT_COUNT = 6;

    private final MachineSpec spec;
    private final ItemStack[] slots = new ItemStack[SLOT_COUNT];
    private int progress = 0;

    public MachineBlockEntity(BlockPos pos, BlockState state, MachineSpec spec) {
        super(ModBlockEntities.MACHINE, pos, state);
        this.spec = spec;
        for (int i = 0; i < SLOT_COUNT; i++) {
            slots[i] = ItemStack.EMPTY;
        }
    }

    /** 每游戏刻调用一次（服务端）。 */
    public static void tick(World world, BlockPos pos, BlockState state, MachineBlockEntity machine) {
        machine.progress++;
        if (machine.progress >= machine.spec.interval()) {
            machine.progress = 0;
            machine.produce();
        }
    }

    private void produce() {
        if (world == null || world.isClient()) {
            return;
        }
        MachineSpec.Output output = spec.pick(world.random);
        int count = output.min();
        if (output.max() > output.min()) {
            count += world.random.nextInt(output.max() - output.min() + 1);
        }
        ItemStack stack = new ItemStack(output.item(), count);

        boolean placed = false;
        for (int i = 0; i < slots.length; i++) {
            if (slots[i].isEmpty()) {
                slots[i] = stack;
                placed = true;
                break;
            }
            if (slots[i].isOf(output.item())
                    && slots[i].getCount() + count <= slots[i].getMaxCount()) {
                slots[i].increment(count);
                placed = true;
                break;
            }
        }
        if (!placed) {
            dropItemStack(world, pos, stack);
        }
        markDirty();
    }

    /** 右键收取：把内部所有物品塞进玩家背包，装不下的掉落在玩家身边。 */
    public void collect(PlayerEntity player) {
        boolean changed = false;
        for (int i = 0; i < slots.length; i++) {
            if (!slots[i].isEmpty()) {
                ItemStack stack = slots[i];
                giveToPlayer(player, stack);
                slots[i] = ItemStack.EMPTY;
                changed = true;
            }
        }
        if (changed) {
            markDirty();
        }
    }

    private static void giveToPlayer(PlayerEntity player, ItemStack stack) {
        Inventory inventory = player.getInventory();
        ItemStack leftover = stack;
        for (int i = 0; i < inventory.size() && !leftover.isEmpty(); i++) {
            ItemStack slot = inventory.getStack(i);
            if (slot.isEmpty()) {
                inventory.setStack(i, leftover);
                leftover = ItemStack.EMPTY;
                break;
            }
            if (slot.isOf(leftover.getItem()) && slot.getCount() < slot.getMaxCount()) {
                int room = slot.getMaxCount() - slot.getCount();
                int move = Math.min(room, leftover.getCount());
                slot.increment(move);
                leftover.decrement(move);
            }
        }
        if (!leftover.isEmpty()) {
            player.dropItem(leftover, false);
        }
    }

    /** 方块被破坏时掉落内部物品。 */
    public void dropContents(World world, BlockPos pos) {
        for (ItemStack stack : slots) {
            if (!stack.isEmpty()) {
                dropItemStack(world, pos, stack);
            }
        }
    }

    private static void dropItemStack(World world, BlockPos pos, ItemStack stack) {
        double x = pos.getX() + 0.5 + (world.random.nextDouble() - 0.5) * 0.6;
        double y = pos.getY() + 0.7;
        double z = pos.getZ() + 0.5 + (world.random.nextDouble() - 0.5) * 0.6;
        ItemEntity entity = new ItemEntity(world, x, y, z, stack);
        entity.setVelocity(
                world.random.nextDouble() * 0.1 - 0.05,
                0.2,
                world.random.nextDouble() * 0.1 - 0.05);
        world.spawnEntity(entity);
    }

    /** 内部物品数量（0-15），用于比较器输出。 */
    public int comparatorOutput() {
        int count = 0;
        for (ItemStack stack : slots) {
            count += stack.getCount();
        }
        return Math.min(15, count);
    }

    @Override
    protected void writeData(WriteView view) {
        view.putInt("Progress", progress);
        WriteView.ListAppender<ItemStack> appender = view.getListAppender("Items", ItemStack.CODEC);
        for (ItemStack stack : slots) {
            if (!stack.isEmpty()) {
                appender.add(stack);
            }
        }
        super.writeData(view);
    }

    @Override
    protected void readData(ReadView view) {
        super.readData(view);
        progress = view.getInt("Progress", 0);
        view.getOptionalTypedListView("Items", ItemStack.CODEC).ifPresent(list -> {
            int i = 0;
            for (ItemStack stack : list) {
                if (i >= slots.length) {
                    break;
                }
                slots[i++] = stack;
            }
        });
    }
}
