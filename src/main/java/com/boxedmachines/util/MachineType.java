package com.boxedmachines.util;

import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;

/**
 * 所有盒装机器的类型定义。
 * 每种机器定义了产出物、产出间隔和颜色标识。
 * ticksPerCycle: 每多少游戏刻产出一轮（20刻=1秒）
 */
public enum MachineType {

    // ===== 刷怪农场 =====
    IRON_FARM("盒装刷铁机", 0xD8D8D8, 200,
            new Output(Items.IRON_INGOT, 2), new Output(Items.POPPY, 1)),
    GOLD_FARM("盒装刷金机", 0xFED959, 300,
            new Output(Items.GOLD_INGOT, 2), new Output(Items.GOLD_NUGGET, 4)),
    GUARDIAN_FARM("盒装刷钩机", 0x5BA89A, 160,
            new Output(Items.PRISMARINE_SHARD, 2), new Output(Items.PRISMARINE_CRYSTALS, 1), new Output(Items.COD, 1)),
    BLAZE_FARM("盒装烈焰刷怪机", 0xFFAA00, 240,
            new Output(Items.BLAZE_ROD, 1)),
    ENDERMAN_FARM("盒装末影人机", 0x16162E, 300,
            new Output(Items.ENDER_PEARL, 1)),
    CREEPER_FARM("盒装苦力怕机", 0x4CAF50, 200,
            new Output(Items.GUNPOWDER, 2)),
    SKELETON_FARM("盒装骷髅机", 0xC8C8C8, 200,
            new Output(Items.BONE, 2), new Output(Items.ARROW, 3)),
    ZOMBIE_FARM("盒装僵尸机", 0x2D7835, 200,
            new Output(Items.ROTTEN_FLESH, 3), new Output(Items.IRON_INGOT, 1)),
    SPIDER_FARM("盒装蜘蛛机", 0x5C1A1A, 200,
            new Output(Items.STRING, 2), new Output(Items.SPIDER_EYE, 1)),
    SLIME_FARM("盒装史莱姆机", 0x7EC850, 240,
            new Output(Items.SLIME_BALL, 2)),
    WITCH_FARM("盒装女巫机", 0x4A3656, 260,
            new Output(Items.REDSTONE, 3), new Output(Items.GLOWSTONE_DUST, 2), new Output(Items.GLASS_BOTTLE, 1), new Output(Items.SUGAR, 1)),
    WITHER_SKELETON_FARM("盒装凋灵骷髅机", 0x1A1A1A, 400,
            new Output(Items.COAL, 2), new Output(Items.BONE, 2)),

    // ===== 动物农场 =====
    CHICKEN_COOKER("盒装岩浆烤鸡机", 0xE85030, 160,
            new Output(Items.COOKED_CHICKEN, 2), new Output(Items.FEATHER, 1)),
    CHICKEN_FARM("盒装养鸡机", 0xF5F5DC, 200,
            new Output(Items.CHICKEN, 1), new Output(Items.EGG, 1), new Output(Items.FEATHER, 1)),
    COW_FARM("盒装养牛机", 0x6B4226, 200,
            new Output(Items.BEEF, 1), new Output(Items.LEATHER, 1)),
    SHEEP_FARM("盒装养羊机", 0xE8E8E8, 200,
            new Output(Items.WHITE_WOOL, 2), new Output(Items.MUTTON, 1)),
    PIG_FARM("盒装养猪机", 0xE89B9B, 200,
            new Output(Items.PORKCHOP, 2)),

    // ===== 资源生成 =====
    LAVA_MACHINE("盒装岩浆机", 0xCF4A16, 600,
            new Output(Items.LAVA_BUCKET, 1)),
    COBBLESTONE_MACHINE("盒装造石机", 0x8B8B8B, 80,
            new Output(Items.COBBLESTONE, 4)),
    SNOW_MACHINE("盒装刷雪机", 0xE8F4FF, 120,
            new Output(Items.SNOWBALL, 4)),
    ICE_MACHINE("盒装冰机", 0x99CCFF, 200,
            new Output(Items.ICE, 2)),

