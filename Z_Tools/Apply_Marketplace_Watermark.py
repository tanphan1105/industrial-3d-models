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
    TỐI ƯU HÓA ĐỘ NÉT GỐC CAD CHUẨN XÁC (ZERO-BLEED, ZERO-JAGGED, CRYSTAL-CLEAN):
    1. Giữ nguyên độ sắc nét tự nhiên 100% từ Inventor GPU Render.
    2. Khử sạch toàn bộ hiệu ứng Bloom/Blur nhân tạo gây lem màu và mờ viền.
    3. Giữ màu sắc trung thực, đậm đà, đường nét CAD phẳng mịn, sắc sảo.
    """
    # 1. SSAA Downsampling nếu ảnh chụp supersampled với bộ lọc Lanczos mịn mượt
    if target_w and target_h and (img.size[0] > target_w or img.size[1] > target_h):
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
    base_rgb = img.convert('RGB')
    
    # 2. Cân chỉnh độ tương phản nhẹ nhàng (Contrast 1.04) tôn khối mà không làm cháy trắng
    enh_contrast = ImageEnhance.Contrast(base_rgb)
    contrasted = enh_contrast.enhance(1.04)
    
    # 3. Giữ độ tươi màu tự nhiên (Color 1.06)
    enh_color = ImageEnhance.Color(contrasted)
    colored = enh_color.enhance(1.06)
    
    # 4. Tinh chỉnh độ nét vi mô trong trẻo tuyệt đối (không sinh quầng sáng, không răng cưa)
    final_rgb = colored
    
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
        
        # Ribbon Background (Green #16a34a)
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
            radius=int(badge_h * 0.45),
            fill=(22, 163, 74, 235),
            outline=(255, 255, 255, 180),
            width=max(1, int(target_h * 0.0012))
        )
        
        # Author Text
        tx = badge_x + (badge_w - atw) // 2
        ty = badge_y + (badge_h - ath) // 2 - int(target_h * 0.002)
        draw.text((tx, ty), author_tag, font=author_font, fill=(255, 255, 255, 255))
        
        # 3. Top-Right Software Icons Pillar (10 icons)
        if include_software_pillar:
            icon_names = ["SolidWorks", "Inventor", "AutoCAD", "Revit", "Fusion360", "STEP", "Blender", "3dsMax", "UnrealEngine", "Cinema4D"]
            icon_size = max(24, int(target_h * 0.052))
            gap = max(4, int(target_h * 0.010))
            
            pillar_x = target_w - (icon_size * 2 + gap + margin_x)
            pillar_y = int(target_h * 0.035)
            
            for i, name in enumerate(icon_names):
                row = i // 2
                col = i % 2
                ix = pillar_x + col * (icon_size + gap)
                iy = pillar_y + row * (icon_size + gap)
                
                icon_file = os.path.join(ICONS_DIR, f"{name}.png")
                icon_img = render_normalized_icon(icon_file, target_size=icon_size)
                overlay.paste(icon_img, (ix, iy), icon_img)
                
        # 4. Composite Overlay onto Image
        result = Image.alpha_composite(img.convert('RGBA'), overlay)
        
        # Save output
        if not output_path:
            output_path = image_path
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result.save(output_path, 'PNG')
        print(f"Successfully applied clean watermark & polish to: {output_path}")
        return True
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def process_directory(directory_path, output_directory=None, author_tag="tanphan1105", brand_title="WaterTreatment3D", include_software_pillar=True, enable_keyshot_polish=True):
    if not os.path.exists(directory_path):
        print(f"Error: Directory not found: {directory_path}")
        return False
        
    print(f"Scanning directory: {directory_path}")
    count = 0
    for root, dirs, files in os.walk(directory_path):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_file = os.path.join(root, f)
                
                if output_directory:
                    rel_p = os.path.relpath(input_file, directory_path)
                    out_file = os.path.join(output_directory, rel_p)
                else:
                    out_file = input_file
                    
                apply_marketplace_watermark(
                    input_file,
                    output_path=out_file,
                    author_tag=author_tag,
                    brand_title=brand_title,
                    include_software_pillar=include_software_pillar,
                    enable_keyshot_polish=enable_keyshot_polish
                )
                count += 1
    print(f"Finished processing {count} images.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Clean 3D Marketplace Watermark and Polish")
    parser.add_argument("input_path", help="Path to input image or directory")
    parser.add_argument("-o", "--output", help="Path to output image or directory (optional)")
    parser.add_argument("-a", "--author", default="tanphan1105", help="Author tag")
    parser.add_argument("-b", "--brand", default="WaterTreatment3D", help="Brand title watermark")
    parser.add_argument("--no-pillar", action="store_true", help="Disable software icons pillar")
    parser.add_argument("--no-polish", action="store_true", help="Disable Keyshot style polish")
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input_path):
        process_directory(
            args.input_path,
            output_directory=args.output,
            author_tag=args.author,
            brand_title=args.brand,
            include_software_pillar=not args.no_pillar,
            enable_keyshot_polish=not args.no_polish
        )
    elif os.path.isfile(args.input_path):
        apply_marketplace_watermark(
            args.input_path,
            output_path=args.output,
            author_tag=args.author,
            brand_title=args.brand,
            include_software_pillar=not args.no_pillar,
            enable_keyshot_polish=not args.no_polish
        )
    else:
        print(f"Error: Invalid path: {args.input_path}")
