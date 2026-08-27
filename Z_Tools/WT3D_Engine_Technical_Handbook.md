# 📘 SỔ TAY KỸ THUẬT: WT3D ENGINEERING PROJECTION ENGINE (v7.0 MASTER LOCKED)

> **Tài liệu khóa thông số & chuẩn hóa quy trình xuất bản Video / Snapshot CAD 3D**  
> **Tác giả:** Phan Trọng Tấn (@tanphan1105)  
> **Dự án:** WaterTreatment3D (WT3D_Project)  
> **Script Master:** `D:\WT3D_Project\Z_Tools\WT3D_Engineering_Projection_Engine.iLogicVb`

---

## 1. MA TRẬN 6 PROFILE XUẤT BẢN CHUẨN HÓA

| Khung hình | Độ phân giải | Kích thước (W × H) | Tên Folder SubDir | Tag Tên File | Mục đích ứng dụng |
|---|---|---|---|---|---|
| **Dọc 9:16** | Full HD | 1080 × 1920 | `9_16_Portrait_1080p` | `_9x16_Portrait_1080p` | TikTok, Shorts, Reels (Render siêu nhanh ~25-35s) |
| **Dọc 9:16** | 2K QHD | 1440 × 2560 | `9_16_Portrait_2K` | `_9x16_Portrait_2K` | Mobile 2K, chất lượng sắc nét mượt mà |
| **Dọc 9:16** | 4K UHD | 2160 × 3840 | `9_16_Portrait_4K` | `_9x16_Portrait_4K` | Master 4K siêu nét cho di động cao cấp |
| **Ngang 16:9** | Full HD | 1920 × 1080 | `16_9_Landscape_1080p` | `_16x9_Landscape_1080p` | YouTube Full HD, Website B2B, Tài liệu kỹ thuật |
| **Ngang 16:9** | 2K QHD | 2560 × 1440 | `16_9_Landscape_2K` | `_16x9_Landscape_2K` | Màn hình 2K Desktop, cân bằng tốc độ / độ nét |
| **Ngang 16:9** | 4K UHD | 3840 × 2160 | `16_9_Landscape_4K` | `_16x9_Landscape_4K` | Master 4K UHD bán sàn 3D quốc tế (TurboSquid, CGTrader) |

---

## 2. TRỌN BỘ 19 SNAPSHOT 360 ĐỘ CHUẨN SÀN 3D QUỐC TẾ

### 🔹 Nhóm A: Shaded with Edges (11 ảnh - Khối thực tế & Bản vẽ Studio)
1. `01_Hero3D_Iso_TopRight`: Góc ViewCube Fit To View kinh điển (Đồng thời là Video Thumbnail `FRAME_00000`).
2. `02_Hero3D_Iso_TopLeft`: Góc Isometric chéo trước bên trái.
3. `03_Hero3D_LowAngle`: Góc ngước 3/4 dưới nhìn lên bề thế.
4. `08_Studio_Clean_Front_Shaded`: Hình chiếu đứng thực tế (Front Shaded).
5. `09_Studio_Clean_Top_Shaded`: Hình chiếu bằng thực tế (Top Shaded).
6. `10_Studio_Clean_Right_Shaded`: Hình chiếu cạnh thực tế (Right Shaded).
7. `11_Hero3D_Iso_BackRight`: Góc Isometric chéo sau lưng bên phải.
8. `12_Hero3D_Iso_BackLeft`: Góc Isometric chéo sau lưng bên trái.
9. `13_Studio_Clean_Back_Shaded`: Hình chiếu mặt sau (Back Shaded).
10. `14_Studio_Clean_Left_Shaded`: Hình chiếu mặt trái (Left Shaded).
11. `15_Studio_Clean_Bottom_Shaded`: Hình chiếu mặt đáy (Bottom Shaded).

### 🔹 Nhóm B: Wireframe Topology (3 ảnh - Khung dây nét thấy cho kỹ sư)
12. `04_Wireframe3D_Topology_CheckMate`: Khung dây 3D phối cảnh chuẩn kiểm định CheckMate.
13. `16_Wireframe_Clean_Front`: Khung dây trực giao mặt trước (Front Wireframe nét xanh).
14. `17_Wireframe_Clean_Top`: Khung dây trực giao mặt bằng (Top Wireframe nét xanh).

### 🔹 Nhóm C: Monochrome Clay Render (2 ảnh - Xám bóng phô diễn cơ khí)
15. `18_Monochrome_Clay_Hero3D`: Render đất sét xám bóng góc Isometric 3D.
16. `19_Monochrome_Clay_Front`: Render đất sét xám bóng mặt trước.

### 🔹 Nhóm Blueprint CAD Dimensions (3 ảnh dập nét & kích thước mm)
17. `05_Blueprint_Front_Elevation_Dim`: Mặt đứng + Kích thước Dài (L) × Cao (H).
18. `06_Blueprint_Top_Plan_Dim`: Mặt bằng + Kích thước Dài (L) × Rộng (W).
19. `07_Blueprint_Right_Side_Dim`: Mặt cạnh + Kích thước Rộng (W) × Cao (H).

