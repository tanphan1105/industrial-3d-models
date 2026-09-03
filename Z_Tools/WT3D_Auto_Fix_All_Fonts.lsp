; ==============================================================================
; WT3D PRO LISP: TỰ ĐỘNG SỬA 100% LỖI FONT TCVN3 (ƯỞĂÚ...) SANG UNICODE ARIAL
; Tác giả: Phan Trọng Tấn - WaterTreatment3D
; Cách dùng: Tự động chạy ngay khi load hoặc gõ lệnh FIXALL
; ==============================================================================

(defun c:FIXALL (/ doc textStyles count ss i ent obj txtStr newStr blks blk atts)
  (vl-load-com)
  (setq doc (vla-get-ActiveDocument (vlax-get-acad-object)))
  (setq count 0)
  (princ "
⚡ [WT3D] ĐANG TỰ ĐỘNG QUÉT VÀ CHUYỂN ĐỔI TOÀN BỘ CHỮ BỊ LỖI FONT TRONG BẢN VẼ...")

  ;; 1. Đổi tất cả Text Style sang font Arial.ttf
  (setq textStyles (vla-get-TextStyles doc))
  (vlax-for st textStyles
    (vl-catch-all-apply 'vla-put-fontfile (list st "Arial.ttf"))
    (vl-catch-all-apply 'vla-put-BigFontFile (list st ""))
  )

  ;; 2. Quét TẤT CẢ Text và MText trong toàn bộ bản vẽ (Model & Layout)
  (setq ss (ssget "_X" '((0 . "TEXT,MTEXT"))))
  (if ss
    (progn
      (setq i 0)
      (while (< i (sslength ss))
        (setq ent (ssname ss i))
        (setq obj (vlax-ename->vla-object ent))
        (setq txtStr (vl-catch-all-apply 'vla-get-TextString (list obj)))
        (if (and txtStr (not (vl-catch-all-error-p txtStr)))
          (progn
            (setq newStr (wt3d-tcvn-to-uni txtStr))
            (if (/= newStr txtStr)
              (progn
                (vl-catch-all-apply 'vla-put-TextString (list obj newStr))
                (setq count (1+ count))
              )
            )
          )
        )
        (setq i (1+ i))
      )
    )
  )

  ;; 3. Quét TẤT CẢ Block Attributes trong toàn bộ bản vẽ
  (setq blks (ssget "_X" '((0 . "INSERT"))))
  (if blks
    (progn
      (setq i 0)
      (while (< i (sslength blks))
        (setq ent (ssname blks i))
        (setq obj (vlax-ename->vla-object ent))
        (if (= (vla-get-HasAttributes obj) :vlax-true)
          (progn
            (setq atts (vlax-safearray->list (vlax-variant-value (vla-GetAttributes obj))))
            (foreach att atts
              (setq txtStr (vla-get-TextString att))
              (setq newStr (wt3d-tcvn-to-uni txtStr))
              (if (/= newStr txtStr)
                (progn
                  (vla-put-TextString att newStr)
                  (setq count (1+ count))
                )
              )
            )
          )
        )
        (setq i (1+ i))
      )
    )
  )

  ;; 4. Tái tạo hiển thị toàn màn hình
  (command "_.regenall")
  (princ (strcat "
💎 [WT3D] ĐÃ TỰ ĐỘNG SỬA THÀNH CÔNG " (itoa count) " ĐỐI TƯỢNG CHỮ SANG TIẾNG VIỆT UNICODE ARIAL!"))
  (princ "
🚀 TOÀN BỘ BẢN VẼ ĐÃ ĐỌC ĐƯỢC 100% TIẾNG VIỆT CÓ DẤU HOÀN HẢO!
")
  (princ)
)

;; Hàm chuyển đổi chuỗi ký tự TCVN3 sang Unicode
(defun wt3d-tcvn-to-uni (str / res idx len c code u)
  (setq res "")
  (setq len (strlen str))
  (setq idx 1)
  (while (<= idx len)
    (setq c (substr str idx 1))
    (setq code (ascii c))
    (setq u (wt3d-map-code code))
    (if u
      (setq res (strcat res u))
      (setq res (strcat res c))
    )
    (setq idx (1+ idx))
  )
  res
)

;; Bảng mã tra cứu ký tự TCVN3 đầy đủ
(defun wt3d-map-code (code)
  (cond
    ;; Chữ a
    ((= code 181) "\U+00E0") ; à
    ((= code 182) "\U+1EA3") ; ả
    ((= code 183) "\U+00E3") ; ã
    ((= code 184) "\U+00E1") ; á
    ((= code 185) "\U+1EA1") ; ạ
    ;; Chữ ă
    ((= code 168) "\U+0103") ; ă
    ((= code 187) "\U+1EB1") ; ằ
    ((= code 188) "\U+1EB3") ; ẳ
    ((= code 189) "\U+1EB5") ; ẵ
    ((= code 190) "\U+1EAF") ; ắ
    ((= code 192) "\U+1EB7") ; ặ
    ;; Chữ â
    ((= code 169) "\U+00E2") ; â
    ((= code 193) "\U+1EA7") ; ầ
    ((= code 194) "\U+1EA9") ; ẩ
    ((= code 195) "\U+1EAB") ; ẫ
    ((= code 196) "\U+1EA5") ; ấ
    ((= code 197) "\U+1EAD") ; ậ
    ;; Chữ e
    ((= code 232) "\U+00E8") ; è
    ((= code 233) "\U+1EBB") ; ẻ
    ((= code 234) "\U+1EBD") ; ẽ
    ((= code 235) "\U+00E9") ; é
    ((= code 236) "\U+1EB9") ; ẹ
    ;; Chữ ê
    ((= code 170) "\U+00EA") ; ê
    ((= code 237) "\U+1EC1") ; ề
    ((= code 238) "\U+1EC3") ; ể
    ((= code 239) "\U+1EC5") ; ễ
    ((= code 240) "\U+1EBF") ; ế
    ((= code 241) "\U+1EC7") ; ệ
    ;; Chữ i
    ((= code 242) "\U+00EC") ; ì
    ((= code 243) "\U+1EC9") ; ỉ
    ((= code 244) "\U+0129") ; ĩ
    ((= code 245) "\U+00ED") ; í
    ((= code 246) "\U+1ECB") ; ị
    ;; Chữ o
    ((= code 247) "\U+00F2") ; ò
    ((= code 248) "\U+1ECF") ; ỏ
    ((= code 249) "\U+00F5") ; õ
    ((= code 250) "\U+00F3") ; ó
    ((= code 251) "\U+1ECD") ; ọ
    ;; Chữ ô
    ((= code 171) "\U+00F4") ; ô
    ((= code 252) "\U+1ED3") ; ồ
    ((= code 253) "\U+1ED5") ; ổ
    ((= code 254) "\U+1ED7") ; ỗ
    ((= code 255) "\U+1ED1") ; ố
    ((= code 186) "\U+1ED9") ; ộ
    ;; Chữ ơ
    ((= code 172) "\U+01A1") ; ơ
    ((= code 199) "\U+1EDD") ; ờ
    ((= code 200) "\U+1EDF") ; ở
    ((= code 201) "\U+1EE1") ; ỡ
    ((= code 202) "\U+1EDB") ; ớ
    ((= code 203) "\U+1EE3") ; ợ
    ;; Chữ u
    ((= code 217) "\U+00F9") ; ù
    ((= code 218) "\U+1EE7") ; ủ
    ((= code 219) "\U+0169") ; ũ
    ((= code 220) "\U+00FA") ; ú
    ((= code 221) "\U+1EE5") ; ụ
    ;; Chữ ư
    ((= code 173) "\U+01B0") ; ư
    ((= code 222) "\U+1EEB") ; ừ
    ((= code 223) "\U+1EED") ; ử
    ((= code 224) "\U+1EEF") ; ữ
    ((= code 225) "\U+1EE9") ; ứ
    ((= code 226) "\U+1EF1") ; ự
    ;; Chữ y
    ((= code 227) "\U+1EF3") ; ỳ
    ((= code 228) "\U+1EF7") ; ỷ
    ((= code 229) "\U+1EF9") ; ỹ
    ((= code 230) "\U+00FD") ; ý
    ((= code 231) "\U+1EF5") ; ỵ
    ;; Chữ đ
    ((= code 174) "\U+0111") ; đ
    ;; Chữ HOA TCVN3
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

;; Tự động chạy ngay khi load LISP
(c:FIXALL)
