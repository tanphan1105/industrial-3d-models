from PIL import Image, ImageDraw, ImageFont
import os

icons_dir = r"D:\WT3D_Project\Z_Tools\Assets\Icons"
os.makedirs(icons_dir, exist_ok=True)

def make_vector_app_icon(brand_code, letter, bg_color, text_color=(255,255,255), size=256, sub_text=""):
    """Tạo Icon Ứng Dụng Kỹ Thuật Siêu Nét Đúng Chuẩn Visual Style 2025/2026"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Bo góc App Icon chuẩn Autodesk/Apple (Squircle 24%)
    radius = int(size * 0.22)
    # Drop shadow
    draw.rounded_rectangle([4, 8, size-4, size], radius=radius, fill=(0, 0, 0, 90))
    # Base
    draw.rounded_rectangle([0, 0, size-8, size-8], radius=radius, fill=bg_color, outline=(255, 255, 255, 160), width=3)
    # Highlight
    draw.rounded_rectangle([3, 3, size-11, int((size-8)*0.45)], radius=radius-2, fill=(255, 255, 255, 40))
    
    # Letter / Logo Symbol
    try:
        font = ImageFont.truetype('ariblk.ttf', int(size * 0.46))
        font_sub = ImageFont.truetype('arialbd.ttf', int(size * 0.14))
    except:
        font = ImageFont.truetype('arialbd.ttf', int(size * 0.46))
        font_sub = ImageFont.load_default()
        
    bbox = draw.textbbox((0, 0), letter, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    ty_offset = -int(size * 0.06) if sub_text else -int(size * 0.02)
    tx = (size - 8 - tw) // 2
    ty = (size - 8 - th) // 2 + ty_offset
    
    # Letter Shadow
    draw.text((tx+2, ty+3), letter, font=font, fill=(0, 0, 0, 100))
    draw.text((tx, ty), letter, font=font, fill=text_color)
    
    if sub_text:
        s_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
        sw = s_bbox[2] - s_bbox[0]
        sx = (size - 8 - sw) // 2
        sy = ty + th + int(size * 0.06)
        draw.text((sx, sy), sub_text, font=font_sub, fill=(255, 255, 255, 240))
        
    return img

# 1. SolidWorks: Hộp Đỏ 3D Khối Chữ DS / SW
sw_img = Image.new('RGBA', (256, 256), (0,0,0,0))
sw_draw = ImageDraw.Draw(sw_img)
sw_draw.rounded_rectangle([4, 8, 252, 256], radius=56, fill=(0, 0, 0, 90))
sw_draw.rounded_rectangle([0, 0, 248, 248], radius=56, fill=(230, 35, 45), outline=(255,255,255,160), width=3)
sw_draw.rounded_rectangle([3, 3, 245, 110], radius=52, fill=(255,255,255,40))
f_sw = ImageFont.truetype('ariblk.ttf', 108)
f_sub = ImageFont.truetype('arialbd.ttf', 30)
sw_draw.text((26, 42), "SW", font=f_sw, fill=(255,255,255))
sw_draw.text((36, 170), "SOLIDWORKS", font=f_sub, fill=(255,255,255,230))
sw_img.save(os.path.join(icons_dir, "solidworks_app.png"))

# 2. Autodesk Inventor: Hộp Vàng Cam Chuẩn Hãng
inv_img = make_vector_app_icon("IN", "I", (235, 130, 20), sub_text="INVENTOR")
inv_img.save(os.path.join(icons_dir, "inventor_app.png"))

# 3. AutoCAD: Hộp Đỏ Chữ A
acad_img = make_vector_app_icon("AC", "A", (220, 30, 45), sub_text="AUTOCAD")
acad_img.save(os.path.join(icons_dir, "autocad_app.png"))

# 4. Revit: Hộp Xanh Dương Chữ R
rv_img = make_vector_app_icon("RV", "R", (15, 125, 210), sub_text="REVIT")
rv_img.save(os.path.join(icons_dir, "revit_app.png"))

# 5. Fusion 360: Hộp Cam Chữ F
fs_img = make_vector_app_icon("FS", "F", (235, 100, 30), sub_text="FUSION")
fs_img.save(os.path.join(icons_dir, "fusion_app.png"))

# 6. 3ds Max: Hộp Xanh Mòng Két Chữ 3
max_img = make_vector_app_icon("3D", "3", (25, 155, 175), sub_text="3DS MAX")
max_img.save(os.path.join(icons_dir, "3dsmax_app.png"))

# 7. CATIA: Hộp Xanh Đậm Navy Chữ C
cat_img = make_vector_app_icon("CA", "C", (0, 85, 165), sub_text="CATIA")
cat_img.save(os.path.join(icons_dir, "catia_app.png"))

# 8. Siemens NX: Hộp Xanh Lục Bảo Chữ NX
nx_img = make_vector_app_icon("NX", "NX", (0, 140, 150), sub_text="SIEMENS")
nx_img.save(os.path.join(icons_dir, "nx_app.png"))

print("All High-Res Vector App Icons Generated!")
