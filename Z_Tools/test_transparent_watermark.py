from PIL import Image
import os

def apply_transparent_watermark(base_image_path, watermark_path, output_path):
    try:
        base = Image.open(base_image_path).convert('RGBA')
        watermark = Image.open(watermark_path).convert('RGBA')

        # Resize watermark (e.g. to 35% of base image width)
        scale_factor = 0.35
        new_width = int(base.width * scale_factor)
        new_height = int(watermark.height * (new_width / watermark.width))
        watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Calculate center position
        x = (base.width - new_width) // 2
        y = (base.height - new_height) // 2

        # Create a transparent layer the size of the base image
        transparent_layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
        transparent_layer.paste(watermark, (x, y), watermark)

        # Alpha composite the watermark over the base image
        result = Image.alpha_composite(base, transparent_layer)
        
        # Convert back to RGB to save as JPG
        result = result.convert('RGB')
        result.save(output_path, quality=95)
        print(f"Success! Saved faint watermark preview to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    base_img = r"d:\WT3D_Project\Preview_Image\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology_19_Realistic_CloseUp.jpg"
    watermark_img = r"d:\WT3D_Project\Z_Tools\Assets\OMWATER_Master_Watermark_25.png"
    out_img = r"d:\WT3D_Project\Preview_Image\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology\Test_Watermark_Result_OMWATER25.jpg"
    
    apply_transparent_watermark(base_img, watermark_img, out_img)
