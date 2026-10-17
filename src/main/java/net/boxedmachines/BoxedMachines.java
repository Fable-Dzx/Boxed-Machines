package net.boxedmachines;

import net.fabricmc.api.ModInitializer;

public class BoxedMachines implements ModInitializer {

    public static final String MOD_ID = "boxedmachines";

    @Override
    public void onInitialize() {
        ModBlocks.initialize();
        ModItems.initialize();
        ModBlockEntities.initialize();
    }
}
