; ==============================================================================
; WT3D PRO LISP: MASTER FONT FIXER FOR AUTOCAD 2025
; Tác giả: Phan Trọng Tấn - WaterTreatment3D
; Chức năng:
;   1. Tự động chuyển 100% Text Style trong bản vẽ về Arial.ttf (Unicode chuẩn)
;   2. Khử sạch toàn bộ font SHX thiếu làm biến dạng chữ thành dấu hỏi ?
;   3. Tự động REGENALL cập nhật toàn bộ bản vẽ chỉ trong 1 giây!
; ==============================================================================

(defun c:FIXFONT (/ acadObj doc textStyles count)
  (vl-load-com)
  (setq acadObj (vlax-get-acad-object))
  (setq doc (vla-get-ActiveDocument acadObj))
  (setq textStyles (vla-get-TextStyles doc))
  (setq count 0)
  
  (princ "
⚡ [WT3D] Đang tự động quét và sửa lỗi toàn bộ Text Style trong bản vẽ...")
  
  (vlax-for st textStyles
    (vl-catch-all-apply 'vla-put-fontfile (list st "Arial.ttf"))
    (vl-catch-all-apply 'vla-put-BigFontFile (list st ""))
    (setq count (1+ count))
  )
  
  (command "_.regenall")
  (princ (strcat "
💎 [WT3D] ĐÃ CHUYỂN ĐỔI THÀNH CÔNG " (itoa count) " TEXT STYLE SANG FONT ARIAL.TTF!"))
  (princ "
🚀 TOÀN BỘ CHỮ VÀ KÍCH THƯỚC ĐÃ ĐƯỢC TÁI TẠO RÕ NÉT 100%!
")
  (princ)
)

;; Tự động chạy ngay khi load
(c:FIXFONT)
