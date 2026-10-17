package com.boxedmachines.item;

import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.tooltip.TooltipType;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;

import java.util.List;

/**
 * 机器外壳 — 所有盒装机器的基础结构材料
 */
public class MachineCasingItem extends Item {

    public MachineCasingItem(Settings settings) {
        super(settings);
    }

    @Override
    public void appendTooltip(ItemStack stack, TooltipContext context, List<Text> tooltip, TooltipType type) {
        tooltip.add(Text.literal("盒装机器的通用外壳")
                .formatted(Formatting.GRAY));
        tooltip.add(Text.literal("由铁锭、红石、黑曜石和石英锻造而成")
                .formatted(Formatting.DARK_GRAY));
    }
}
