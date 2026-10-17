package net.boxedmachines;

import net.boxedmachines.block.MachineBlock;
import net.boxedmachines.machine.MachineSpec;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.Block;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.registry.RegistryKey;
import net.minecraft.registry.RegistryKeys;
import net.minecraft.util.Identifier;

import java.util.ArrayList;
import java.util.List;

import static net.boxedmachines.machine.MachineSpec.out;

/**
 * 全部盒装机器方块与对应方块物品的注册。
 */
public final class ModBlocks {

    public static final List<Block> ALL_MACHINES = new ArrayList<>();

    // ---- 刷铁机：铁锭/铁粒 ----
    public static final MachineBlock IRON_FARM = machine("iron_farm",
            MachineSpec.of("iron_farm", 600,
                    out(net.minecraft.item.Items.IRON_INGOT, 1, 2, 10),
                    out(net.minecraft.item.Items.IRON_NUGGET, 2, 4, 5)));

    // ---- 自动钓鱼机（刷钩机）：鱼 + 杂物 ----
    public static final MachineBlock FISHING_MACHINE = machine("fishing_machine",
            MachineSpec.of("fishing_machine", 900,
                    out(net.minecraft.item.Items.COD, 1, 1, 6),
                    out(net.minecraft.item.Items.SALMON, 1, 1, 5),
                    out(net.minecraft.item.Items.PUFFERFISH, 1, 1, 2),
                    out(net.minecraft.item.Items.TROPICAL_FISH, 1, 1, 2),
                    out(net.minecraft.item.Items.BONE, 1, 1, 3),
                    out(net.minecraft.item.Items.STRING, 1, 1, 2),
                    out(net.minecraft.item.Items.ENCHANTED_BOOK, 1, 1, 1)));

    // ---- 岩浆机：岩浆桶 ----
    public static final MachineBlock LAVA_MACHINE = machine("lava_machine",
            MachineSpec.of("lava_machine", 1200,
                    out(net.minecraft.item.Items.LAVA_BUCKET, 1, 1, 10)));

    // ---- 岩浆烤鸡机：熟鸡肉 ----
    public static final MachineBlock LAVA_CHICKEN_MACHINE = machine("lava_chicken_machine",
            MachineSpec.of("lava_chicken_machine", 400,
                    out(net.minecraft.item.Items.COOKED_CHICKEN, 1, 2, 10),
                    out(net.minecraft.item.Items.FEATHER, 1, 2, 5)));

    // ---- 刷石机：圆石/石头 ----
    public static final MachineBlock COBBLESTONE_MACHINE = machine("cobblestone_machine",
            MachineSpec.of("cobblestone_machine", 100,
                    out(net.minecraft.item.Items.COBBLESTONE, 1, 2, 10),
                    out(net.minecraft.item.Items.STONE, 1, 1, 3)));

    // ---- 刷怪机：怪物掉落物 ----
    public static final MachineBlock MOB_FARM = machine("mob_farm",
            MachineSpec.of("mob_farm", 600,
                    out(net.minecraft.item.Items.GUNPOWDER, 1, 2, 6),
                    out(net.minecraft.item.Items.BONE, 1, 1, 5),
                    out(net.minecraft.item.Items.ROTTEN_FLESH, 1, 2, 6),
                    out(net.minecraft.item.Items.STRING, 1, 2, 5),
                    out(net.minecraft.item.Items.SPIDER_EYE, 1, 1, 2)));

    // ---- 刷金机：金粒/金锭 ----
    public static final MachineBlock GOLD_FARM = machine("gold_farm",
            MachineSpec.of("gold_farm", 600,
                    out(net.minecraft.item.Items.GOLD_NUGGET, 2, 4, 8),
                    out(net.minecraft.item.Items.GOLD_INGOT, 1, 1, 4)));

    // ---- 刷蜜机：蜂蜜瓶/蜜脾 ----
    public static final MachineBlock HONEY_FARM = machine("honey_farm",
            MachineSpec.of("honey_farm", 600,
                    out(net.minecraft.item.Items.HONEY_BOTTLE, 1, 1, 6),
                    out(net.minecraft.item.Items.HONEYCOMB, 1, 2, 8)));

    // ---- 甘蔗机：甘蔗/糖 ----
    public static final MachineBlock SUGARCANE_FARM = machine("sugarcane_farm",
            MachineSpec.of("sugarcane_farm", 600,
                    out(net.minecraft.item.Items.SUGAR_CANE, 1, 2, 10),
                    out(net.minecraft.item.Items.SUGAR, 1, 1, 3)));

    // ---- 瓜机：西瓜片/南瓜 ----
    public static final MachineBlock MELON_FARM = machine("melon_farm",
            MachineSpec.of("melon_farm", 600,
                    out(net.minecraft.item.Items.MELON_SLICE, 2, 4, 8),
                    out(net.minecraft.item.Items.PUMPKIN, 1, 1, 4),
                    out(net.minecraft.item.Items.PUMPKIN_SEEDS, 1, 2, 2)));

    // ---- 仙人掌机 ----
    public static final MachineBlock CACTUS_FARM = machine("cactus_farm",
            MachineSpec.of("cactus_farm", 600,
                    out(net.minecraft.item.Items.CACTUS, 1, 2, 10),
                    out(net.minecraft.item.Items.GREEN_DYE, 1, 1, 3)));

    // ---- 竹子机 ----
    public static final MachineBlock BAMBOO_FARM = machine("bamboo_farm",
            MachineSpec.of("bamboo_farm", 600,
                    out(net.minecraft.item.Items.BAMBOO, 1, 2, 10),
                    out(net.minecraft.item.Items.PAPER, 1, 1, 2)));

