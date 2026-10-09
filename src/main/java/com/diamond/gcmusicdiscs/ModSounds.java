package com.diamond.gcmusicdiscs;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModSounds {
    public static final DeferredRegister<SoundEvent> SOUND_EVENTS =
            DeferredRegister.create(Registries.SOUND_EVENT, GcMusicDiscs.MODID);

    /** Registers the sound event "gcmusicdiscs:music_disc.<name>" (mapped to a file in sounds.json). */
    static DeferredHolder<SoundEvent, SoundEvent> registerDisc(String name) {
        String id = "music_disc." + name;
        return SOUND_EVENTS.register(id, () -> SoundEvent.createVariableRangeEvent(
                ResourceLocation.fromNamespaceAndPath(GcMusicDiscs.MODID, id)));
    }
}
