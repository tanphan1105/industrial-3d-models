import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ICONS_DIR = r"D:\WT3D_Project\Z_Tools\Assets\Icons"

def render_normalized_icon(icon_path, target_size=115):
    """Render icon chuẩn hóa đồng nhất 100% tỷ lệ và kích thước với bóng đổ 3D"""
    img = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
    if os.path.exists(icon_path):
        try:
            ico = Image.open(icon_path).convert('RGBA')
            ico = ico.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            # Shadow 3D
            shadow = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
            s_alpha = ico.split()[-1].point(lambda p: int(p * 0.40))
            s_color = Image.new('L', ico.size, 0)
            shadow_mask = Image.merge('RGBA', (s_color, s_color, s_color, s_alpha))
            
            img.paste(shadow_mask, (2, 3), shadow_mask)
            img.paste(ico, (0, 0), ico)
        except Exception:
            pass
    return img

def apply_keyshot_edge_and_aa_polish(img, target_w=None, target_h=None):
    """
    TỐI ƯU HÓA PHONG CÁCH TWO LIGHTS + ALL SHADOWS + ÁNH SÁNG VIỀN NỔI BẬT:
    1. Super-Sampling Anti-Aliasing (SSAA): Khử răng cưa mịn màng bằng bộ lọc Lanczos-3
    2. Màu sắc đậm đà tự nhiên từ Two Lights + All Shadows (Ambient Occlusion & Ground Shadows)
    3. Tăng nhẹ ánh sáng viền (Specular Rim Highlight Sheen 10%) bám theo mép cong Inox/kim loại
    4. Micro-Clarity làm sắc nét chi tiết máy mà không gây chói lóa
    """
    # 1. SSAA Downsampling nếu ảnh chụp supersampled
    if target_w and target_h and (img.size[0] > target_w or img.size[1] > target_h):
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
    base_rgb = img.convert('RGB')
    
    # 2. Khử mờ vi mô làm nét chi tiết máy (Clarity)
    clarity = base_rgb.filter(ImageFilter.UnsharpMask(radius=1.6, percent=125, threshold=2))
    
    # 3. Tương phản cân bằng hoàn hảo cho Two Lights (Contrast 1.10)
    enh_contrast = ImageEnhance.Contrast(clarity)
    contrasted = enh_contrast.enhance(1.10)
    
    # 4. No màu công nghiệp tự nhiên (Color 1.15)
    enh_color = ImageEnhance.Color(contrasted)
    colored = enh_color.enhance(1.15)
    
    # 5. Tăng xíu ánh sáng viền bạc bám mép chi tiết (Luminance > 230)
    gray = colored.convert('L')
    rim_mask = gray.point(lambda p: 255 if p > 230 else (int((p - 180) * 4.4) if p > 180 else 0))
    
    bloom_radius = max(2, int(img.height * 0.0022))
    rim_glow = rim_mask.filter(ImageFilter.GaussianBlur(radius=bloom_radius))
    
    # Ánh sáng viền bạc Studio tinh tế (248, 250, 255)
    soft_silver_rim = Image.new('RGB', img.size, (248, 250, 255))
    rim_layer = Image.composite(soft_silver_rim, colored, rim_glow)
    
    # Hòa trộn 10% tạo viền sáng rõ nét trên nền shadow đậm đà
    enhanced = Image.blend(colored, rim_layer, 0.10)
    
    # 6. Độ sắc nét hoàn thiện
    enh_sharp = ImageEnhance.Sharpness(enhanced)
    final_rgb = enh_sharp.enhance(1.12)
    
    if img.mode == 'RGBA':
        final_rgb = final_rgb.convert('RGBA')
        final_rgb.putalpha(img.split()[-1])
    return final_rgb

