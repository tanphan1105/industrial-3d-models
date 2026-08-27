import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

def create_tech_badge(abbr, color_bg, size=52):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Shadow
    draw.rounded_rectangle([1, 3, size-1, size], radius=10, fill=(0, 0, 0, 95))
    # Icon Base
    draw.rounded_rectangle([0, 0, size-2, size-2], radius=10, fill=color_bg, outline=(255, 255, 255, 140), width=1)
    # Glass sheen
    draw.rounded_rectangle([1, 1, size-4, int((size-2)*0.45)], radius=8, fill=(255, 255, 255, 45))
    
    try:
        font = ImageFont.truetype('arialbd.ttf', int(size * 0.38))
    except:
        font = ImageFont.load_default()
        
    bbox = draw.textbbox((0, 0), abbr, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - 2 - tw) // 2
    ty = (size - 2 - th) // 2 - 2
    
    draw.text((tx, ty), abbr, font=font, fill=(255, 255, 255, 255))
    return img

def create_vertical_right_pillar(base_image_path, output_path):
    base_img = Image.open(base_image_path).convert('RGBA')
    W, H = base_img.size
    
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. TẦNG 1: Chữ Ký Thủy Tinh Xuyên Thấu Chính Giữa (WaterTreatment3D)
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
    
    # Bevel 3D Light
    draw.text((c_pos_x + 1.4, c_pos_y + 1.4), center_title, font=center_font, fill=(0, 0, 0, 0), stroke_width=2, stroke_fill=(0, 0, 0, 85))
    draw.text((c_pos_x - 1.2, c_pos_y - 1.2), center_title, font=center_font, fill=(0, 0, 0, 0), stroke_width=2, stroke_fill=(255, 255, 255, 150))
    
    # 2. TẦNG 2: Thẻ Tác Giả Ribbon (tanphan1105)
    author_tag = "tanphan1105"
    author_font_size = int(H * 0.038)
    try:
        author_font = ImageFont.truetype('arialbd.ttf', author_font_size)
    except:
        author_font = ImageFont.load_default()
        
    a_bbox = draw.textbbox((0, 0), author_tag, font=author_font)
    atw = a_bbox[2] - a_bbox[0]
    ath = a_bbox[3] - a_bbox[1]
    
    pad_x = int(W * 0.035)
    pad_y = int(H * 0.011)
    badge_w = atw + pad_x * 2
    badge_h = ath + pad_y * 2
    
    margin_x = int(W * 0.035) # 90px
    margin_y = int(H * 0.045) # 65px
    
    badge_x = W - badge_w - margin_x
    badge_y = H - badge_h - margin_y
    
    # Draw Green Ribbon Card
    draw.rounded_rectangle([badge_x + 3, badge_y + 3, badge_x + badge_w + 3, badge_y + badge_h + 3], radius=12, fill=(0, 0, 0, 90))
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(24, 150, 68, 240), outline=(255, 255, 255, 200), width=2)
    draw.text((badge_x + (badge_w - atw)//2, badge_y + (badge_h - ath)//2 - 2), author_tag, font=author_font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 200))
    
    # 3. CỘT DỌC COMPATIBILITY BÊN PHẢI (SLIM VERTICAL PILLAR)
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
        ("3D", "3ds Max", (30, 155, 170))
    ]
    
    # Độ rộng khung dọc vừa khít thẻ tác giả
    pillar_w = badge_w # Bằng chính xác chiều rộng của Thẻ tanphan1105 (~310px)
    pillar_x = badge_x
    pillar_y_top = int(H * 0.06) # Cách đỉnh 86px
    pillar_h = (badge_y - int(H * 0.025)) - pillar_y_top # ~1120px
    
    # Khung Thủy Tinh Khói Mờ (Frosted Dark Glass)
    p_box = [pillar_x, pillar_y_top, pillar_x + pillar_w, pillar_y_top + pillar_h]
    draw.rounded_rectangle([p_box[0]+4, p_box[1]+6, p_box[2]+4, p_box[3]+6], radius=16, fill=(0, 0, 0, 95))
    draw.rounded_rectangle(p_box, radius=16, fill=(12, 16, 24, 230), outline=(255, 255, 255, 60), width=1)
    
    # Header Cột
    try:
        head_font = ImageFont.truetype('arialbd.ttf', int(H * 0.015))
        sub_font = ImageFont.truetype('arialbd.ttf', int(H * 0.0115))
        item_font = ImageFont.truetype('arialbd.ttf', int(H * 0.0125))
    except:
        head_font = sub_font = item_font = ImageFont.load_default()
        
    h_text = "COMPATIBILITY"
    h_bb = draw.textbbox((0, 0), h_text, font=head_font)
    draw.text((pillar_x + (pillar_w - (h_bb[2]-h_bb[0]))//2, pillar_y_top + 16), h_text, font=head_font, fill=(255, 255, 255, 255))
    
    s_text = "100% CAD TESTED"
    s_bb = draw.textbbox((0, 0), s_text, font=sub_font)
    draw.text((pillar_x + (pillar_w - (s_bb[2]-s_bb[0]))//2, pillar_y_top + 42), s_text, font=sub_font, fill=(52, 199, 89, 255))
    
    draw.line([(pillar_x + 18, pillar_y_top + 66), (pillar_x + pillar_w - 18, pillar_y_top + 66)], fill=(255, 255, 255, 40), width=1)
    
    # Danh sách 2 Cột x 5 Hàng (Bố trí đều hoàn hảo bên trong khung)
    grid_top = pillar_y_top + 80
    grid_h = pillar_h - 100
    row_step = grid_h / 5
    badge_size = int(row_step * 0.65) # ~64px
    
    col_gap = int(pillar_w * 0.16)
    left_x = pillar_x + int((pillar_w - (badge_size * 2 + col_gap)) / 2)
    right_x = left_x + badge_size + col_gap
    
    for idx, (abbr, name, col) in enumerate(softwares):
        row_i = idx // 2
        col_i = idx % 2
        
        bx = left_x if col_i == 0 else right_x
        by = int(grid_top + (row_i * row_step))
        
        # Draw Icon Badge
        badge_img = create_tech_badge(abbr, col, size=badge_size)
        overlay.paste(badge_img, (bx, by), badge_img)
        
        # Label tên ngắn bên dưới
        l_bb = draw.textbbox((0, 0), abbr, font=item_font)
        lw = l_bb[2] - l_bb[0]
        draw.text((bx + (badge_size - lw)//2, by + badge_size + 4), abbr, font=item_font, fill=(210, 225, 245, 230))
        
    final_img = Image.alpha_composite(base_img, overlay)
    final_img.save(output_path, "PNG")
    print(f"Pillar Generated: {output_path}")

if __name__ == "__main__":
    src = r"D:\WT3D_Project\Z_Tools\Demo_Watermark_3D_Bevel_Edge_2K.png"
    out = r"D:\WT3D_Project\Z_Tools\Demo_Vertical_Right_Pillar_2K.png"
    create_vertical_right_pillar(src, out)
