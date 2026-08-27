# ==============================================================================
# BẢNG TIÊU CHUẨN VÀNG & CHECKLIST ĐỐI CHIẾU THÔNG SỐ WT3D MASTER v7.0
# WT3D ENGINEERING PROJECTION & MARKETPLACE PUBLISHING ENGINE (LOCKED 100%)
# ==============================================================================
# Ngày khóa chuẩn: 17/08/2026
# Tệp tài liệu tra cứu, kiểm tra chất lượng và hoàn nguyên sự cố chính thức của dự án.
# Lưu tại: D:\WT3D_Project\Z_Tools\WT3D_Master_Quality_Checklist_Benchmark.md
# ==============================================================================

## PHẦN 1: BẢNG THÔNG SỐ VÀNG ĐÃ KHÓA CỨNG (GOLDEN MASTER BENCHMARK)

| Hạng Mục | 📱 Khung DỌC (9:16)<br>*(TikTok / Shorts / Reels)* | 🖥️ Khung NGANG (16:9)<br>*(YouTube / Web / Catalog)* | Ghi Chú Kỹ Thuật |
| :--- | :---: | :---: | :--- |
| **Độ Phân Giải Full HD** | `1080 × 1920 px` | `1920 × 1080 px` | 30 FPS, tốc độ render 25-35 giây |
| **Độ Phân Giải 4K UHD** | `2160 × 3840 px` | `3840 × 2160 px` | Ultra HD siêu sắc nét |
| **Trục Trọng Lực 3D** | `UpVector = (0, 1, 0)` | `UpVector = (0, 1, 0)` | Khóa trục Y, mô hình thẳng đứng 90° tuyệt đối |
| **Tâm Ngắm Camera 3D** | `Target = centerPt (cx, cy, cz)` | `Target = centerPt (cx, cy, cz)` | 100% trích xuất từ RangeBox vật lý |
| **Cảnh Đầu: Tỷ Lệ Chiều Cao** | **90%** khung hình (`dy / 0.90`) | **74%** khung hình (`dy / 0.74`) | To lớn, choáng ngợp, lề an toàn không tràn mép |
| **Cảnh Cuối: Tỷ Lệ Chiều Cao** | **82%** khung hình (`dy / 0.82`) | **72%** khung hình (`dy / 0.72`) | Thoáng đãng, đỉnh chóp có lề an toàn 14% |
| **Góc Nghiêng Cảnh Đầu** | `-0.16 rad` (~-10°) | `-0.16 rad` (~-10°) | Góc 3/4 DƯỚI ngước lên hùng vĩ |
| **Góc Nghiêng Cảnh Cuối** | `+0.25 rad` (~+14°) | `+0.25 rad` (~+14°) | Góc 3/4 TRÊN bao quát nóc bồn |
| **Góc Quay Ban Đầu** | `initialAngle = π / 4.0` (45°) | `initialAngle = π / 4.0` (45°) | Chuẩn đối xứng Isometric |
| **Nét Xanh Bản Vẽ 2D** | `#0228AA` (R=2, G=40, B=170) | `#0228AA` (R=2, G=40, B=170) | Deep Royal Navy Blueprint + Gamma Boost 1.45x |
| **Ngưỡng Nhận Diện Bounding Box** | `brightnessSum < 450` | `brightnessSum < 450` | Ôm sát mô hình, loại bỏ 100% màu nền xung quanh |
| **Khoảng Cách Khung Chữ Ngang** | `dimY + 18px` | `dimY + 18px` | Nằm dưới, thoáng đãng, không đè mũi tên/chân đế |
| **Khoảng Cách Khung Chữ Dọc** | `dimX + 24px` (Xoay dọc -90°) | `dimX + 24px` (Xoay dọc -90°) | Xoay dọc chuẩn CAD, không đè mũi tên/mép mô hình |
| **Khoảng Cách Thẻ Tiêu Đề Trên** | `minY - badgeH - 35px` | `minY - badgeH - 35px` | Cách đỉnh mô hình ít nhất 35px |
| **Mã Hóa Video (FFmpeg)** | `-c:v libx264 -crf 16 -preset medium` | `-c:v libx264 -crf 16 -preset medium` | Chất lượng cao, màu chuẩn, dung lượng tối ưu |
| **Thumbnail Bìa Video MP4** | `_01_Hero3D_Iso_TopRight` | `_01_Hero3D_Iso_TopRight` | Tự động nhúng Cover Art Poster vào file MP4 |

---

## PHẦN 2: BẢNG CHECKLIST KIỂM ĐỊNH XUẤT BẢN 10 BƯỚC (10-STEP QA CHECKLIST)

Khi chạy xuất bản cho bất kỳ cụm bồn, cột lọc hay máy móc nào trong Inventor, đối chiếu 10 tiêu chí sau:

