from PIL import Image, ImageDraw, ImageFont
import os

icons_dir = r"D:\WT3D_Project\Z_Tools\Assets\Icons"

def normalize_to_exact_canvas(src_path, dst_path, canvas_size=200, pad_percent=0.08):
    """Cắt sạch khoảng trắng và scale vừa khít chính xác vào khung vuông canvas_size x canvas_size"""
    if not os.path.exists(src_path):
        return
    img = Image.open(src_path).convert('RGBA')
    bbox = img.getbbox()
    if not bbox:
        return
    cropped = img.crop(bbox)
    
    # Kích thước tối đa bên trong
    max_inner = int(canvas_size * (1.0 - pad_percent * 2))
    
    # Scale đồng bộ
    w, h = cropped.size
    scale = min(max_inner / w, max_inner / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Đặt vào tâm canvas vuông hoàn hảo
    canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    px = (canvas_size - new_w) // 2
    py = (canvas_size - new_h) // 2
    canvas.paste(resized, (px, py), resized)
    canvas.save(dst_path, "PNG")
    print(f"Normalized: {os.path.basename(dst_path)} (Exact size {canvas_size}x{canvas_size})")

# Chuẩn hóa 10 logo sang file `_norm.png`
items = [
    ("solidworks_cube_official.png", "sw_norm.png"),
    ("inventor_square.png", "inv_norm.png"),
    ("autocad_square.png", "acad_norm.png"),
    ("revit_square.png", "revit_norm.png"),
    ("fusion_square.png", "fusion_norm.png"),
    ("catia_cube_official.png", "catia_norm.png"),
    ("blender.png", "blender_norm.png"),
    ("3dsmax_square.png", "3dsmax_norm.png"),
    ("unreal.png", "unreal_norm.png"),
    ("freecad.png", "freecad_norm.png")
]

for src, dst in items:
    normalize_to_exact_canvas(os.path.join(icons_dir, src), os.path.join(icons_dir, dst), canvas_size=240, pad_percent=0.06)
