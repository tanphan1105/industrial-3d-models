; ==============================================================================
; WT3D PRO LISP: CHUYỂN ĐỔI BẢNG MÃ TCVN3 (ABC) SANG UNICODE CHUẨN ARIAL CHO CAD
; Tác giả: Phan Trọng Tấn - WaterTreatment3D
; Lệnh: C2U (Convert TCVN3 to Unicode)
; ==============================================================================

(defun c:C2U (/ ss i ent obj txtStr newStr)
  (vl-load-com)
  (princ "
👉 Chọn các đối tượng chữ (Text/MText) bị lỗi font TCVN3 (hoặc gõ ALL): ")
  (setq ss (ssget '((0 . "TEXT,MTEXT"))))
  (if ss
    (progn
      (setq i 0)
      (while (< i (sslength ss))
        (setq ent (ssname ss i))
        (setq obj (vlax-ename->vla-object ent))
        (setq txtStr (vla-get-TextString obj))
        (setq newStr (tcvn3->unicode txtStr))
        (vla-put-TextString obj newStr)
        (setq i (1+ i))
      )
      (command "_.regenall")
      (princ (strcat "
💎 [WT3D] ĐÃ CHUYỂN ĐỔI THÀNH CÔNG " (itoa (sslength ss)) " ĐỐI TƯỢNG CHỮ SANG UNICODE ARIAL CHUẨN!"))
    )
    (princ "
Không có đối tượng chữ nào được chọn.")
  )
  (princ)
)

;; Hàm thuật toán hoán đổi ký tự TCVN3 sang Unicode
(defun tcvn3->unicode (str / res c code uStr)
  (setq res "")
  (setq len (strlen str))
  (setq idx 1)
  (while (<= idx len)
    (setq c (substr str idx 1))
    (setq code (ascii c))
    (setq uStr (tcvn-char-map code))
    (if uStr
      (setq res (strcat res uStr))
      (setq res (strcat res c))
    )
    (setq idx (1+ idx))
  )
  res
)

;; Bảng ánh xạ mã TCVN3 sang chuỗi Unicode
(defun tcvn-char-map (code)
  (cond
    ;; Ký tự thường
    ((= code 181) "\U+00E0") ; à
    ((= code 182) "\U+1EA3") ; ả
    ((= code 183) "\U+00E3") ; ã
    ((= code 184) "\U+00E1") ; á
    ((= code 185) "\U+1EA1") ; ạ
    ((= code 168) "\U+0103") ; ă
    ((= code 169) "\U+00E2") ; â
    ((= code 202) "\U+1EDB") ; ớ
    ((= code 200) "\U+1EDF") ; ở
    ((= code 199) "\U+1EDD") ; ờ
    ((= code 201) "\U+1EE1") ; ỡ
    ((= code 203) "\U+1EE3") ; ợ
    ((= code 198) "\U+01A1") ; ơ
    ((= code 209) "\U+01B0") ; ư
    ((= code 213) "\U+1EE9") ; ứ
    ((= code 210) "\U+1EEB") ; ừ
    ((= code 211) "\U+1EED") ; ử
    ((= code 212) "\U+1EEF") ; ữ
    ((= code 214) "\U+1EF1") ; ự
    ((= code 174) "\U+0111") ; đ
    ;; Ký tự hoa
    ((= code 161) "\U+0102") ; Ă
    ((= code 162) "\U+00C2") ; Â
    ((= code 163) "\U+00CA") ; Ê
    ((= code 164) "\U+00D4") ; Ô
    ((= code 165) "\U+01A0") ; Ơ
    ((= code 166) "\U+01AF") ; Ư
    ((= code 167) "\U+0110") ; Đ
    (t nil)
  )
)