---

## 3. CÁC THÔNG SỐ TOÁN HỌC & ĐỒ HỌA ĐÃ KHÓA CỨNG

* **Màu sắc Nét Kỹ Thuật (Deep Navy Blueprint):** `#043296` (`RGB: 4, 50, 150`).
* **Khoảng lề Fit To View (`CFG_FitPadding`):** `0.72` (72% diện tích khung nhìn, chừa 14% mỗi bên cho đường DIM).
* **Góc mở ống kính phối cảnh (`PerspectiveAngle`):** `0.52 rad` (~30 độ chuẩn mắt người, không méo hình).
* **Tốc độ khung hình (`CFG_FPS`):** `30 fps`.
* **Cấu hình FFmpeg Video:**
  - Codec: `libx264`, Pixel Format: `yuv420p`
  - Preset: `medium`, Chất lượng: `CRF 16`
  - Poster Video: Gắn luồng tĩnh `attached_pic` từ `FRAME_00000.png`.

---

## 3.1. QUY CHUẨN "BẢN QUYỀN SÀN 3D" (MARKETPLACE SAFE SYSTEM)

*Tên gọi chuẩn: "bản quyền sàn 3d". Thiết kế 2 tầng nhận diện: 100% An toàn, Không vi phạm chính sách TurboSquid / CGTrader.*

1. **Tầng 1 (Chính giữa) - Chữ ký Kính Quang Học (`WaterTreatment3D`):**
   - **Font**: `Arial Black Bold`, Cỡ chữ: `10.2%` chiều cao ảnh (`147px` với 2K).
   - **Vị trí**: Căn giữa khung hình, độ cao tâm `y = 44%`.
   - **Ruột chữ**: Rỗng hoàn toàn `Alpha = 0`, nhìn xuyên thấu 100% kết cấu cơ khí.
   - **Đổ bóng 3D cạnh vát**: Cạnh bắt sáng trên-trái (`-1.2px`, White `Alpha 150/255`), Cạnh bóng râm dưới-phải (`+1.4px`, Black `Alpha 85/255`).

2. **Tầng 2 (Góc dưới phải) - Thẻ Tác Giả Ribbon (`tanphan1105`):**
   - **Nội dung**: `tanphan1105` (Chữ thường, không có ký tự `@`).
   - **Font**: `Arial Bold`, Cỡ chữ: `3.8%` chiều cao ảnh (`55px` với 2K), màu trắng tinh khiết.
   - **Viền chữ (Stroke)**: Đen siêu mảnh `1.0px` (`Alpha 200/255`).
   - **Khung thẻ xanh Emerald (`#189644`)**: Bo góc `12px`, viền trắng `2px`, đổ bóng nhẹ `3D`. Chiều dài đệm lề `pad_x = 3.5%` chiều rộng ảnh.
   - **Vị trí**: Cách lề góc dưới phải `margin_x = 3.5%`, `margin_y = 4.5%`.

---

## 4. KIẾN TRÚC TỐI ƯU HIỆU NĂNG & AN TOÀN BỘ NHỚ

1. **Quản lý tài nguyên GDI+:** Toàn bộ `Pen`, `SolidBrush`, `Font`, `Graphics` đều được bọc trong cấu trúc `Using...End Using` tự động hủy để triệt tiêu 100% hiện tượng rò rỉ GDI handle.
2. **Triệt tiêu lỗi File Lock:** 
   - Đọc ảnh qua mảng nhị phân `File.ReadAllBytes` và luồng `MemoryStream`.
   - Nhân bản sang `Bitmap(w, h, Format32bppArgb)` độc lập trong RAM để tương thích tuyệt đối với `LockBits` và `Graphics.FromImage`.
   - Ghi đè file đĩa dứt khoát bằng `File.WriteAllBytes`, loại bỏ hoàn toàn các file rác `.tmp.png`.
3. **Thu gom rác (`GC.Collect`):** Gom từ 16 lần phân tán xuống còn **3 lần duy nhất** (1 lần trước mỗi nhóm A, B, C) giúp tiết kiệm ~10-14 giây khi render 4K.
4. **Vùng quét Pixel Bounding Box:** Giới hạn vùng quét 90% × 90% (loại bỏ 5% viền ngoài), giảm 19% số phép tính ma trận điểm ảnh.
5. **Animation Loop mượt mà:** Mỗi frame chỉ gọi duy nhất 1 lần `DoEvents()` ở đầu vòng lặp để bắt phím `Escape`.

---

## 5. QUY TẮC PHÂN CẤP THƯ MỤC THÔNG MINH

* **Dự án chuẩn (nằm trong `01_PROJECTS`):** Tự động nhận diện thư mục cha chứa các cụm `01_Assemblies`, `02_Parts`, `03_Drawings_2D` để xuất vào `06_Renders_and_Media` cấp dự án.
* **Linh kiện độc lập (nằm trong `05_STANDARD_COMPONENTS`):** Xuất trực tiếp vào `05_STANDARD_COMPONENTS\06_Renders_and_Media\` để gom dữ liệu linh kiện mua sẵn gọn gàng.
