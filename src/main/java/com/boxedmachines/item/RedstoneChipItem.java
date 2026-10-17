package com.boxedmachines.item;

import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.tooltip.TooltipType;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;

import java.util.List;

/**
 * 红石芯片 — 盒装机器的核心电路元件
 */
public class RedstoneChipItem extends Item {

    public RedstoneChipItem(Settings settings) {
        super(settings);
    }

    @Override
    public void appendTooltip(ItemStack stack, TooltipContext context, List<Text> tooltip, TooltipType type) {
        tooltip.add(Text.literal("封装了红石逻辑的精密芯片")
                .formatted(Formatting.GRAY));
        tooltip.add(Text.literal("由红石块、金锭和钻石合成")
                .formatted(Formatting.DARK_GRAY));
    }
}
