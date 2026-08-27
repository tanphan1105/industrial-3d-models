from PIL import Image, ImageDraw, ImageFont
import os

icons_dir = r"D:\WT3D_Project\Z_Tools\Assets\Icons"

# 1. Vẽ Icon Khối Lập Phương Đỏ 3D SolidWorks chuẩn gốc (Cube Red 3D Logo)
sw_cube = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
d = ImageDraw.Draw(sw_cube)
# Mặt Top
d.polygon([(128, 20), (228, 75), (128, 130), (28, 75)], fill=(245, 65, 75), outline=(255, 255, 255, 120))
# Mặt Phải
d.polygon([(128, 130), (228, 75), (228, 190), (128, 245)], fill=(185, 20, 30), outline=(255, 255, 255, 80))
# Mặt Trái
d.polygon([(28, 75), (128, 130), (128, 245), (28, 190)], fill=(220, 35, 45), outline=(255, 255, 255, 80))
# Chữ DS / S trên khối
f_sw = ImageFont.truetype('ariblk.ttf', 72)
d.text((56, 115), "S", font=f_sw, fill=(255, 255, 255, 230))
d.text((146, 115), "W", font=f_sw, fill=(255, 255, 255, 230))
sw_cube.save(os.path.join(icons_dir, "solidworks_cube_official.png"))

# 2. Vẽ Icon La Bàn / Cánh Buồm 3D CATIA chuẩn Dassault Systèmes
catia_cube = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
d_c = ImageDraw.Draw(catia_cube)
# Vòng la bàn xanh Dassault
d_c.rounded_rectangle([10, 10, 246, 246], radius=50, fill=(10, 85, 165), outline=(255, 255, 255, 140), width=3)
f_c = ImageFont.truetype('ariblk.ttf', 110)
d_c.text((36, 60), "3D", font=f_c, fill=(255, 255, 255, 250))
f_c_sub = ImageFont.truetype('arialbd.ttf', 36)
d_c.text((54, 180), "CATIA", font=f_c_sub, fill=(255, 255, 255, 230))
catia_cube.save(os.path.join(icons_dir, "catia_cube_official.png"))

print("Official Brand Symbols Rendered Successfully!")
