package com.diamond.gcmusicdiscs;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.JukeboxSong;
import net.minecraft.world.item.Rarity;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(GcMusicDiscs.MODID);

    /** Every disc declared via {@link #disc(String)}, used to fill the creative tab. */
    public static final List<DeferredItem<Item>> DISCS = new ArrayList<>();

    /**
     * Declares a disc. For name "foo" this registers:
     *  - item  gcmusicdiscs:music_disc_foo
     *  - sound gcmusicdiscs:music_disc.foo
     * and points the item at the data-driven jukebox song gcmusicdiscs:foo
     * (data/gcmusicdiscs/jukebox_song/foo.json).
     */
    private static DeferredItem<Item> disc(String name) {
        ModSounds.registerDisc(name);
        ResourceKey<JukeboxSong> song = ResourceKey.create(Registries.JUKEBOX_SONG,
                ResourceLocation.fromNamespaceAndPath(GcMusicDiscs.MODID, name));
        DeferredItem<Item> item = ITEMS.registerSimpleItem("music_disc_" + name,
                new Item.Properties().stacksTo(1).rarity(Rarity.RARE).jukeboxPlayable(song));
        DISCS.add(item);
        return item;
    }

    // --- Discs (tools/add_disc.py appends new ones above the marker) ---
    public static final DeferredItem<Item> FALLING_BEHIND = disc("falling_behind");
    public static final DeferredItem<Item> THE_MIND_ELECTRIC = disc("the_mind_electric");
    public static final DeferredItem<Item> AFTER_DARK = disc("after_dark");
    public static final DeferredItem<Item> CICADA = disc("cicada");
    // ADD_DISCS_ABOVE
}