    // ---- 刷线机：线/白羊毛 ----
    public static final MachineBlock STRING_FARM = machine("string_farm",
            MachineSpec.of("string_farm", 600,
                    out(net.minecraft.item.Items.STRING, 1, 3, 10),
                    out(net.minecraft.item.Items.WHITE_WOOL, 1, 1, 3)));

    // ---- 刷骨机：骨头/骨粉 ----
    public static final MachineBlock BONE_FARM = machine("bone_farm",
            MachineSpec.of("bone_farm", 600,
                    out(net.minecraft.item.Items.BONE, 1, 2, 8),
                    out(net.minecraft.item.Items.BONE_MEAL, 2, 3, 6)));

    // ---- 末影珍珠机 ----
    public static final MachineBlock ENDER_PEARL_FARM = machine("ender_pearl_farm",
            MachineSpec.of("ender_pearl_farm", 900,
                    out(net.minecraft.item.Items.ENDER_PEARL, 1, 1, 8),
                    out(net.minecraft.item.Items.CHORUS_FRUIT, 1, 1, 4)));

    // ---- 经验机：附魔之瓶 ----
    public static final MachineBlock XP_MACHINE = machine("xp_machine",
            MachineSpec.of("xp_machine", 300,
                    out(net.minecraft.item.Items.EXPERIENCE_BOTTLE, 1, 1, 10)));

    // ---- 鸡蛋机 ----
    public static final MachineBlock EGG_FARM = machine("egg_farm",
            MachineSpec.of("egg_farm", 300,
                    out(net.minecraft.item.Items.EGG, 1, 2, 8),
                    out(net.minecraft.item.Items.FEATHER, 1, 1, 4)));

    // ---- 羊毛机 ----
    public static final MachineBlock WOOL_FARM = machine("wool_farm",
            MachineSpec.of("wool_farm", 600,
                    out(net.minecraft.item.Items.WHITE_WOOL, 1, 2, 10),
                    out(net.minecraft.item.Items.STRING, 1, 1, 3)));

    // ---- 烤牛肉机 ----
    public static final MachineBlock BEEF_MACHINE = machine("beef_machine",
            MachineSpec.of("beef_machine", 400,
                    out(net.minecraft.item.Items.COOKED_BEEF, 1, 1, 8),
                    out(net.minecraft.item.Items.LEATHER, 1, 1, 4)));

    // ---- 苔藓机 ----
    public static final MachineBlock MOSS_FARM = machine("moss_farm",
            MachineSpec.of("moss_farm", 600,
                    out(net.minecraft.item.Items.MOSS_BLOCK, 1, 1, 7),
                    out(net.minecraft.item.Items.MOSS_CARPET, 1, 2, 6),
                    out(net.minecraft.item.Items.BONE_MEAL, 1, 1, 3)));

    // ---- 蘑菇机 ----
    public static final MachineBlock MUSHROOM_FARM = machine("mushroom_farm",
            MachineSpec.of("mushroom_farm", 600,
                    out(net.minecraft.item.Items.BROWN_MUSHROOM, 1, 2, 5),
                    out(net.minecraft.item.Items.RED_MUSHROOM, 1, 2, 5),
                    out(net.minecraft.item.Items.MUSHROOM_STEW, 1, 1, 2)));

    // ---- 深板岩机 ----
    public static final MachineBlock DEEPSLATE_MACHINE = machine("deepslate_machine",
            MachineSpec.of("deepslate_machine", 200,
                    out(net.minecraft.item.Items.DEEPSLATE, 1, 2, 10),
                    out(net.minecraft.item.Items.COBBLED_DEEPSLATE, 1, 1, 4)));

    // ---- 石英机 ----
    public static final MachineBlock QUARTZ_FARM = machine("quartz_farm",
            MachineSpec.of("quartz_farm", 600,
                    out(net.minecraft.item.Items.QUARTZ, 1, 2, 10),
                    out(net.minecraft.item.Items.QUARTZ_BLOCK, 1, 1, 3)));

    // ---- 粘液机 ----
    public static final MachineBlock SLIME_FARM = machine("slime_farm",
            MachineSpec.of("slime_farm", 600,
                    out(net.minecraft.item.Items.SLIME_BALL, 1, 1, 10)));

    // ---- 红石机 ----
    public static final MachineBlock REDSTONE_MACHINE = machine("redstone_machine",
            MachineSpec.of("redstone_machine", 400,
                    out(net.minecraft.item.Items.REDSTONE, 2, 4, 10),
                    out(net.minecraft.item.Items.REDSTONE_TORCH, 1, 1, 2)));

    private ModBlocks() {
    }

    private static MachineBlock machine(String name, MachineSpec spec) {
        Identifier blockId = Identifier.of(BoxedMachines.MOD_ID, name);
        MachineBlock block = new MachineBlock(spec,
                AbstractBlock.Settings.create()
                        .strength(2.5f, 6.0f)
                        .sounds(BlockSoundGroup.METAL));
        Registry.register(Registries.BLOCK, blockId, block);

        RegistryKey<Item> itemKey = RegistryKey.of(RegistryKeys.ITEM, blockId);
        BlockItem blockItem = new BlockItem(block,
                new Item.Settings().useBlockPrefixedTranslationKey().registryKey(itemKey));
        Registry.register(Registries.ITEM, itemKey, blockItem);

        ALL_MACHINES.add(block);
        return block;
    }

    /** 触发静态初始化（被主类调用）。 */
    public static void initialize() {
    }
}
