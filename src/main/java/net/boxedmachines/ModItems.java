package net.boxedmachines;

import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.registry.RegistryKey;
import net.minecraft.registry.RegistryKeys;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

/**
 * 中间合成物品（机械齿轮、盒装机壳）与自定义创造物品栏。
 */
public final class ModItems {

    public static final Item MECHANISM_GEAR = registerItem("mechanism_gear");
    public static final Item BOXED_CASING = registerItem("boxed_casing");

    public static final RegistryKey<ItemGroup> GROUP_KEY =
            RegistryKey.of(RegistryKeys.ITEM_GROUP, Identifier.of(BoxedMachines.MOD_ID, "machines"));

    private ModItems() {
    }

    private static Item registerItem(String name) {
        Identifier id = Identifier.of(BoxedMachines.MOD_ID, name);
        RegistryKey<Item> key = RegistryKey.of(RegistryKeys.ITEM, id);
        Item item = new Item(new Item.Settings().registryKey(key));
        Registry.register(Registries.ITEM, key, item);
        return item;
    }

    public static void initialize() {
        ItemGroup group = FabricItemGroup.builder()
                .icon(() -> new ItemStack(ModBlocks.IRON_FARM))
                .displayName(Text.translatable("itemGroup.boxedmachines"))
                .build();
        Registry.register(Registries.ITEM_GROUP, GROUP_KEY, group);

        ItemGroupEvents.modifyEntriesEvent(GROUP_KEY).register(entries -> {
            entries.add(MECHANISM_GEAR);
            entries.add(BOXED_CASING);
            ModBlocks.ALL_MACHINES.forEach(entries::add);
        });
    }
}
