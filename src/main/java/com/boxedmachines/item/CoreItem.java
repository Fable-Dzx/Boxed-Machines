package com.boxedmachines.item;

import com.boxedmachines.util.MachineType;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.tooltip.TooltipType;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;

import java.util.List;

/**
 * 核心组件 — 每种盒装机器对应的中间合成材料。
 * 由机器外壳 + 红石芯片 + 对应材料合成。
 */
public class CoreItem extends Item {

    private final MachineType machineType;

    public CoreItem(Settings settings, MachineType machineType) {
        super(settings);
        this.machineType = machineType;
    }

    @Override
    public void appendTooltip(ItemStack stack, TooltipContext context, List<Text> tooltip, TooltipType type) {
        tooltip.add(Text.literal(machineType.getDisplayName() + "的核心组件")
                .formatted(Formatting.GRAY));
        tooltip.add(Text.literal(machineType.getCategory().getDisplayName())
                .formatted(Formatting.DARK_GRAY));
    }

    public MachineType getMachineType() {
        return machineType;
    }
}
