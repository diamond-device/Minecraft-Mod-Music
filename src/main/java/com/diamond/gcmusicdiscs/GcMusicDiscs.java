package com.diamond.gcmusicdiscs;

import net.minecraft.world.item.CreativeModeTabs;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;

@Mod(GcMusicDiscs.MODID)
public class GcMusicDiscs {
    public static final String MODID = "gcmusicdiscs";

    public GcMusicDiscs(IEventBus modEventBus) {
        // ModItems must be touched first: declaring a disc also registers its sound event.
        ModItems.ITEMS.register(modEventBus);
        ModSounds.SOUND_EVENTS.register(modEventBus);

        modEventBus.addListener(this::addToCreativeTabs);
    }

    private void addToCreativeTabs(BuildCreativeModeTabContentsEvent event) {
        // Vanilla music discs live in "Tools & Utilities"
        if (event.getTabKey() == CreativeModeTabs.TOOLS_AND_UTILITIES) {
            ModItems.DISCS.forEach(event::accept);
        }
    }
}