def apply_marketplace_watermark(image_path, output_path=None, author_tag="tanphan1105", brand_title="WaterTreatment3D", include_software_pillar=True, enable_keyshot_polish=True, target_w=None, target_h=None):
    """
    Dập 'Bản Quyền Sàn 3D' kết hợp Khử Răng Cưa SSAA & Two Lights Studio Polish
    """
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        return False
        
    try:
        raw_img = Image.open(image_path).convert('RGBA')
        
        filename_lower = os.path.basename(image_path).lower()
        is_blueprint = "blueprint" in filename_lower or "_dim_" in filename_lower
        
        if enable_keyshot_polish and not is_blueprint:
            img = apply_keyshot_edge_and_aa_polish(raw_img, target_w=target_w, target_h=target_h)
        else:
            if target_w and target_h and (raw_img.size[0] > target_w or raw_img.size[1] > target_h):
                img = raw_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            else:
                img = raw_img
            
        target_w, target_h = img.size
        
        # 1. Overlay Layer
        overlay = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Font sizing scale based on image height
        center_font_size = int(target_h * 0.102)
        try:
            center_font = ImageFont.truetype('ariblk.ttf', center_font_size)
        except Exception:
            center_font = ImageFont.truetype('arialbd.ttf', center_font_size)
            
        bbox = draw.textbbox((0, 0), brand_title, font=center_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        pos_x = (target_w - tw) // 2
        pos_y = int(target_h * 0.44) - (th // 2)
        
        # Directional 3D Bevel Edge (Top-Left Light / Bottom-Right Shadow)
        shadow_offset = max(1.0, target_h * 0.001)
        light_offset = max(0.9, target_h * 0.0008)
        stroke_w = max(1, int(target_h * 0.0014))
        
        # Shadow Edge (Khuất sáng dưới-phải: Black Alpha 85)
        draw.text((pos_x + shadow_offset, pos_y + shadow_offset), brand_title, font=center_font, fill=(0, 0, 0, 0), stroke_width=stroke_w, stroke_fill=(0, 0, 0, 85))
        # Highlight Edge (Đón sáng trên-trái: White Alpha 150)
        draw.text((pos_x - light_offset, pos_y - light_offset), brand_title, font=center_font, fill=(0, 0, 0, 0), stroke_width=stroke_w, stroke_fill=(255, 255, 255, 150))
        
        # 2. Bottom-Right Badge: tanphan1105
        author_font_size = int(target_h * 0.038)
        try:
            author_font = ImageFont.truetype('arialbd.ttf', author_font_size)
        except Exception:
            author_font = ImageFont.load_default()
            
        a_bbox = draw.textbbox((0, 0), author_tag, font=author_font)
        atw = a_bbox[2] - a_bbox[0]
        ath = a_bbox[3] - a_bbox[1]
        
        pad_x = int(target_w * 0.035)
        pad_y = int(target_h * 0.011)
        
        badge_w = atw + pad_x * 2
        badge_h = ath + pad_y * 2
        
        margin_x = int(target_w * 0.035)
        margin_y = int(target_h * 0.045)
        
        badge_x = target_w - badge_w - margin_x
        badge_y = target_h - badge_h - margin_y
        
        # Card Shadow
        shadow_box = [badge_x + 3, badge_y + 3, badge_x + badge_w + 3, badge_y + badge_h + 3]
        draw.rounded_rectangle(shadow_box, radius=12, fill=(0, 0, 0, 90))
        
        # Emerald Green Ribbon Card (#189644)
        green_box = [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h]
        draw.rounded_rectangle(green_box, radius=12, fill=(24, 150, 68, 240), outline=(255, 255, 255, 200), width=2)
        
        # Author Text White with Razor Sharp Black Outline (Stroke 1.0px)
        text_x = badge_x + (badge_w - atw) // 2
        text_y = badge_y + (badge_h - ath) // 2 - 2
        
        draw.text((text_x, text_y), author_tag, font=author_font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 200))
        
        # 3. Software Compatibility Pillar (10 Official CAD & DCC Logos)
        if include_software_pillar and not is_blueprint:
            norm_logos = [
                os.path.join(ICONS_DIR, "sw_norm.png"),
                os.path.join(ICONS_DIR, "inv_norm.png"),
                os.path.join(ICONS_DIR, "acad_norm.png"),
                os.path.join(ICONS_DIR, "revit_norm.png"),
                os.path.join(ICONS_DIR, "fusion_norm.png"),
                os.path.join(ICONS_DIR, "catia_norm.png"),
                os.path.join(ICONS_DIR, "blender_norm.png"),
                os.path.join(ICONS_DIR, "3dsmax_norm.png"),
                os.path.join(ICONS_DIR, "unreal_norm.png"),
                os.path.join(ICONS_DIR, "freecad_norm.png")
            ]
            
            pillar_w = badge_w
            pillar_x = badge_x
            start_y = int(target_h * 0.065)
            total_grid_h = (badge_y - int(target_h * 0.035)) - start_y
            row_step = total_grid_h / 5
            icon_display_size = int(row_step * 0.76)
            
            col_gap = int(pillar_w * 0.16)
            left_x = pillar_x + int((pillar_w - (icon_display_size * 2 + col_gap)) / 2)
            right_x = left_x + icon_display_size + col_gap
            
            for idx, icon_file in enumerate(norm_logos):
                row_i = idx // 2
                col_i = idx % 2
                
                ix = left_x if col_i == 0 else right_x
                iy = int(start_y + (row_i * row_step))
                
                ico_img = render_normalized_icon(icon_file, target_size=icon_display_size)
                overlay.paste(ico_img, (ix, iy), ico_img)
        
        # Merge Layer
        final_img = Image.alpha_composite(img, overlay)
        
        if output_path is None:
            output_path = image_path
            
        final_img.save(output_path, "PNG")
        mode_str = "with 10 Icons + Two Lights Polish" if (include_software_pillar and not is_blueprint) else "Standard Clean"
        print(f"  [OK] Applied Marketplace Safe Watermark ({mode_str}): {output_path}")
        return True
    except Exception as e:
        print(f"  [ERROR] Watermark failed on {image_path}: {e}")
        return False

def batch_process_directory(directory_path, recursive=True, include_pillar=True, enable_keyshot=True, target_w=None, target_h=None):
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return
        
    exts = ('.png', '.jpg', '.jpeg')
    count = 0
    
    if recursive:
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith(exts) and not file.startswith('Demo_'):
                    full_path = os.path.join(root, file)
                    if apply_marketplace_watermark(full_path, include_software_pillar=include_pillar, enable_keyshot_polish=enable_keyshot, target_w=target_w, target_h=target_h):
                        count += 1
    else:
        for file in os.listdir(directory_path):
            if file.lower().endswith(exts) and not file.startswith('Demo_'):
                full_path = os.path.join(directory_path, file)
                if apply_marketplace_watermark(full_path, include_software_pillar=include_pillar, enable_keyshot_polish=enable_keyshot, target_w=target_w, target_h=target_h):
                    count += 1
    print(f"Batch completed: Processed {count} images.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Locked Marketplace Safe Watermark with Two Lights Polish.")
    parser.add_argument("input", help="Image file path or directory path.")
    parser.add_argument("-o", "--output", help="Output file path (optional).")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process directory recursively.")
    parser.add_argument("-a", "--author", default="tanphan1105", help="Author handle (default: tanphan1105).")
    parser.add_argument("-b", "--brand", default="WaterTreatment3D", help="Brand title (default: WaterTreatment3D).")
    parser.add_argument("-p", "--pillar", dest="pillar", action="store_true", default=True, help="Include 10 Official CAD Icons Pillar (default: True).")
    parser.add_argument("--no-pillar", dest="pillar", action="store_false", help="Disable 10 Official CAD Icons Pillar.")
    parser.add_argument("--keyshot", dest="keyshot", action="store_true", default=True, help="Enable Two Lights Polish (default: True).")
    parser.add_argument("--no-keyshot", dest="keyshot", action="store_false", help="Disable KeyShot Polish.")
    parser.add_argument("--target-w", dest="target_w", type=int, default=None, help="Target SSAA downsampling width.")
    parser.add_argument("--target-h", dest="target_h", type=int, default=None, help="Target SSAA downsampling height.")
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        batch_process_directory(args.input, recursive=args.recursive, include_pillar=args.pillar, enable_keyshot=args.keyshot, target_w=args.target_w, target_h=args.target_h)
    elif os.path.isfile(args.input):
        apply_marketplace_watermark(args.input, args.output, author_tag=args.author, brand_title=args.brand, include_software_pillar=args.pillar, enable_keyshot_polish=args.keyshot, target_w=args.target_w, target_h=args.target_h)
    else:
        print(f"Invalid path: {args.input}")
