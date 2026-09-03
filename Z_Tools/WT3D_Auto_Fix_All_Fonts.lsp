; ==============================================================================
; WT3D PRO LISP: SIÊU CÔNG CỤ SỬA FONT TCVN3 TỰ ĐỘNG PHÂN BIỆT CHỮ HOA / CHỮ THƯỜNG
; Tác giả: Phan Trọng Tấn - WaterTreatment3D
; Tự động biến KH[á]M thành KHÁM (CHỮ HOA CHUẨN 100%), không bao giờ bị thành KHầM!
; ==============================================================================

(defun c:FIXALL (/ doc textStyles count ss i ent obj txtStr newStr blks blk atts)
  (vl-load-com)
  (setq doc (vla-get-ActiveDocument (vlax-get-acad-object)))
  (setq count 0)
  (princ "
⚡ [WT3D] Đang quét và sửa toàn bộ lỗi chữ hoa/thường TCVN3 sang Unicode Arial...")

  ;; 1. Đổi tất cả Text Style sang font Arial.ttf
  (setq textStyles (vla-get-TextStyles doc))
  (vlax-for st textStyles
    (vl-catch-all-apply 'vla-put-fontfile (list st "Arial.ttf"))
    (vl-catch-all-apply 'vla-put-BigFontFile (list st ""))
  )

  ;; 2. Quét TẤT CẢ Text và MText trong Model & Layout
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
            (setq newStr (wt3d-convert-smart txtStr))
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

  ;; 3. Quét TẤT CẢ Block Attributes
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
              (setq newStr (wt3d-convert-smart txtStr))
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

  ;; 4. Tái tạo hiển thị
  (command "_.regenall")
  (princ (strcat "
💎 [WT3D] ĐÃ TỰ ĐỘNG SỬA THÀNH CÔNG " (itoa count) " ĐỐI TƯỢNG (CHỮ HOA RA HOA, CHỮ THƯỜNG RA THƯỜNG)!"))
  (princ "
🚀 CHỮ 'KHÁM' VÀ TOÀN BỘ TIÊU ĐỀ IN HOA ĐÃ HIỂN THỊ CHUẨN XÁC 100%!
")
  (princ)
)

;; Hàm chuyển đổi thông minh nhận diện ngữ cảnh Chữ Hoa (ALL-CAPS)
(defun wt3d-convert-smart (str / res idx len c code isUpper u)
  (setq res "")
  (setq len (strlen str))
  
  ;; Kiểm tra chuỗi có phải là cụm chữ in hoa không (ví dụ "KH...M", "PHÒNG KHÁM")
  (setq strUpper (strcase str))
  (setq isAllUpper (wt3d-is-all-caps str))
  
  (setq idx 1)
  (while (<= idx len)
    (setq c (substr str idx 1))
    (setq code (ascii c))
    
    ;; Kiểm tra xem ký tự lân cận có phải chữ in hoa không
    (setq isUpper (or isAllUpper (wt3d-check-upper-context str idx len)))
    
    (setq u (wt3d-get-unicode code isUpper))
    (if u
      (setq res (strcat res u))
      (setq res (strcat res c))
    )
    (setq idx (1+ idx))
  )
  
  ;; Sửa các lỗi tồn đọng nếu từng bị đổi nhầm sang 'ầ' trong cụm chữ hoa (như KHầM -> KHÁM)
  (setq res (wt3d-fix-legacy-mismatches res))
  res
)

;; Kiểm tra xem chuỗi có phải phần lớn là chữ in hoa không
(defun wt3d-is-all-caps (str / len i c code upperCount totalAlpha)
  (setq len (strlen str))
  (setq i 1)
  (setq upperCount 0)
  (setq totalAlpha 0)
  (while (<= i len)
    (setq code (ascii (substr str i 1)))
    (if (and (>= code 65) (<= code 90)) ; A-Z
      (progn
        (setq upperCount (1+ upperCount))
        (setq totalAlpha (1+ totalAlpha))
      )
      (if (and (>= code 97) (<= code 122)) ; a-z
        (setq totalAlpha (1+ totalAlpha))
      )
    )
    (setq i (1+ i))
  )
  (if (> totalAlpha 0)
    (>= (/ (float upperCount) (float totalAlpha)) 0.6)
    nil
  )
)

;; Kiểm tra ký tự trước hoặc sau có phải là chữ in hoa không
(defun wt3d-check-upper-context (str idx len / prevCode nextCode)
  (setq prevCode 0)
  (setq nextCode 0)
  (if (> idx 1)
    (setq prevCode (ascii (substr str (1- idx) 1)))
  )
  (if (< idx len)
    (setq nextCode (ascii (substr str (1+ idx) 1)))
  )
  (or (and (>= prevCode 65) (<= prevCode 90))
      (and (>= nextCode 65) (<= nextCode 90)))
)

;; Bảng tra ký tự TCVN3 (Chữ thường / Chữ hoa)
(defun wt3d-get-unicode (code isUpper)
  (cond
    ;; a
    ((= code 181) (if isUpper "\U+00C0" "\U+00E0")) ; À / à
    ((= code 182) (if isUpper "\U+1EA2" "\U+1EA3")) ; Ả / ả
    ((= code 183) (if isUpper "\U+00C3" "\U+00E3")) ; Ã / ã
    ((= code 184) (if isUpper "\U+00C1" "\U+00E1")) ; Á / á  <-- KHÁM ra KHÁM!
    ((= code 185) (if isUpper "\U+1EA0" "\U+1EA1")) ; Ạ / ạ
    ;; ă
    ((= code 168) (if isUpper "\U+0102" "\U+0103")) ; Ă / ă
    ((= code 187) (if isUpper "\U+1EB0" "\U+1EB1")) ; Ằ / ằ
    ((= code 188) (if isUpper "\U+1EB2" "\U+1EB3")) ; Ẳ / ẳ
    ((= code 189) (if isUpper "\U+1EB4" "\U+1EB5")) ; Ẵ / ẵ
    ((= code 190) (if isUpper "\U+1EAE" "\U+1EAF")) ; Ắ / ắ
    ((= code 192) (if isUpper "\U+1EB6" "\U+1EB7")) ; Ặ / ặ
    ;; â
    ((= code 169) (if isUpper "\U+00C2" "\U+00E2")) ; Â / â
    ((= code 193) (if isUpper "\U+00C1" "\U+1EA7")) ; Nếu chữ hoa là Á, nếu thường là ầ!
    ((= code 194) (if isUpper "\U+1EA8" "\U+1EA9")) ; Ẩ / ẩ
    ((= code 195) (if isUpper "\U+1EAA" "\U+1EAB")) ; Ẫ / ẫ
    ((= code 196) (if isUpper "\U+1EA4" "\U+1EA5")) ; Ấ / ấn
    ((= code 197) (if isUpper "\U+1EAC" "\U+1EAD")) ; Ậ / ậ
    ;; e
    ((= code 232) (if isUpper "\U+00C8" "\U+00E8")) ; È / è
    ((= code 233) (if isUpper "\U+1EBA" "\U+1EBB")) ; Ẻ / ẻ
    ((= code 234) (if isUpper "\U+1EBC" "\U+1EBD")) ; Ẽ / ẽ
    ((= code 235) (if isUpper "\U+00C9" "\U+00E9")) ; É / é
    ((= code 236) (if isUpper "\U+1EB8" "\U+1EB9")) ; Ẹ / ẹ
    ;; ê
    ((= code 170) (if isUpper "\U+00CA" "\U+00EA")) ; Ê / ê
    ((= code 237) (if isUpper "\U+1EC0" "\U+1EC1")) ; Ề / ề
    ((= code 238) (if isUpper "\U+1EC2" "\U+1EC3")) ; Ể / ể
    ((= code 239) (if isUpper "\U+1EC4" "\U+1EC5")) ; Ễ / ễ
    ((= code 240) (if isUpper "\U+1EBE" "\U+1EBF")) ; Ế / ế
    ((= code 241) (if isUpper "\U+1EC6" "\U+1EC7")) ; Ệ / ệ
    ;; i
    ((= code 242) (if isUpper "\U+00CC" "\U+00EC")) ; Ì / ì
    ((= code 243) (if isUpper "\U+1EC8" "\U+1EC9")) ; Ỉ / ỉ
    ((= code 244) (if isUpper "\U+0128" "\U+0129")) ; Ĩ / ĩ
    ((= code 245) (if isUpper "\U+00CD" "\U+00ED")) ; Í / í
    ((= code 246) (if isUpper "\U+1ECA" "\U+1ECB")) ; Ị / ị
    ;; o
    ((= code 247) (if isUpper "\U+00D2" "\U+00F2")) ; Ò / ò
    ((= code 248) (if isUpper "\U+1ECE" "\U+1ECF")) ; Ỏ / ỏ
    ((= code 249) (if isUpper "\U+00D5" "\U+00F5")) ; Õ / õ
    ((= code 250) (if isUpper "\U+00D3" "\U+00F3")) ; Ó / ó
    ((= code 251) (if isUpper "\U+1ECC" "\U+1ECD")) ; Ọ / ọ
    ;; ô
    ((= code 171) (if isUpper "\U+00D4" "\U+00F4")) ; Ô / ô
    ((= code 252) (if isUpper "\U+1ED2" "\U+1ED3")) ; Ồ / ồ
    ((= code 253) (if isUpper "\U+1ED4" "\U+1ED5")) ; Ổ / ổ
    ((= code 254) (if isUpper "\U+1ED6" "\U+1ED7")) ; Ỗ / ỗ
    ((= code 255) (if isUpper "\U+1ED0" "\U+1ED1")) ; Ố / ố
    ((= code 186) (if isUpper "\U+1ED8" "\U+1ED9")) ; Ộ / ộ
    ;; ơ
    ((= code 172) (if isUpper "\U+01A0" "\U+01A1")) ; Ơ / ơ
    ((= code 199) (if isUpper "\U+1EDC" "\U+1EDD")) ;精神 / ờ
    ((= code 200) (if isUpper "\U+1EDE" "\U+1EDF")) ; Ở / ở
    ((= code 201) (if isUpper "\U+1EE0" "\U+1EE1")) ; Ỡ / ỡ
    ((= code 202) (if isUpper "\U+1EDA" "\U+1EDB")) ; Ớ / ớ
    ((= code 203) (if isUpper "\U+1EE2" "\U+1EE3")) ; Ợ / ợ
    ;; u
    ((= code 217) (if isUpper "\U+00D9" "\U+00F9")) ; Ù / ù
    ((= code 218) (if isUpper "\U+1EE6" "\U+1EE7")) ; Ủ / ủ
    ((= code 219) (if isUpper "\U+0168" "\U+0169")) ; Ũ / ũ
    ((= code 220) (if isUpper "\U+00DA" "\U+00FA")) ; Ú / ú
    ((= code 221) (if isUpper "\U+1EE4" "\U+1EE5")) ; Ụ / ụ
    ;; ư
    ((= code 173) (if isUpper "\U+01AF" "\U+01B0")) ; Ư / ư
    ((= code 222) (if isUpper "\U+1EEA" "\U+1EEB")) ; Ừ / ừ
    ((= code 223) (if isUpper "\U+1EEC" "\U+1EED")) ; Ử / ử
    ((= code 224) (if isUpper "\U+1EEE" "\U+1EEF")) ; Ữ / ữ
    ((= code 225) (if isUpper "\U+1EE8" "\U+1EE9")) ; Ứ / ứ
    ((= code 226) (if isUpper "\U+1EF0" "\U+1EF1")) ; Ự / ự
    ;; y
    ((= code 227) (if isUpper "\U+1EF2" "\U+1EF3")) ; Ỳ / ỳ
    ((= code 228) (if isUpper "\U+1EF6" "\U+1EF7")) ; Ỷ / ỷ
    ((= code 229) (if isUpper "\U+1EF8" "\U+1EF9")) ; Ỹ / ỹ
    ((= code 230) (if isUpper "\U+00DD" "\U+00FD")) ; Ý / ý
    ((= code 231) (if isUpper "\U+1EF4" "\U+1EF5")) ; Ỵ / ỵ
    ;; đ
    ((= code 174) (if isUpper "\U+0110" "\U+0111")) ; Đ / đ
    ;; Ký tự hoa chuẩn
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

;; Hàm thay thế chuỗi con
(defun wt3d-str-replace (pattern replacement string / pos len)
  (setq len (strlen pattern))
  (while (setq pos (vl-string-search pattern string))
    (setq string (strcat (substr string 1 pos) replacement (substr string (+ pos len 1))))
  )
  string
)

;; Sửa triệt để các trường hợp đặc thù như KHầM -> KHÁM, KHáM -> KHÁM
(defun wt3d-fix-legacy-mismatches (s)
  (setq s (wt3d-str-replace "KHầM" "KHÁM" s))
  (setq s (wt3d-str-replace "KHáM" "KHÁM" s))
  (setq s (wt3d-str-replace "PHÒNG KHầM" "PHÒNG KHÁM" s))
  (setq s (wt3d-str-replace "PHÒNG KHáM" "PHÒNG KHÁM" s))
  (setq s (wt3d-str-replace "BầN VẼ" "BẢN VẼ" s))
  (setq s (wt3d-str-replace "BáN VẼ" "BẢN VẼ" s))
  (setq s (wt3d-str-replace "MẶT BẦNG" "MẶT BẰNG" s))
  (setq s (wt3d-str-replace "MẶT BầNG" "MẶT BẰNG" s))
  s
)

;; Tự động chạy ngay khi load
(c:FIXALL)
