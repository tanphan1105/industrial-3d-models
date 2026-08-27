import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_badge(text_abbr, color_bg, size=76):
    """Tạo logo badge hình khối hiện đại bóng bẩy chuẩn Apple/Tech Icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Shadow
    draw.rounded_rectangle([2, 5, size-2, size], radius=16, fill=(0, 0, 0, 90))
    # Main Icon Rounded Box
    draw.rounded_rectangle([0, 0, size-4, size-4], radius=16, fill=color_bg, outline=(255, 255, 255, 140), width=1)
    
    # Top highlight sheen
    draw.rounded_rectangle([2, 2, size-6, int((size-4)*0.45)], radius=14, fill=(255, 255, 255, 45))
    
    # Text abbreviation
    try:
        font = ImageFont.truetype('arialbd.ttf', int(size * 0.38))
    except:
        font = ImageFont.load_default()
        
    bbox = draw.textbbox((0, 0), text_abbr, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - 4 - tw) // 2
    ty = (size - 4 - th) // 2 - 2
    
    draw.text((tx, ty), text_abbr, font=font, fill=(255, 255, 255, 255))
    return img

def generate_compatibility_banner(base_image_path, output_path):
    # Lấy ảnh gốc
    base_img = Image.open(base_image_path).convert('RGBA')
    W, H = base_img.size
    
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. TẦNG 1: Chữ ký Kính Quang Học Chính Giữa (WaterTreatment3D)
    center_title = "WaterTreatment3D"
    center_font_size = int(H * 0.102) # 147px
    try:
        center_font = ImageFont.truetype('ariblk.ttf', center_font_size)
    except:
        center_font = ImageFont.truetype('arialbd.ttf', center_font_size)
        
    c_bbox = draw.textbbox((0, 0), center_title, font=center_font)
    ctw = c_bbox[2] - c_bbox[0]
    cth = c_bbox[3] - c_bbox[1]
    
    c_pos_x = (W - ctw) // 2
    c_pos_y = int(H * 0.44) - (cth // 2)
    
    # Nổi cạnh 3D sáng/tối
    draw.text((c_pos_x + 1.4, c_pos_y + 1.4), center_title, font=center_font, fill=(0, 0, 0, 0), stroke_width=2, stroke_fill=(0, 0, 0, 85))
    draw.text((c_pos_x - 1.2, c_pos_y - 1.2), center_title, font=center_font, fill=(0, 0, 0, 0), stroke_width=2, stroke_fill=(255, 255, 255, 150))
    
    # Danh sách phần mềm: (Viết tắt, Tên hiển thị, Màu Brand RGB)
    softwares = [
        ("SW", "SolidWorks", (230, 40, 40)),
        ("IN", "Inventor", (235, 120, 20)),
        ("NX", "Siemens NX", (0, 140, 150)),
        ("CA", "CATIA", (0, 85, 160)),
        ("CR", "PTC Creo", (115, 170, 40)),
        ("FS", "Fusion 360", (225, 95, 30)),
        ("RV", "Revit BIM", (15, 125, 200)),
        ("AC", "AutoCAD", (210, 30, 45)),
        ("BL", "Blender", (235, 125, 25)),
        ("3D", "3ds Max", (30, 155, 170)),
        ("UE", "Unreal 5", (35, 35, 45)),
        ("FC", "FreeCAD", (195, 35, 45))
    ]
    
    # Ribbon Bar Dimensions (Dải dẹp góc dưới)
    bar_height = int(H * 0.088) # ~126px trên 2K
    bar_y = H - bar_height - int(H * 0.032) # Cách đáy 46px
    bar_margin_x = int(W * 0.025) # Cách lề 64px
    
    # Dành chỗ bên phải cho Thẻ Author Ribbon: tanphan1105
    author_tag = "tanphan1105"
    author_font_size = int(H * 0.038)
    try:
        author_font = ImageFont.truetype('arialbd.ttf', author_font_size)
    except:
        author_font = ImageFont.load_default()
        
    a_bbox = draw.textbbox((0, 0), author_tag, font=author_font)
    atw = a_bbox[2] - a_bbox[0]
    ath = a_bbox[3] - a_bbox[1]
    
    pad_x = int(W * 0.032)
    badge_w = atw + pad_x * 2
    badge_h = bar_height
    
    badge_x = W - badge_w - bar_margin_x
    badge_y = bar_y
    
    # Thanh Banner Trái (Dài từ lề trái đến sát thẻ Author)
    bar_w = badge_x - bar_margin_x - int(W * 0.012)
    
    # 2. VẼ DẢI THỦY TINH ĐEN FROSTED GLASS (BÊN TRÁI)
    glass_box = [bar_margin_x, bar_y, bar_margin_x + bar_w, bar_y + bar_height]
    draw.rounded_rectangle([glass_box[0]+3, glass_box[1]+5, glass_box[2]+3, glass_box[3]+5], radius=14, fill=(0, 0, 0, 90))
    draw.rounded_rectangle(glass_box, radius=14, fill=(12, 16, 24, 230), outline=(255, 255, 255, 60), width=1)
    
    # Tiêu đề bên trái
    try:
        title_font_1 = ImageFont.truetype('arialbd.ttf', int(bar_height * 0.22))
        title_font_2 = ImageFont.truetype('arial.ttf', int(bar_height * 0.17))
        name_font = ImageFont.truetype('arialbd.ttf', int(bar_height * 0.15))
    except:
        title_font_1 = title_font_2 = name_font = ImageFont.load_default()
        
    title_x = bar_margin_x + int(W * 0.015)
    title_y = bar_y + int(bar_height * 0.26)
    
    draw.text((title_x, title_y), "UNIVERSAL CAD FORMATS", font=title_font_1, fill=(255, 255, 255, 255))
    draw.text((title_x, title_y + int(bar_height * 0.30)), "STEP AP214 • IGES • SAT • FBX • OBJ", font=title_font_2, fill=(52, 199, 89, 255))
    
    # Vạch chia
    div_x = title_x + int(W * 0.16)
    draw.line([(div_x, bar_y + 14), (div_x, bar_y + bar_height - 14)], fill=(255, 255, 255, 45), width=1)
    
    # Vẽ các icon phần mềm
    icon_size = int(bar_height * 0.56)
    start_icons_x = div_x + int(W * 0.018)
    available_w = (bar_margin_x + bar_w) - start_icons_x - int(W * 0.012)
    spacing = available_w / len(softwares)
    
    for i, (abbr, name, col) in enumerate(softwares):
        ix = int(start_icons_x + (i * spacing) + (spacing - icon_size)/2)
        iy = bar_y + int(bar_height * 0.12)
        
        badge_img = create_badge(abbr, col, size=icon_size)
        overlay.paste(badge_img, (ix, iy), badge_img)
        
        bbox = draw.textbbox((0, 0), name, font=name_font)
        nw = bbox[2] - bbox[0]
        nx = ix + (icon_size - nw)//2
        ny = iy + icon_size + 2
        draw.text((nx, ny), name, font=name_font, fill=(215, 225, 240, 230))
        
    # 3. VẼ THẺ TÁC GIẢ RIBBON XANH EMERALD (BÊN PHẢI)
    green_box = [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h]
    draw.rounded_rectangle([green_box[0]+3, green_box[1]+5, green_box[2]+3, green_box[3]+5], radius=14, fill=(0, 0, 0, 90))
    draw.rounded_rectangle(green_box, radius=14, fill=(24, 150, 68, 240), outline=(255, 255, 255, 200), width=2)
    
    text_x = badge_x + (badge_w - atw) // 2
    text_y = badge_y + (badge_h - ath) // 2 - 2
    draw.text((text_x, text_y), author_tag, font=author_font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 200))
    
    # Ghép ảnh
    final_img = Image.alpha_composite(base_img, overlay)
    final_img.save(output_path, "PNG")
    print(f"Generated Banner Preview: {output_path}")

if __name__ == "__main__":
    # Test trên ảnh mô hình thực tế (den alarm)
    src = r"D:\WT3D_Project\Z_Tools\Demo_Watermark_Thin_Stroke_2K.png"
    out = r"D:\WT3D_Project\Z_Tools\Demo_Compatibility_Banner_2K.png"
    generate_compatibility_banner(src, out)
