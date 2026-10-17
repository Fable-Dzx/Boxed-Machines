package com.boxedmachines.screen;

import com.boxedmachines.BoxedMachinesMod;
import com.boxedmachines.blockentity.BoxedMachineBlockEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.Inventory;
import net.minecraft.inventory.SimpleInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.screen.ScreenHandler;
import net.minecraft.screen.slot.Slot;

/**
 * 盒装机器的 GUI 容器。
 * 布局：3行9列（27槽）产出区 + 玩家背包
 * 产出槽只允许取出，不允许放入。
 */
public class BoxedMachineScreenHandler extends ScreenHandler {

    private final Inventory inventory;

    // 客户端用构造函数（无 BE 引用）
    public BoxedMachineScreenHandler(int syncId, PlayerInventory playerInventory) {
        this(syncId, playerInventory, new SimpleInventory(27));
    }

    // 服务端用构造函数
    public BoxedMachineScreenHandler(int syncId, PlayerInventory playerInventory, Inventory inventory) {
        super(BoxedMachinesMod.BOXED_MACHINE_SCREEN_HANDLER, syncId);
        this.inventory = inventory;
        inventory.onOpen(playerInventory.player);

        // 机器产出区：3行 x 9列（起始偏移：x=8, y=18）
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new OutputSlot(inventory, col + row * 9, 8 + col * 18, 18 + row * 18));
            }
        }

        // 玩家背包：3行 x 9列（y=86）
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInventory, col + row * 9 + 9, 8 + col * 18, 86 + row * 18));
            }
        }

        // 玩家快捷栏（y=144）
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInventory, col, 8 + col * 18, 144));
        }
    }

    @Override
    public boolean canUse(PlayerEntity player) {
        return this.inventory.canPlayerUse(player);
    }

    @Override
    public ItemStack quickMove(PlayerEntity player, int slotIndex) {
        ItemStack newStack = ItemStack.EMPTY;
        Slot slot = this.slots.get(slotIndex);

        if (slot.hasStack()) {
            ItemStack originalStack = slot.getStack();
            newStack = originalStack.copy();

            if (slotIndex < 27) {
                // 从机器移到玩家背包
                if (!this.insertItem(originalStack, 27, 63, true)) {
                    return ItemStack.EMPTY;
                }
            } else {
                // 从玩家背包移到机器（通常不允许，但保留接口）
                if (!this.insertItem(originalStack, 0, 27, false)) {
                    return ItemStack.EMPTY;
                }
            }

            if (originalStack.isEmpty()) {
                slot.setStack(ItemStack.EMPTY);
            } else {
                slot.markDirty();
            }
        }

        return newStack;
    }

    /**
     * 产出槽 — 只允许取出，不允许放入
     */
    private static class OutputSlot extends Slot {
        public OutputSlot(Inventory inventory, int index, int x, int y) {
            super(inventory, index, x, y);
        }

        @Override
        public boolean canInsert(ItemStack stack) {
            return false; // 不允许放入产出槽
        }
    }
}
