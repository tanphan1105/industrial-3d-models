---
name: apple-web-design-and-a4-print
description: Comprehensive standard for Apple-inspired web design (SF Pro typography, Bento grid, micro-interactions, subtle glassmorphism) and pixel-perfect CSS A4 Portrait multi-page print pagination standards.
---

# 🍎 Chuẩn Thiết Kế Web Apple (Apple Web Design System) & Chuẩn In Ấn PDF A4 Dọc (A4 Portrait Print Pagination Standard) 2026

Tài liệu này tổng hợp toàn bộ quy chuẩn kiến trúc giao diện lấy cảm hứng từ **Apple Store Online (`apple.com/vn/store`)** kết hợp với **Tiêu chuẩn CSS In Ấn A4 Dọc đa trang hoàn hảo** không bao giờ bị cắt vỡ layout, tràn bảng hay nhảy trang lỗi.

---

## 🎨 PHẦN 1: NGUYÊN TẮC THIẾT KẾ GIAO DIỆN PHONG CÁCH APPLE (APPLE 5S DESIGN SYSTEM)

### 1. Hệ Thống Màu Sắc Apple Light 5S (Apple Color Palette):
*   **Nền Trang (`--bg-page`)**: `#fbfbfd` (Màu trắng kem siêu nhẹ, tạo cảm giác sang trọng, không chói mắt).
*   **Nền Bề Mặt (`--bg-surface`)**: `#ffffff` (Trắng tinh khiết cho các thẻ Card).
*   **Nền Phụ Trợ (`--bg-subtle`)**: `#f5f5f7` (Xám bạc nhạt dùng cho bảng, ô nhập, nút phụ).
*   **Chữ Chính (`--text-main`)**: `#1d1d1f` (Đen than chì sang trọng, độ tương phản cao tuyệt đối).
*   **Chữ Phụ (`--text-secondary`)**: `#6e6e73` (Xám trung tính cho mô tả).
*   **Màu Điểm Nhấn (Vibrant Accents)**:
    *   🔵 **Apple Blue**: `#0071e3` (Nút bấm, link, tab đang chọn).
    *   🟢 **Apple Emerald**: `#34c759` (Thành công, thực nhận doanh thu, trạng thái hoàn tất).
    *   🟠 **Apple Orange**: `#ff9500` (Cảnh báo, điểm nhấn kỹ thuật, nhãn đặc biệt).
    *   🟣 **Apple Purple**: `#5856d6` (Tính năng nâng cao, phân tích).
    *   🔴 **Apple Crimson**: `#e11d48` (Thị trường Trung Quốc / CGModel).
    *   🌊 **Apple Cyan / Teal**: `#0284c7` (TurboSquid / CheckMate).

### 2. Hệ Thống Typography (SF Pro Type Scale):
```css
font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```
*   **Tiêu đề lớn (Hero Title)**: `2.2rem - 2.8rem`, `font-weight: 800`, `letter-spacing: -0.03em`, `line-height: 1.15`.
*   **Tiêu đề thẻ (Card Title)**: `1.15rem - 1.35rem`, `font-weight: 700`, `letter-spacing: -0.01em`.
*   **Nhãn phân loại (Eyebrow Pill Badge)**: `font-size: 0.72rem`, `font-weight: 700`, `text-transform: uppercase`, `letter-spacing: 0.06em`, bọc trong pill tròn viền mờ.
*   **Nội dung văn bản (Body)**: `font-size: 0.92rem - 0.95rem`, `line-height: 1.55`.

### 3. Bố Cục Thẻ Bento Modular Grid (Apple Bento Layout):
*   Khung lưới 12 cột linh hoạt (`grid-template-columns: repeat(12, 1fr)`).
*   Bo tròn góc lớn mượt mà: `border-radius: 16px` đến `24px`.
*   Viền mờ tinh xảo: `border: 1px solid rgba(0, 0, 0, 0.08)` hoặc `#e5e5ea`.
*   Đổ bóng mềm: `box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04)`.
*   Hiệu ứng rê chuột: Nâng nhẹ thẻ `transform: translateY(-2px)`, tăng bóng `box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08)`.

