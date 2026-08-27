from PIL import Image, ImageChops
import os

def apply_watermark(base_image_path, watermark_path, output_path):
    try:
        base = Image.open(base_image_path).convert('RGB')
        watermark = Image.open(watermark_path).convert('RGB')

        # Resize watermark (e.g. to 35% of base image width for a prominent logo)
        scale_factor = 0.35
        new_width = int(base.width * scale_factor)
        new_height = int(watermark.height * (new_width / watermark.width))
        watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create a black image the same size as the base image
        watermark_layer = Image.new('RGB', base.size, (0, 0, 0))

        # Calculate center position
        x = (base.width - new_width) // 2
        y = (base.height - new_height) // 2

        # Paste the resized watermark onto the black layer
        watermark_layer.paste(watermark, (x, y))

        # Blend using Screen mode to drop the black background
        # Screen formula: f(a,b) = 1 - (1-a)*(1-b)
        result = ImageChops.screen(base, watermark_layer)

        # Save result
        result.save(output_path, quality=95)
        print(f"Success! Saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    base_img = r"d:\WT3D_Project\Preview_Image\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology_19_Realistic_CloseUp.jpg"
    watermark_img = r"C:\Users\ADMIN\.gemini\antigravity\brain\8e14c44c-5afb-490d-a0ee-996a9613d1d3\media__1777357688449.png"
    out_img = r"d:\WT3D_Project\Preview_Image\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology\Test_Watermark_Result_Silver.jpg"
    
    apply_watermark(base_img, watermark_img, out_img)
