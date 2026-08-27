import os
import sys
from PIL import Image, ImageDraw, ImageFont

def render_large_floating_icon(icon_path, target_size=105):
    """Xử lý icon hãng to nổi khối 3D trực tiếp, không cần đóng khung hộp, để lộ hoàn toàn nền"""
    img = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
    if os.path.exists(icon_path):
        try:
            ico = Image.open(icon_path).convert('RGBA')
            ico.thumbnail((target_size - 8, target_size - 8), Image.Resampling.LANCZOS)
            
            # Tạo bóng đổ 3D mềm mại cho chính thân icon (Drop Shadow)
            shadow = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
            s_alpha = ico.split()[-1]
            s_color = Image.new('L', ico.size, 0)
            shadow_mask = Image.merge('RGBA', (s_color, s_color, s_color, s_alpha))
            
            # Paste bóng lệch nhẹ (3px, 4px)
            img.paste(shadow_mask, ((target_size - ico.width)//2 + 2, (target_size - ico.height)//2 + 4), shadow_mask)
            # Paste icon chính hãng sắc nét lên trên
            img.paste(ico, ((target_size - ico.width)//2, (target_size - ico.height)//2), ico)
        except Exception as e:
            print(f"Error {icon_path}: {e}")
    return img

def create_clean_floating_icons(base_image_path, output_path):
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
    
    # Vẽ Thẻ xanh Ribbon
    draw.rounded_rectangle([badge_x + 3, badge_y + 3, badge_x + badge_w + 3, badge_y + badge_h + 3], radius=12, fill=(0, 0, 0, 90))
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(24, 150, 68, 240), outline=(255, 255, 255, 200), width=2)
    draw.text((badge_x + (badge_w - atw)//2, badge_y + (badge_h - ath)//2 - 2), author_tag, font=author_font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 200))
    
    # 3. ICON CHÍNH HÃNG TO BÓNG BẨY THẲNG TRÊN NỀN ẢNH (KHÔNG HỘP ĐEN)
    icons_dir = r"D:\WT3D_Project\Z_Tools\Assets\Icons"
    official_softwares = [
        os.path.join(icons_dir, "solidworks.png"),
        os.path.join(icons_dir, "inventor.png"),
        os.path.join(icons_dir, "autocad.png"),
        os.path.join(icons_dir, "revit.png"),
        os.path.join(icons_dir, "fusion.png"),
        os.path.join(icons_dir, "catia.png"),
        os.path.join(icons_dir, "blender.png"),
        os.path.join(icons_dir, "3dsmax.png"),
        os.path.join(icons_dir, "unreal.png"),
        os.path.join(icons_dir, "freecad.png")
    ]
    
    # Bố trí 2 Cột x 5 Hàng, icon siêu to (88px) đặt trôi nổi thanh thoát
    pillar_w = badge_w # Căn thẳng hàng với thẻ tanphan1105
    pillar_x = badge_x
    start_y = int(H * 0.08) # Cách đỉnh 115px
    total_grid_h = (badge_y - int(H * 0.04)) - start_y # ~1060px
    row_step = total_grid_h / 5
    icon_size = int(row_step * 0.72) # ~110px siêu to rõ
    
    col_gap = int(pillar_w * 0.12)
    left_x = pillar_x + int((pillar_w - (icon_size * 2 + col_gap)) / 2)
    right_x = left_x + icon_size + col_gap
    
    for idx, icon_file in enumerate(official_softwares):
        row_i = idx // 2
        col_i = idx % 2
        
        ix = left_x if col_i == 0 else right_x
        iy = int(start_y + (row_i * row_step))
        
        # Render icon to nổi bóng
        ico_img = render_large_floating_icon(icon_file, target_size=icon_size)
        overlay.paste(ico_img, (ix, iy), ico_img)
        
    final_img = Image.alpha_composite(base_img, overlay)
    final_img.save(output_path, "PNG")
    print(f"Clean Floating Icons Generated: {output_path}")

if __name__ == "__main__":
    src = r"D:\WT3D_Project\Z_Tools\Demo_Watermark_3D_Bevel_Edge_2K.png"
    out = r"D:\WT3D_Project\Z_Tools\Demo_Clean_Floating_Icons_2K.png"
    create_clean_floating_icons(src, out)
