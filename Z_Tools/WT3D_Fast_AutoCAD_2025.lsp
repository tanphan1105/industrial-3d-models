(defun c:WT3D_FAST ()
  (vl-load-com)
  ;; ---------------------------------------------------------------------------
  ;; 1. TỐI ƯU HIỆU NĂNG SIÊU NHẸ & PHẢN HỒI TỨC THÌ (0ms DELAY)
  ;; ---------------------------------------------------------------------------
  (mapcar '(lambda (x) (vl-catch-all-apply 'setvar x))
    '(("VTDURATION" 0)          ; Zoom & Pan tức thì 0ms (tắt trễ chuyển cảnh 750ms)
      ("HPQUICKPREVIEW" 0)      ; Tắt tính toán Hatch tự động gây đơ chuột
      ("HPMAXAREAS" 100)        ; Giới hạn vùng tính toán Hatch
      ("SELECTIONCYCLING" 0)    ; Tắt icon chồng chéo làm khựng chuột
      ("ROLLOVERTOOLTIPS" 0)    ; Tắt bong bóng thông tin khi rê qua nét vẽ
      ("SELECTIONEFFECT" 0)     ; Dùng viền nét đứt cổ điển nhẹ GPU
      ("PRESELECTIONEFFECT" 0)  ; Tắt phát sáng trước khi chọn đối tượng
      ("LINESMOOTHING" 0)       ; Tối ưu hóa GPU cho đường nét CAD cơ khí
      ("INPUTSEARCHDELAY" 200)  ; Tối ưu hóa tốc độ gõ dòng lệnh
      ("DWGCHECK" 0)            ; Tắt cảnh báo phiên bản DWG khi mở file
      ("INDEXCTL" 3)            ; Tối ưu hóa Index Layer & Không gian cho Xref
      ("XLOADCTL" 2)            ; Bật Demand Loading mở bản vẽ lớn siêu tốc
      ("CACHEMAXFILES" 256)     ; Bộ nhớ đệm RAM tối đa
      ("CACHEMAXTOTALSIZE" 1024); Bộ nhớ đệm đồ họa 1GB
      ("PALETTEOPAQUE" 1)       ; Tắt độ trong suốt thanh Properties/Layer để nhẹ GPU
      
      ;; -----------------------------------------------------------------------
      ;; 2. MÔI TRƯỜNG VẼ THÔNG MINH (SMART DRAWING ENVIRONMENT)
      ;; -----------------------------------------------------------------------
      ("OSMODE" 4287)           ; Bật trọn bộ bắt điểm vàng: Đầu mút, Tâm, Trung điểm, Giao điểm, Vuông góc, Tiếp tuyến
      ("AUTOSNAP" 63)           ; Bật Nam châm hút điểm + Tooltip + Tia dóng trực quan
      ("POLARMODE" 2)           ; Bắt góc thông minh Polar Tracking
      ("POLARANG" 45)           ; Bắt các góc vàng 45°, 90°, 135°, 180°
      ("TRACKPATH" 0)           ; Tia dóng vô tận giúp căn chỉnh thiết bị từ xa
      ("CURSORSIZE" 100)        ; Sợi tóc chữ thập Crosshair 100% màn hình dóng thẳng cực chuẩn
      ("APERTURE" 10)           ; Vùng bắt điểm vừa vặn, không bị trượt chuột
      ("GRIPSIZE" 5)            ; Kích thước điểm Grip màu xanh tối ưu
      ("GRIPMULTIFUNCTION" 3)   ; Bật menu đa năng khi rê chuột vào Grip (kéo dài, thêm đỉnh)
      
      ;; -----------------------------------------------------------------------
      ;; 3. THAO TÁC CHỌN LỌC & CO GIÃN THÔNG MINH
      ;; -----------------------------------------------------------------------
      ("PICKFIRST" 1)           ; Cho phép chọn đối tượng trước rồi mới gõ lệnh
      ("PICKADD" 2)             ; Chọn cộng dồn liên tục không bị mất vùng chọn cũ
      ("EDGEMODE" 0)            ; Cắt tỉa chuẩn xác đúng giao điểm
      ("DRAWORDERCTL" 3)        ; Text và Dimension luôn tự động nổi trên mặt Hatch
      ("DIMASSOC" 2)            ; Kích thước tự động co giãn theo mô hình khi di chuyển
    )
  )
  (princ "
🚀 [WT3D] ĐÃ TỐI ƯU HÓA CẤU HÌNH HỆ THỐNG & MÔI TRƯỜNG VẼ AUTOCAD 2025 THÀNH CÔNG!
")
  (princ)
)

;; Tự động kích hoạt ngay khi nạp file
(c:WT3D_FAST)