---

## 🖨️ PHẦN 2: TIÊU CHUẨN CSS IN ẤN A4 DỌC ĐA TRANG HOÀN HẢO (A4 PORTRAIT PRINT CSS)

Để file HTML khi bấm `Ctrl + P` hoặc `window.print()` xuất ra file **PDF A4 Dọc** đẹp như một cuốn catalogue in ấn thương mại:

### 1. Khai Báo Trang Khóa Cứng A4 Dọc (`@page`):
```css
@media print {
    @page {
        size: A4 portrait;
        margin: 12mm 15mm 15mm 15mm; /* Canh lề chuẩn: Trên 12mm, Trái-Phải-Dưới 15mm */
    }

    /* Thiết lập nền trắng & độ sắc nét mực in */
    body {
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 9pt !important;
        line-height: 1.45 !important;
        padding: 0 !important;
        margin: 0 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
}
```

### 2. Cơ Chế Chống Cắt Xé Thẻ & Tránh Nhảy Trang Lỗi (Anti-Break Engine):
```css
@media print {
    /* 1. Tuyệt đối không cắt đôi thẻ Card hoặc khối nội dung */
    .bento-card, .stat-box, .protips-box, .print-card {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
        box-shadow: none !important;
        border: 1pt solid #d1d1d6 !important;
        margin-bottom: 12pt !important;
    }

    /* 2. Tiêu đề không bao giờ bị mồ côi ở cuối trang */
    h1, h2, h3, h4, .card-header {
        break-after: avoid !important;
        page-break-after: avoid !important;
    }

    /* 3. Bảng dữ liệu tự động lặp lại tiêu đề khi qua trang mới */
    table {
        width: 100% !important;
        border-collapse: collapse !important;
    }
    thead {
        display: table-header-group !important; /* Lặp lại Header bảng trên mỗi trang A4 */
    }
    tr {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }

    /* 4. Ẩn toàn bộ các nút bấm tương tác, thanh search, modal khóa */
    .no-print, .btn, .search-bar, #wt3d-security-modal, #toast, header .header-actions {
        display: none !important;
    }

    /* 5. Mở rộng toàn bộ các thanh cuộn để in hết 100% danh mục */
    .scroll-container, .models-scroll-container {
        max-height: none !important;
        overflow: visible !important;
        border: none !important;
    }
}
```

---

## 🚀 PHẦN 3: BỘ KHUNG TEMPLATE MẪU TÍCH HỢP ĐẦY ĐỦ (READY-TO-USE BOILERPLATE)

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apple Style A4 Portrait Document</title>
    <style>
        :root {
            --bg-page: #fbfbfd;
            --bg-surface: #ffffff;
            --bg-subtle: #f5f5f7;
            --text-main: #1d1d1f;
            --text-secondary: #6e6e73;
            --apple-blue: #0071e3;
            --radius-card: 18px;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
            background: var(--bg-page);
            color: var(--text-main);
            margin: 0; padding: 24px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .bento-card {
            background: var(--bg-surface);
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: var(--radius-card);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        }
        @media print {
            @page { size: A4 portrait; margin: 12mm 15mm; }
            body { background: #ffffff !important; padding: 0 !important; font-size: 9pt !important; }
            .bento-card { break-inside: avoid !important; box-shadow: none !important; border: 1pt solid #ccc !important; }
            .no-print { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="bento-card">
            <h1>Tiêu Đề Hồ Sơ Chuẩn Apple</h1>
            <p>Nội dung hiển thị tuyệt đẹp trên màn hình và in ấn chuẩn A4 dọc.</p>
        </div>
    </div>
</body>
</html>
```
