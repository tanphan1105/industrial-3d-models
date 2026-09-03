wt3d_dialog : dialog {
    label = "WT3D PRO STUDIO - AUTOCAD 2025 CONTROL PANEL";
    spacer;
    : text {
        label = "🚀 BẢNG CÔNG CỤ ĐIỀU KHIỂN & TỐI ƯU HÓA 1-CHẠM";
        alignment = centered;
    }
    spacer;
    : boxed_column {
        label = "⚡ TỐI ƯU HIỆU NĂNG (0ms DELAY)";
        : button {
            key = "btn_fast";
            label = "⚡ LÀM NHẸ HỆ THỐNG (0ms Delay, Không Lag)";
            width = 38;
            height = 2;
            is_default = true;
        }
        : button {
            key = "btn_purge";
            label = "🧹 DỌN RÁC & SỬA LỖI FILE (Purge + Audit)";
            width = 38;
        }
        : button {
            key = "btn_reset";
            label = "🔄 PHỤC HỒI CÀI ĐẶT MẶC ĐỊNH GỐC";
            width = 38;
        }
    }
    spacer;
    : boxed_column {
        label = "🔤 QUẢN LÝ FONT & BẢNG MÃ CHỮ VIỆT";
        : button {
            key = "btn_v2u";
            label = "🔤 CHUYỂN VNI -> UNICODE ARIAL (Sửa lỗi toàn bản vẽ)";
            width = 38;
            height = 2;
        }
        : button {
            key = "btn_sf";
            label = "🎯 QUÉT CHỌN VÙNG & ĐỔI FONT (Arial, Times, VNI...)";
            width = 38;
        }
    }
    spacer;
    : row {
        : button {
            key = "cancel";
            label = "Đóng";
            is_cancel = true;
            width = 15;
            alignment = centered;
        }
    }
}
