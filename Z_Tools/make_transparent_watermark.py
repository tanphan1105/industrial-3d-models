import os
from PIL import Image, ImageFilter

def create_transparent_watermark(input_path, output_path, opacity_percent=25):
    """
    Bóc tách nền đen và tạo Watermark trong suốt giữ nguyên độ sắc nét kim loại.
    """
    print(f"Đang xử lý ảnh: {input_path}")
    
    # Mở ảnh gốc
    logo = Image.open(input_path).convert('RGBA')
    
    # Chuyển sang ảnh xám để tính toán độ chói (Luminosity)
    gray = logo.convert('L')
    
    # Tính toán giá trị Alpha tối đa dựa trên phần trăm Opacity sếp muốn (Ví dụ 25% của 255 = 64)
    max_alpha = int(255 * (opacity_percent / 100.0))
    
    # Tạo Mask (Mặt nạ trong suốt): 
    # Những vùng tối (nền đen) có giá trị màu < 20 sẽ bị đục thủng (Alpha = 0).
    # Những chi tiết kim loại có giá trị > 20 sẽ được gán độ mờ tương ứng max_alpha.
    mask = gray.point(lambda p: max_alpha if p > 20 else 0)
    
    # Khử răng cưa (Anti-aliasing) bằng cách làm mờ nhẹ viền mask
    mask = mask.filter(ImageFilter.GaussianBlur(radius=0.8))
    
    # Gắn mặt nạ Alpha vào ảnh Gốc (Giữ nguyên 100% màu sắc và độ tương phản của kim loại)
    logo.putalpha(mask)
    
    # Lưu kết quả
    logo.save(output_path)
    print(f"Đã lưu Watermark thành công tại: {output_path}")

if __name__ == "__main__":
    # Đường dẫn ảnh gốc sếp gửi (Nền đen)
    source_image = r"C:\Users\ADMIN\.gemini\antigravity\brain\a7bcbf78-0967-47f6-91f9-c05df97a51d7\media__1777357395527.jpg"
    
    # Đường dẫn lưu Watermark
    output_watermark = r"d:\WT3D_Project\Z_Tools\Assets\OMWATER_Master_Watermark_25.png"
    
    # Tạo thư mục nếu chưa có
    os.makedirs(os.path.dirname(output_watermark), exist_ok=True)
    
    # Chạy hàm tạo Watermark 25%
    create_transparent_watermark(source_image, output_watermark, opacity_percent=25)