- [ ] **1. Trục đứng 90°:** Thân mô hình (cột đèn, bồn lọc, ống) **đứng thẳng 90 độ hoàn hảo**, chân đế nằm ngang phẳng phiu song song mép đáy.
- [ ] **2. Cảnh đầu (Scene 1):** Mô hình xoay tròn 360 độ **to lớn vừa vặn** (Dọc 90%, Ngang 74%), không chạm mép trên/dưới.
- [ ] **3. Cảnh cuối (Scene 5 & 6):** Mô hình xoay góc trên **thoáng đãng** (Dọc 82%, Ngang 72%), đỉnh chóp có khoảng trống an toàn.
- [ ] **4. Chuyển cảnh (Flights 1-4):** Chuyến bay lướt chuyển góc mượt mà với hiệu ứng hãm phanh Speed Ramp.
- [ ] **5. Nét xanh 2D (Scenes 2, 3, 4):** Các đường nét cơ khí có màu **xanh đậm đà `#0228AA`, dày dặn, sắc nét và mịn màng**, không bị mờ nhạt hay răng cưa.
- [ ] **6. Số đo kích thước:** Số liệu $L \times W \times H$ (mm) **chính xác 100%** trích xuất từ RangeBox hình học.
- [ ] **7. Vị trí khung chữ DIM:** Khung chữ ngang nằm **dưới (cách 18px)**, khung chữ dọc **xoay 90 độ bên phải (cách 24px)**, hoàn toàn **không đè lên mũi tên hay mép mô hình**.
- [ ] **8. Thẻ tiêu đề:** Thẻ tên bản vẽ trên cùng nằm căn giữa và **cách đỉnh mô hình ít nhất 35px**.
- [ ] **9. Bộ ảnh xuất bản:** Thư mục ảnh xuất ra đủ **10 ảnh chất lượng cao** (Hero 3D, Wireframe, Studio, Bản vẽ Blueprint) với tên file chuẩn xác.
- [ ] **10. Video Thumbnail:** Tệp MP4 trên Windows Explorer hiển thị **ảnh bìa ViewCube 3D thẳng tắp đẹp mắt**.

---

## PHẦN 3: MA TRẬN KHẮC PHỤC SỰ CỐ NHANH (TROUBLESHOOTING MATRIX)

| Hiện Tượng / Lỗi | Nguyên Nhân Gốc Rễ | Vị Trí Code & Cách Khắc Phục Nhanh |
| :--- | :--- | :--- |
| **Mô hình bị nghiêng/xéo 45°** | Dùng lệnh góc nhìn tự động của Inventor | Khóa `oCam.UpVector = tg.CreateUnitVector(0, 1, 0)` và `oCam.Target = centerPt`. |
| **Cảnh đầu bị tràn mép / khuất đỉnh** | Cự ly camera bị đặt quá gần | Giữ tỷ lệ chuẩn: Khung Dọc `dy / 0.90`, Khung Ngang `dy / 0.74`. |
| **Cảnh cuối bị to quá / cấn chóp** | Thiếu khoảng lùi khi nhìn chúc từ trên xuống | Giữ tỷ lệ chuẩn: Khung Dọc `dy / 0.82`, Khung Ngang `dy / 0.72`. |
| **Đường DIM bị tràn ra mép khung hình** | Ngưỡng màu nhận nhầm màu nền xám nhạt | Giữ ngưỡng `brightnessSum < 450` và quét giới hạn `5 To h-6`. |
| **Khung chữ DIM đè lên mũi tên / chân đế** | Khung chữ đặt quá sát đường kích thước | Giữ offset: Ngang `dimY + 18px`, Dọc `dimX + 24px` xoay `-90°`. |
| **Nét xanh bị mờ nhạt** | Hệ số hòa trộn Alpha chưa đủ đậm | Dùng màu `#0228AA` kết hợp Gamma Boost `1.45x` và Dilation 1-pixel. |
| **Nét 3D bị răng cưa bậc thang** | Inventor đang để Hardware = Performance | Vào Inventor $\rightarrow$ Tools $\rightarrow$ Application Options $\rightarrow$ Hardware $\rightarrow$ chọn **Quality**. |
| **Thumbnail MP4 không hiện ảnh 3D** | FFmpeg thiếu luồng Attached Picture | Đảm bảo lệnh FFmpeg có `-disposition:v:1 attached_pic`. |

---

## PHẦN 4: LỆNH HOÀN NGUYÊN PHIÊN BẢN (INSTANT ROLLBACK)

Khi cần khôi phục lại phiên bản chuẩn Master v7.0, mở PowerShell và chạy:
```powershell
powershell -File "D:\WT3D_Project\Z_Tools\WT3D_Version_Manager.ps1"
```
Chọn **`[3] RESTORE`** $\rightarrow$ Chọn phiên bản **`v_..._LOCKED_MASTER_FINAL_v7_ALL_MODES_OK`**.
