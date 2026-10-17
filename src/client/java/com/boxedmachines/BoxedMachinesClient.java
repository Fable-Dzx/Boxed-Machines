package com.boxedmachines;

import com.boxedmachines.screen.BoxedMachineScreen;
import net.fabricmc.api.ClientModInitializer;
import net.minecraft.client.gui.screen.ingame.HandledScreens;

public class BoxedMachinesClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        // 注册 GUI 界面
        HandledScreens.register(BoxedMachinesMod.BOXED_MACHINE_SCREEN_HANDLER, BoxedMachineScreen::new);
    }
}
