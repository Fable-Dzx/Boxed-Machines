package com.boxedmachines;

import com.boxedmachines.block.BoxedMachineBlock;
import com.boxedmachines.blockentity.BoxedMachineBlockEntity;
import com.boxedmachines.item.BoxedMachineItem;
import com.boxedmachines.item.CoreItem;
import com.boxedmachines.item.MachineCasingItem;
import com.boxedmachines.item.RedstoneChipItem;
import com.boxedmachines.screen.BoxedMachineScreenHandler;
import com.boxedmachines.util.MachineType;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.inventory.SimpleInventory;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.registry.RegistryKey;
import net.minecraft.registry.RegistryKeys;
import net.minecraft.resource.featuretoggle.FeatureSet;
import net.minecraft.screen.ScreenHandlerType;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.util.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

public class BoxedMachinesMod implements ModInitializer {

    public static final String MOD_ID = "boxedmachines";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    // 方块注册表
    public static final Map<MachineType, Block> MACHINE_BLOCKS = new HashMap<>();
    // 方块物品注册表
    public static final Map<MachineType, BlockItem> MACHINE_ITEMS = new HashMap<>();
    // 方块实体类型注册表
    public static final Map<MachineType, BlockEntityType<?>> MACHINE_BLOCK_ENTITY_TYPES = new HashMap<>();

    // 基础材料物品
    public static Item MACHINE_CASING;
    public static Item REDSTONE_CHIP;

    // 核心组件物品
    public static final Map<MachineType, Item> CORE_ITEMS = new HashMap<>();

    // ScreenHandler 类型
    public static ScreenHandlerType<BoxedMachineScreenHandler> BOXED_MACHINE_SCREEN_HANDLER;

    @Override
    public void onInitialize() {
        LOGGER.info("盒装机器模组加载中...");

        // 注册基础材料
        MACHINE_CASING = Registry.register(
                Registries.ITEM,
                id("machine_casing"),
                new MachineCasingItem(new Item.Settings())
        );

        REDSTONE_CHIP = Registry.register(
                Registries.ITEM,
                id("redstone_chip"),
                new RedstoneChipItem(new Item.Settings())
        );

        // 注册 ScreenHandler 类型
        BOXED_MACHINE_SCREEN_HANDLER = Registry.register(
                Registries.SCREEN_HANDLER,
                id("boxed_machine"),
                new ScreenHandlerType<>(BoxedMachineScreenHandler::new, FeatureSet.empty())
        );

        // 逐台注册所有盒装机器
        for (MachineType type : MachineType.values()) {
            registerMachine(type);
        }

        // 添加到创造模式物品栏
        ItemGroupEvents.modifyEntriesEvent(net.minecraft.item.ItemGroups.REDSTONE).register(entries -> {
            entries.add(MACHINE_CASING);
            entries.add(REDSTONE_CHIP);
            for (MachineType type : MachineType.values()) {
                if (CORE_ITEMS.containsKey(type)) {
                    entries.add(CORE_ITEMS.get(type));
                }
                entries.add(MACHINE_ITEMS.get(type));
            }
        });

        LOGGER.info("盒装机器模组加载完成！共注册 {} 种机器。", MachineType.values().length);
    }

    private void registerMachine(MachineType type) {
        Identifier blockId = id(type.getBlockId());
        Identifier itemId = id(type.getBlockId());
        Identifier beId = id(type.getBlockId());

        // 创建方块
        Block block = new BoxedMachineBlock(
                AbstractBlock.Settings.create()
                        .strength(5.0f)
                        .requiresTool()
                        .sounds(BlockSoundGroup.METAL)
                        .nonOpaque(),
                type
        );

        Registry.register(Registries.BLOCK, blockId, block);
        MACHINE_BLOCKS.put(type, block);

        // 创建方块物品
        BlockItem blockItem = new BoxedMachineItem(block, new Item.Settings(), type);
        Registry.register(Registries.ITEM, itemId, blockItem);
        MACHINE_ITEMS.put(type, blockItem);

        // 创建方块实体类型
        BlockEntityType<BoxedMachineBlockEntity> beType = Registry.register(
                Registries.BLOCK_ENTITY_TYPE,
                beId,
                BlockEntityType.Builder.create(
                        (pos, state) -> new BoxedMachineBlockEntity(
                                MACHINE_BLOCK_ENTITY_TYPES.get(type), pos, state, type
                        ),
                        block
                ).build()
        );
        MACHINE_BLOCK_ENTITY_TYPES.put(type, beType);

        // 注册核心组件物品
        Identifier coreId = id(type.getCoreId());
        Item coreItem = Registry.register(
                Registries.ITEM,
                coreId,
                new CoreItem(new Item.Settings(), type)
        );
        CORE_ITEMS.put(type, coreItem);
    }

    public static Identifier id(String path) {
        return Identifier.of(MOD_ID, path);
    }
}
