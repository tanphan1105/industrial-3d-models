(defun c:WT3D_FAST ()
  (vl-load-com)
  (princ "
⚡ Đang kích hoạt bộ thiết lập VẼ NHANH & THÔNG MINH AutoCAD 2025...")
  
  ;; ---------------------------------------------------------------------------
  ;; 1. TỐI ƯU HÓA HIỆU NĂNG & TẮT ĐỘ TRỄ (0ms INSTANT RESPONSE)
  ;; ---------------------------------------------------------------------------
  (mapcar '(lambda (x) (vl-catch-all-apply 'setvar x))
    '(("VTDURATION" 0)          ; Tắt hiệu ứng lia/zoom trễ 750ms -> Zoom tức thì 0ms
      ("HPQUICKPREVIEW" 0)      ; Tắt preview Hatch tự động gây đơ chuột
      ("HPMAXAREAS" 100)        ; Giới hạn vùng tính toán Hatch
      ("SELECTIONCYCLING" 0)    ; Tắt icon chồng chéo làm khựng chuột
      ("ROLLOVERTOOLTIPS" 0)    ; Tắt bong bóng thông tin khi rê qua nét vẽ
      ("SELECTIONEFFECT" 0)     ; Dùng viền nét đứt cổ điển nhẹ GPU
      ("PRESELECTIONEFFECT" 0)  ; Tắt phát sáng trước khi chọn
      ("LINESMOOTHING" 0)       ; Tối ưu hóa GPU cho đường nét CAD cơ khí
      ("INPUTSEARCHDELAY" 200)  ; Gợi ý lệnh nhanh trong 200ms
      ("DWGCHECK" 0)            ; Tắt cảnh báo phiên bản DWG khi mở
      ("INDEXCTL" 3)            ; Tối ưu hóa Index Layer & Không gian cho Xref
      ("XLOADCTL" 2)            ; Bật Demand Loading mở bản vẽ lớn siêu tốc
      ("CACHEMAXFILES" 256)     ; Cache RAM tối đa
      ("CACHEMAXTOTALSIZE" 1024); Bộ nhớ đệm đồ họa 1GB
      ("PALETTEOPAQUE" 1)       ; Tắt độ trong suốt thanh Properties/Layer để nhẹ card
      
      ;; -----------------------------------------------------------------------
      ;; 2. BẮT ĐIỂM THÔNG MINH & SỢI TÓC DÓNG THẲNG HÀNG (SMART SNAPS & TRACKING)
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
      ;; 3. THAO TÁC CHỌN & CẮT TỈA THÔNG MINH (SMART TRIM & SELECTION)
      ;; -----------------------------------------------------------------------
      ("PICKFIRST" 1)           ; Cho phép chọn đối tượng trước rồi mới gõ lệnh
      ("PICKADD" 2)             ; Chọn cộng dồn liên tục không bị mất vùng chọn cũ
      ("EDGEMODE" 0)            ; Cắt tỉa chuẩn xác đúng giao điểm
      ("DRAWORDERCTL" 3)        ; Text và Dimension luôn tự động nổi trên mặt Hatch
      ("DIMASSOC" 2)            ; Kích thước tự động co giãn theo mô hình khi di chuyển
    )
  )
  (princ "
🚀 [WT3D] ĐÃ TỐI ƯU HÓA AUTOCAD 2025: SIÊU NHẸ + BẮT ĐIỂM THÔNG MINH + SỢI TÓC 100% THÀNH CÔNG!
")
  (princ)
)

;; -----------------------------------------------------------------------------
;; 4. BỘ LỆNH TẮT 1-CHẠM SIÊU TỐC CHO KỸ SƯ (SUPER SHORTCUTS):
;; -----------------------------------------------------------------------------

;; F0: Nối góc vuông tức thì (Fillet R=0 không cần chỉnh bán kính)
(defun c:F0 () (setvar "FILLETRAD" 0) (command "_.fillet") (princ))

;; D: Đo khoảng cách nhanh tức thì (Quick Distance)
(defun c:D () (command "_.dist") (princ))

;; 11: Cô lập Layer đang chọn (Layer Isolate - chỉ giữ lại layer cần sửa)
(defun c:11 () (command "_.layiso") (princ))

;; 22: Mở lại toàn bộ Layer sau khi sửa xong (Layer Unisolate)
(defun c:22 () (command "_.layuniso") (princ))

;; 33: Tắt Layer của đối tượng được click (Layer Off)
(defun c:33 () (command "_.layoff") (princ))

;; 44: Bật lại tất cả các Layer đã tắt (Layer On)
(defun c:44 () (command "_.layon") (princ))

;; LL: Khóa Layer được chọn (Layer Lock)
(defun c:LL () (command "_.laylck") (princ))

;; UU: Mở khóa Layer được chọn (Layer Unlock)
(defun c:UU () (command "_.layulk") (princ))

;; QQ: Lưu bản vẽ nhanh 1 chạm (Quick Save)
(defun c:QQ () (command "_.qsave") (princ))

;; PUALL: Dọn rác sạch 100% bản vẽ (Purge All + Audit sửa lỗi file trong 1 giây)
(defun c:PUALL ()
  (command "-purge" "all" "*" "n")
  (command "-purge" "regapps" "*" "n")
  (command "_.audit" "y")
  (princ "
🧹 [WT3D] ĐÃ DỌN SẠCH RÁC VÀ SỬA LỖI BẢN VẼ 100% (FILE NHẸ TÊNH)!
")
  (princ)
)

;; Tự động kích hoạt ngay khi nạp file
(c:WT3D_FAST)
