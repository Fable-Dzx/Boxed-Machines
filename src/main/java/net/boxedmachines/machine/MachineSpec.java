package net.boxedmachines.machine;

import net.minecraft.item.Item;
import net.minecraft.util.math.random.Random;

import java.util.List;

/**
 * 一台盒装机器的生产参数：产出间隔（tick）与带权重的产出列表。
 */
public record MachineSpec(String id, int interval, List<Output> outputs) {

    public record Output(Item item, int min, int max, int weight) {
    }

    public static MachineSpec of(String id, int interval, Output... outputs) {
        return new MachineSpec(id, interval, List.of(outputs));
    }

    public static Output out(Item item, int min, int max, int weight) {
        return new Output(item, min, max, weight);
    }

    public static final MachineSpec EMPTY = new MachineSpec("empty", 100, List.of());

    /** 按权重随机挑选一种产出。 */
    public Output pick(Random random) {
        int total = 0;
        for (Output output : outputs) {
            total += output.weight();
        }
        if (total <= 0) {
            return outputs.get(0);
        }
        int roll = random.nextInt(total);
        int acc = 0;
        for (Output output : outputs) {
            acc += output.weight();
            if (roll < acc) {
                return output;
            }
        }
        return outputs.get(outputs.size() - 1);
    }
}
