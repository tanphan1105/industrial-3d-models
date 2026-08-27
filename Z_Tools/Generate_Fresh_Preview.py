from PIL import Image, ImageDraw, ImageFont
import os, math

w, h = 1080, 1920
img = Image.new('RGB', (w, h), color=(18, 26, 36))
draw = ImageDraw.Draw(img)

# 1. Subtle 3D Grid Lines
for x in range(0, w, 120):
    draw.line([(x, 0), (x, h)], fill=(30, 44, 58), width=2)
for y in range(0, h, 120):
    draw.line([(0, y), (w, y)], fill=(30, 44, 58), width=2)

# 2. Vietnam Flag at Top Left
flag_w, flag_h = 120, 80
flag_x, flag_y = 50, 50
draw.rectangle([flag_x, flag_y, flag_x + flag_w, flag_y + flag_h], fill=(218, 37, 29), outline=(255, 255, 255), width=3)

# Yellow Star
cx, cy = flag_x + flag_w // 2, flag_y + flag_h // 2
r_out, r_in = 24, 9
pts = []
for i in range(10):
    ang = (i * 36 - 90) * math.pi / 180.0
    r = r_out if i % 2 == 0 else r_in
    pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
draw.polygon(pts, fill=(255, 255, 0))

# 3. Load Fonts
try:
    font_center = ImageFont.truetype("arialbd.ttf", 75)
    font_brand = ImageFont.truetype("arial.ttf", 36)
    font_contact = ImageFont.truetype("arialbd.ttf", 46)
except:
    font_center = ImageFont.load_default()
    font_brand = ImageFont.load_default()
    font_contact = ImageFont.load_default()

# 4. Center Glass Emboss @tanphan1105
text_center = "@tanphan1105"
bbox_c = draw.textbbox((0, 0), text_center, font=font_center)
cw = bbox_c[2] - bbox_c[0]
ch = bbox_c[3] - bbox_c[1]
center_x = (w - cw) // 2
center_y = int(h * 0.44)

# Glass shadow and light
draw.text((center_x + 4, center_y + 4), text_center, fill=(0, 0, 0, 180), font=font_center)
draw.text((center_x, center_y), text_center, fill=(255, 255, 255), font=font_center)

# 5. Green Card Badge at Bottom
brand_text = "WaterTreatment3D"
contact_text = "@tanphan1105 | Zalo: +84985267326"

bbox_b = draw.textbbox((0, 0), brand_text, font=font_brand)
bbox_ct = draw.textbbox((0, 0), contact_text, font=font_contact)

w_brand = bbox_b[2] - bbox_b[0]
h_brand = bbox_b[3] - bbox_b[1]
w_contact = bbox_ct[2] - bbox_ct[0]
h_contact = bbox_ct[3] - bbox_ct[1]

max_txt_w = max(w_brand, w_contact)
qr_w = 150
pad = 30

card_w = max_txt_w + 30 + qr_w + pad * 2
card_h = h_brand + h_contact + 30 + pad * 2

card_x = (w - card_w) // 2
card_y = h - card_h - 100

# Draw Green Card
draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill=(52, 199, 89), outline=(255, 255, 255), width=3)

# Draw Brand Header (WaterTreatment3D)
draw.text((card_x + pad + 2, card_y + pad + 2), brand_text, fill=(30, 80, 40), font=font_brand)
draw.text((card_x + pad, card_y + pad), brand_text, fill=(255, 255, 255), font=font_brand)

# Draw Contact Line (HUGE & BOLD)
y_contact = card_y + pad + h_brand + 15
draw.text((card_x + pad + 2, y_contact + 2), contact_text, fill=(30, 80, 40), font=font_contact)
draw.text((card_x + pad, y_contact), contact_text, fill=(255, 255, 255), font=font_contact)

# Draw QR Code
qr_img_path = "D:/WT3D_Project/Z_Tools/wt3d_qr_green.png"
if os.path.exists(qr_img_path):
    qr_img = Image.open(qr_img_path).convert("RGBA").resize((qr_w, qr_w))
    qr_x = card_x + pad + max_txt_w + 25
    qr_y = card_y + (card_h - qr_w) // 2
    img.paste(qr_img, (qr_x, qr_y), qr_img)

out_path = "C:/Users/ADMIN/.gemini/antigravity/brain/43aef838-7520-4e40-bcba-b8699ab024a8/watermark_preview_watertreatment3d.png"
img.save(out_path, format="PNG")
print("Saved fresh watermark preview to:", out_path)
