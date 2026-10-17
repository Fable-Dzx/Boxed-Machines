package com.boxedmachines.item;

import com.boxedmachines.util.MachineType;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.ItemStack;
import net.minecraft.item.tooltip.TooltipType;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;

import java.util.List;

/**
 * 盒装机器方块对应的物品。
 * 在 tooltip 中显示机器名称、类别和产出物。
 */
public class BoxedMachineItem extends BlockItem {

    private final MachineType machineType;

    public BoxedMachineItem(Block block, Settings settings, MachineType machineType) {
        super(block, settings);
        this.machineType = machineType;
    }

    @Override
    public void appendTooltip(ItemStack stack, TooltipContext context, List<Text> tooltip, TooltipType type) {
        tooltip.add(Text.literal(machineType.getCategory().getDisplayName())
                .formatted(Formatting.GRAY));

        tooltip.add(Text.empty());
        tooltip.add(Text.literal("产出物:").formatted(Formatting.YELLOW));

        for (MachineType.Output output : machineType.getOutputs()) {
            ItemStack outStack = new ItemStack(output.item(), output.count());
            tooltip.add(Text.literal("  ")
                    .append(outStack.getName())
                    .append(Text.literal(" x" + output.count()))
                    .formatted(Formatting.WHITE));
        }

        tooltip.add(Text.empty());
        double secondsPerCycle = machineType.getTicksPerCycle() / 20.0;
        tooltip.add(Text.literal(String.format("产出间隔: %.1f 秒", secondsPerCycle))
                .formatted(Formatting.AQUA));

        tooltip.add(Text.literal("放置即自动运行").formatted(Formatting.GREEN));
    }
}
