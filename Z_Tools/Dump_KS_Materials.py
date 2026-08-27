# -*- coding: utf-8 -*-
# KeyShot Full Asset Library Dumper v2
# Chạy trong KeyShot Scripting Console
# Output → d:\WT3D_Project\Z_Tools\keyshot_assets_dump.txt

import lux

out_path = r"d:\WT3D_Project\Z_Tools\keyshot_assets_dump.txt"

def dump_section(f, title, items):
    f.write(f"\n{'='*60}\n")
    f.write(f"  {title} ({len(items)} items)\n")
    f.write(f"{'='*60}\n")
    for i, item in enumerate(items):
        try:
            f.write(f"  {i:04d}  {str(item)}\n")
        except:
            f.write(f"  {i:04d}  [unreadable]\n")

sections = [
    ("MATERIALS",    "getLibraryMaterials"),
    ("ENVIRONMENTS", "getLibraryEnvironments"),
    ("BACKPLATES",   "getLibraryBackplates"),
    ("COLORS",       "getLibraryColors"),
    ("TEXTURES",     "getLibraryTextures"),
]

with open(out_path, "w", encoding="utf-8") as f:
    f.write("KeyShot Full Asset Library Dump\n")
    for title, fn_name in sections:
        try:
            fn = getattr(lux, fn_name)
            items = list(fn()) or []
            dump_section(f, title, items)
            print(f"✅ {title}: {len(items)} items")
        except Exception as e:
            f.write(f"\n[{title}] ERROR: {e}\n")
            print(f"❌ {title}: {e}")

print(f"\n→ Saved: {out_path}")
