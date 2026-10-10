#!/usr/bin/env python3
"""Add a music disc to the mod.

Usage:
    python3 tools/add_disc.py <id> "<Title>" "<Artist>" <song.ogg> [--color RRGGBB] [--comparator 1-15]

Example:
    python3 tools/add_disc.py falling_behind "Falling Behind" "Laufey" ~/Downloads/song.ogg --color 7a5cc0

What it does (everything the code can't do for you):
  - copies the .ogg to assets/gcmusicdiscs/sounds/records/<id>.ogg
  - reads the song length with ffprobe (needed for the jukebox song JSON)
  - writes data/gcmusicdiscs/jukebox_song/<id>.json
  - writes assets/gcmusicdiscs/models/item/music_disc_<id>.json
  - generates a 16x16 placeholder texture (replace it with your own art any time)
  - adds the sounds.json and en_us.json entries
  - adds the registration line to ModItems.java
  - adds the disc to the dungeon loot table (chests/dungeon_discs.json)

<id> must be lowercase letters, digits and underscores. Needs ffprobe and Pillow.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

MODID = "gcmusicdiscs"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "src/main/resources/assets" / MODID
DATA = ROOT / "src/main/resources/data" / MODID
MOD_ITEMS = ROOT / "src/main/java/com/diamond/gcmusicdiscs/ModItems.java"
MARKER = "// ADD_DISCS_ABOVE"
LOOT_TABLE = DATA / "loot_table/chests/dungeon_discs.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def duration_seconds(ogg: Path) -> int:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ogg)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return max(1, round(float(out)))


def make_texture(path: Path, color: str) -> None:
    """Simple vinyl-style disc: coloured ring, dark grooves, light label, centre hole."""
    r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    base, dark, light = (r, g, b, 255), (r // 3, g // 3, b // 3, 255), (min(255, r + 90), min(255, g + 90), min(255, b + 90), 255)
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    cx = cy = 7.5
    for y in range(16):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d > 7.6:
                continue
            if d < 1.2:
                continue  # centre hole
            if d < 3.4:
                img.putpixel((x, y), light)  # label
            elif d > 6.6:
                img.putpixel((x, y), dark)  # rim
            else:
                img.putpixel((x, y), dark if int(d) % 2 == 0 else base)  # grooves
    # small highlight
    for x, y in ((4, 3), (5, 3), (3, 4)):
        img.putpixel((x, y), light)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def main() -> int:
    ap = argparse.ArgumentParser(description="Add a music disc to the mod")
    ap.add_argument("id")
    ap.add_argument("title")
    ap.add_argument("artist")
    ap.add_argument("ogg", type=Path)
    ap.add_argument("--color", default="5c7ac0", help="placeholder texture colour, hex RRGGBB")
    ap.add_argument("--comparator", type=int, default=1, help="comparator output 1-15")
    a = ap.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9_]*", a.id):
        sys.exit("id must be lowercase letters, digits and underscores, starting with a letter")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", a.color):
        sys.exit("--color must be 6 hex digits, e.g. 7a5cc0")
    if not 1 <= a.comparator <= 15:
        sys.exit("--comparator must be between 1 and 15")
    if not a.ogg.is_file():
        sys.exit(f"audio file not found: {a.ogg}")

    # audio
    dest = ASSETS / "sounds/records" / f"{a.id}.ogg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if a.ogg.resolve() != dest.resolve():
        shutil.copyfile(a.ogg, dest)
    length = duration_seconds(dest)

    # sounds.json
    sounds_path = ASSETS / "sounds.json"
    sounds = load_json(sounds_path)
    sounds[f"music_disc.{a.id}"] = {"sounds": [{"name": f"{MODID}:records/{a.id}", "stream": True}]}
    save_json(sounds_path, sounds)

    # jukebox song
    save_json(DATA / "jukebox_song" / f"{a.id}.json", {
        "comparator_output": a.comparator,
        "description": {"translate": f"jukebox_song.{MODID}.{a.id}"},
        "length_in_seconds": length,
        "sound_event": f"{MODID}:music_disc.{a.id}",
    })

    # item model + texture
    save_json(ASSETS / "models/item" / f"music_disc_{a.id}.json", {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": f"{MODID}:item/music_disc_{a.id}"},
    })
    tex = ASSETS / "textures/item" / f"music_disc_{a.id}.png"
    if not tex.exists():
        make_texture(tex, a.color)

    # lang
    lang_path = ASSETS / "lang/en_us.json"
    lang = load_json(lang_path)
    lang[f"item.{MODID}.music_disc_{a.id}"] = "Music Disc"
    lang[f"jukebox_song.{MODID}.{a.id}"] = f"{a.artist} - {a.title}"
    save_json(lang_path, lang)

    # dungeon loot (the table is attached to minecraft:chests/simple_dungeon by a global loot modifier)
    loot = load_json(LOOT_TABLE)
    if loot:
        entries = loot["pools"][0]["entries"]
        item_id = f"{MODID}:music_disc_{a.id}"
        if not any(e.get("name") == item_id for e in entries):
            entries.append({"type": "minecraft:item", "name": item_id})
            save_json(LOOT_TABLE, loot)

    # Java registration
    java = MOD_ITEMS.read_text(encoding="utf-8")
    const = a.id.upper()
    line = f'    public static final DeferredItem<Item> {const} = disc("{a.id}");'
    if f'disc("{a.id}")' in java:
        print("ModItems.java already registers this disc; left unchanged")
    elif MARKER not in java:
        print(f"Marker '{MARKER}' missing from ModItems.java; add this line yourself:\n{line}")
    else:
        MOD_ITEMS.write_text(java.replace(f"    {MARKER}", f"{line}\n    {MARKER}"), encoding="utf-8")

    print(f"Added disc '{a.id}': {a.artist} - {a.title} ({length}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
