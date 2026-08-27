import os
import shutil
from PIL import Image, ImageDraw, ImageFont

src_path = r'D:\INVENTOR_DATA\05_STANDARD_COMPONENTS\06_Renders_and_Media\02_Images_4K_Previews\16_9_Landscape_1080p\den alarm_01_Hero3D_Iso_TopRight_16x9_Landscape_1080p.png'
img = Image.open(src_path).convert('RGBA')
target_w, target_h = 2560, 1440
img_2k = img.resize((target_w, target_h), Image.LANCZOS)

# 1. Overlay Layer - Center Crystal Bevel
overlay = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

text = 'WaterTreatment3D'
font_size = int(target_h * 0.102)
font = ImageFont.truetype('ariblk.ttf', font_size)

bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]

pos_x = (target_w - tw) // 2
pos_y = int(target_h * 0.44) - (th // 2)

# Shadow & Highlight edge
draw.text((pos_x + 1.4, pos_y + 1.4), text, font=font, fill=(0, 0, 0, 0), stroke_width=2, stroke_fill=(0, 0, 0, 85))
draw.text((pos_x - 1.2, pos_y - 1.2), text, font=font, fill=(0, 0, 0, 0), stroke_width=2, stroke_fill=(255, 255, 255, 150))

# 2. BOTTOM-RIGHT BADGE: tanphan1105 - VIỀN ĐEN SIÊU MẢNH TINH TẾ (STROKE = 1PX)
author_text = 'tanphan1105'
author_font_size = int(target_h * 0.038)
author_font = ImageFont.truetype('arialbd.ttf', author_font_size)

a_bbox = draw.textbbox((0, 0), author_text, font=author_font)
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

# Bóng mờ dưới thẻ
shadow_box = [badge_x + 3, badge_y + 3, badge_x + badge_w + 3, badge_y + badge_h + 3]
draw.rounded_rectangle(shadow_box, radius=12, fill=(0, 0, 0, 90))

# Khung thẻ xanh Emerald
green_box = [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h]
draw.rounded_rectangle(green_box, radius=12, fill=(24, 150, 68, 240), outline=(255, 255, 255, 200), width=2)

# Chữ trắng căn giữa thẻ + Viền đen siêu thanh mảnh (Stroke 1px dứt khoát)
text_x = badge_x + (badge_w - atw) // 2
text_y = badge_y + (badge_h - ath) // 2 - 2

draw.text((text_x, text_y), author_text, font=author_font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 200))

final_img = Image.alpha_composite(img_2k, overlay)

out_demo = r'D:\WT3D_Project\Z_Tools\Demo_Watermark_Thin_Stroke_2K.png'
final_img.save(out_demo)

dst = r'C:\Users\PHAN TRONG TAN\.gemini\antigravity\brain\0ae66afd-c144-4254-9d6b-7633e3f0365d\demo_thin_stroke.png'
shutil.copy(out_demo, dst)
print('Thin stroke demo created successfully!')