    // ===== 植物农场 =====
    AUTO_FARM("盒装自动农场", 0x8BC34A, 160,
            new Output(Items.WHEAT, 3), new Output(Items.CARROT, 2), new Output(Items.POTATO, 2), new Output(Items.BEETROOT, 1)),
    SUGARCANE_MACHINE("盒装甘蔗机", 0x90C060, 160,
            new Output(Items.SUGAR_CANE, 3)),
    CACTUS_MACHINE("盒装仙人掌机", 0x1B6B1A, 200,
            new Output(Items.CACTUS, 2)),
    TREE_FARM("盒装伐木机", 0x795548, 240,
            new Output(Items.OAK_LOG, 4), new Output(Items.OAK_SAPLING, 1)),
    FISHING_MACHINE("盒装钓鱼机", 0x2196F3, 400,
            new Output(Items.COD, 2)),

    // ===== 特殊 =====
    RAID_FARM("盒装袭击机", 0xB71C1C, 600,
            new Output(Items.EMERALD, 3), new Output(Items.TOTEM_OF_UNDYING, 1));

    private final String displayName;
    private final int color;
    private final int ticksPerCycle;
    private final Output[] outputs;

    MachineType(String displayName, int color, int ticksPerCycle, Output... outputs) {
        this.displayName = displayName;
        this.color = color;
        this.ticksPerCycle = ticksPerCycle;
        this.outputs = outputs;
    }

    public String getDisplayName() { return displayName; }
    public int getColor() { return color; }
    public int getTicksPerCycle() { return ticksPerCycle; }
    public Output[] getOutputs() { return outputs; }

    public ItemStack[] getOutputStacks() {
        ItemStack[] stacks = new ItemStack[outputs.length];
        for (int i = 0; i < outputs.length; i++) {
            stacks[i] = new ItemStack(outputs[i].item(), outputs[i].count());
        }
        return stacks;
    }

    public String asString() {
        return name().toLowerCase();
    }

    /**
     * 获取用于方块注册的 ID（带 boxed_ 前缀）
     */
    public String getBlockId() {
        return "boxed_" + asString();
    }

    /**
     * 获取用于核心组件注册的 ID
     */
    public String getCoreId() {
        return asString() + "_core";
    }

    // ===== 分类 =====
    public enum Category {
        MOB_FARM("刷怪农场"),
        ANIMAL_FARM("动物农场"),
        RESOURCE_GEN("资源生成"),
        PLANT_FARM("植物农场"),
        SPECIAL("特殊");

        private final String displayName;
        Category(String displayName) { this.displayName = displayName; }
        public String getDisplayName() { return displayName; }
    }

    public Category getCategory() {
        return switch (this) {
            case IRON_FARM, GOLD_FARM, GUARDIAN_FARM, BLAZE_FARM, ENDERMAN_FARM,
                 CREEPER_FARM, SKELETON_FARM, ZOMBIE_FARM, SPIDER_FARM, SLIME_FARM,
                 WITCH_FARM, WITHER_SKELETON_FARM -> Category.MOB_FARM;
            case CHICKEN_COOKER, CHICKEN_FARM, COW_FARM, SHEEP_FARM, PIG_FARM -> Category.ANIMAL_FARM;
            case LAVA_MACHINE, COBBLESTONE_MACHINE, SNOW_MACHINE, ICE_MACHINE -> Category.RESOURCE_GEN;
            case AUTO_FARM, SUGARCANE_MACHINE, CACTUS_MACHINE, TREE_FARM, FISHING_MACHINE -> Category.PLANT_FARM;
            case RAID_FARM -> Category.SPECIAL;
        };
    }

    /**
     * 产出物定义
     */
    public record Output(net.minecraft.item.Item item, int count) {}
}
