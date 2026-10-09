# Minecraft-Mod-Music

**GC Music Discs** (`gcmusicdiscs`): a NeoForge 1.21.1 mod that adds custom music discs.

## Discs

| Disc | Song |
|------|------|
| `music_disc_falling_behind` | Laufey - Falling Behind |

## Requirements

- JDK 21
- NeoForge 21.1.x (Minecraft 1.21.1)

## Building / running

```sh
./gradlew build        # jar ends up in build/libs/
./gradlew runClient    # launch a dev client
```

Get a disc in-game with `/give @s gcmusicdiscs:music_disc_falling_behind`.

## Adding a disc

Needs Python 3, Pillow and ffprobe (part of ffmpeg).

```sh
python3 tools/add_disc.py <id> "<Title>" "<Artist>" path/to/song.ogg --color 7a5cc0
```

This copies the `.ogg`, writes the `sounds.json`, jukebox song, item model and lang entries, generates a
placeholder 16x16 texture (replace `textures/item/music_disc_<id>.png` with your own art), and adds the
registration line to `ModItems.java`.

## Notes on audio

Audio must be Ogg Vorbis (`.ogg`). Only include music you have the rights to distribute if you publish the mod.

## License

MIT (code). Music files are not covered by this license.
