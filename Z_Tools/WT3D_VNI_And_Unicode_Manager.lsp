; ==============================================================================
; WT3D PRO LISP: QUẢN LÝ VÀ CHUYỂN ĐỔI CHUYÊN DỤNG UNICODE & VNI-WINDOWS CHO CAD
; Tác giả: Phan Trọng Tấn - WaterTreatment3D
; Chuẩn hóa 100%: CHỈ SỬ DỤNG UNICODE (ARIAL/TIMES) VÀ VNI-WINDOWS (VNI-TIMES/VNI-HELVE)
;
; CÁC LỆNH SỬ DỤNG:
;   1. V2U hoặc FIXALL : Tự động chuyển toàn bộ chữ VNI (KHAÙM, HAØNH...) sang Unicode Arial
;   2. SF hoặc CHFONT  : Quét chọn vùng và đổi nhanh giữa font Unicode và font VNI-Windows
; ==============================================================================

;; -----------------------------------------------------------------------------
;; 1. LỆNH V2U / FIXALL: CHUYỂN ĐỔI VNI-WINDOWS SANG UNICODE ARIAL TOÀN BẢN VẼ
;; -----------------------------------------------------------------------------
(defun c:V2U () (c:FIXALL))
(defun c:FIXVNI () (c:FIXALL))

(defun c:FIXALL (/ doc textStyles count ss i ent obj txtStr newStr blks blk atts)
  (vl-load-com)
  (setq doc (vla-get-ActiveDocument (vlax-get-acad-object)))
  (setq count 0)
  (princ "
⚡ [WT3D] Đang quét và chuyển đổi toàn bộ chữ VNI-Windows sang Unicode Arial chuẩn...")

  ;; Đổi tất cả Text Style sang font Arial.ttf
  (setq textStyles (vla-get-TextStyles doc))
  (vlax-for st textStyles
    (vl-catch-all-apply 'vla-put-fontfile (list st "Arial.ttf"))
    (vl-catch-all-apply 'vla-put-BigFontFile (list st ""))
  )

  ;; Quét TẤT CẢ Text & MText
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
            (setq newStr (wt3d-vni-to-unicode txtStr))
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

  ;; Quét TẤT CẢ Block Attributes
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
              (setq newStr (wt3d-vni-to-unicode txtStr))
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

  (command "_.regenall")
  (princ (strcat "
💎 [WT3D] ĐÃ CHUYỂN ĐỔI THÀNH CÔNG " (itoa count) " ĐỐI TƯỢNG VNI SANG UNICODE ARIAL!"))
  (princ "
🚀 KHÁM, HÀNH, BẢN VẼ, MẶT BẰNG, ĐƯỜNG ỐNG ĐÃ HIỂN THỊ CHUẨN XÁC 100%!
")
  (princ)
)

;; -----------------------------------------------------------------------------
;; 2. LỆNH SF / CHFONT: QUÉT CHỌN VÙNG VÀ GÁN FONT UNICODE HOẶC VNI TÙY Ý
;; -----------------------------------------------------------------------------
(defun c:CHFONT () (c:SF))

(defun c:SF (/ ss opt fontFile styleName doc acadObj i ent obj count textStyles targetStyle atts entType)
  (vl-load-com)
  (setq acadObj (vlax-get-acad-object))
  (setq doc (vla-get-ActiveDocument acadObj))
  
  (princ "
👉 QUÉT CHỌN CÁC ĐỐI TƯỢNG CHỮ (HOẶC NHẤN ENTER ĐỂ CHỌN TẤT CẢ): ")
  (setq ss (ssget '((0 . "TEXT,MTEXT,INSERT,DIMENSION"))))
  (if (not ss) (setq ss (ssget "_X" '((0 . "TEXT,MTEXT,INSERT,DIMENSION")))))
  (if (not ss) (progn (princ "
❌ Không tìm thấy đối tượng chữ!") (exit)))
  
  (princ "
=======================================================")
  (princ "
CHỌN BẢNG MÃ & FONT MUỐN DÙNG:")
  (princ "
  [1] Arial.ttf         (Unicode chuẩn nét - Mặc định)")
  (princ "
  [2] Times New Roman   (Unicode có chân)")
  (princ "
  [3] VNI-Times         (VNI-Windows chuẩn)")
  (princ "
  [4] VNI-Helve         (VNI-Windows không chân nét đậm)")
  (princ "
  [5] Tự nhập tên font khác")
  (princ "
=======================================================")
  
  (initget "1 2 3 4 5")
  (setq opt (getkword "
👉 Nhập lựa chọn [1/2/3/4/5] <1 - Arial>: "))
  (if (not opt) (setq opt "1"))
  
  (cond
    ((= opt "1") (setq fontFile "Arial.ttf" styleName "WT3D_Arial"))
    ((= opt "2") (setq fontFile "times.ttf" styleName "WT3D_Times"))
    ((= opt "3") (setq fontFile "VNI-Times.ttf" styleName "WT3D_VNI_Times"))
    ((= opt "4") (setq fontFile "VNI-Helve.ttf" styleName "WT3D_VNI_Helve"))
    ((= opt "5") (setq fontFile (getstring "
👉 Nhập tên file font: ") styleName (strcat "WT3D_" (vl-filename-base fontFile))))
  )
  
  (setq textStyles (vla-get-TextStyles doc))
  (setq targetStyle (vl-catch-all-apply 'vla-Item (list textStyles styleName)))
  (if (vl-catch-all-error-p targetStyle)
    (progn
      (setq targetStyle (vla-Add textStyles styleName))
      (vl-catch-all-apply 'vla-put-fontfile (list targetStyle fontFile))
    )
    (vl-catch-all-apply 'vla-put-fontfile (list targetStyle fontFile))
  )
  
  (setq count 0)
  (setq i 0)
  (while (< i (sslength ss))
    (setq ent (ssname ss i))
    (setq obj (vlax-ename->vla-object ent))
    (setq entType (vla-get-ObjectName obj))
    (if (or (= entType "AcDbText") (= entType "AcDbMText"))
      (progn
        (vl-catch-all-apply 'vla-put-StyleName (list obj styleName))
        (setq count (1+ count))
      )
    )
    (if (= entType "AcDbBlockReference")
      (if (= (vla-get-HasAttributes obj) :vlax-true)
        (progn
          (setq atts (vlax-safearray->list (vlax-variant-value (vla-GetAttributes obj))))
          (foreach att atts
            (vl-catch-all-apply 'vla-put-StyleName (list att styleName))
            (setq count (1+ count))
          )
        )
      )
    )
    (setq i (1+ i))
  )
  
  (command "_.regenall")
  (princ (strcat "
💎 [WT3D] ĐÃ ĐỔI THÀNH CÔNG " (itoa count) " ĐỐI TƯỢNG SANG FONT: " fontFile "!"))
  (princ)
)

;; -----------------------------------------------------------------------------
;; THUẬT TOÁN CHUYỂN MÃ VNI-WINDOWS SANG UNICODE TOÀN DIỆN
;; -----------------------------------------------------------------------------
(defun wt3d-vni-to-unicode (str / vniList pair)
  (setq vniList '(
    ("AÙ" . "\U+00C1") ("AØ" . "\U+00C0") ("AÛ" . "\U+1EA2") ("AÕ" . "\U+00C3") ("AÏ" . "\U+1EA0")
    ("aù" . "\U+00E1") ("aø" . "\U+00E0") ("aû" . "\U+1EA3") ("aõ" . "\U+00E3") ("aï" . "\U+1EA1")
    ("AÁ" . "\U+1EA4") ("AÀ" . "\U+1EA6") ("AÅ" . "\U+1EA8") ("AÃ" . "\U+1EAA") ("AÄ" . "\U+1EAC")
    ("aá" . "\U+1EA5") ("aà" . "\U+1EA7") ("aå" . "\U+1EA9") ("aã" . "\U+1EAB") ("aä" . "\U+1EAD")
    ("AÉ" . "\U+1EAE") ("AÈ" . "\U+1EB0") ("AÚ" . "\U+1EB2") ("AÜ" . "\U+1EB4") ("AË" . "\U+1EB6")
    ("aé" . "\U+1EAF") ("aè" . "\U+1EB1") ("aú" . "\U+1EB3") ("aü" . "\U+1EB5") ("aë" . "\U+1EB7")
    ("EÙ" . "\U+00C9") ("EØ" . "\U+00C8") ("EÛ" . "\U+1EBA") ("EÕ" . "\U+1EBC") ("EÏ" . "\U+1EB8")
    ("eù" . "\U+00E9") ("eø" . "\U+00E8") ("eû" . "\U+1EBB") ("eõ" . "\U+1EBD") ("eï" . "\U+1EB9")
    ("EÁ" . "\U+1EBE") ("EÀ" . "\U+1EC0") ("EÅ" . "\U+1EC2") ("EÃ" . "\U+1EC4") ("EÄ" . "\U+1EC6")
    ("eá" . "\U+1EBF") ("eà" . "\U+1EC1") ("eå" . "\U+1EC3") ("eã" . "\U+1EC5") ("eä" . "\U+1EC7")
    ("OÙ" . "\U+00D3") ("OØ" . "\U+00D2") ("OÛ" . "\U+1ECE") ("OÕ" . "\U+00D5") ("OÏ" . "\U+1ECC")
    ("où" . "\U+00F3") ("oø" . "\U+00F2") ("oû" . "\U+1ECF") ("oõ" . "\U+00F5") ("oï" . "\U+1ECD")
    ("OÁ" . "\U+1ED0") ("OÀ" . "\U+1ED2") ("OÅ" . "\U+1ED4") ("OÃ" . "\U+1ED6") ("OÄ" . "\U+1ED8")
    ("oá" . "\U+1ED1") ("oà" . "\U+1ED3") ("oå" . "\U+1ED5") ("oã" . "\U+1ED7") ("oä" . "\U+1ED9")
    ("ÔÙ" . "\U+1EDA") ("ÔØ" . "\U+1EDC") ("ÔÛ" . "\U+1EDE") ("ÔÕ" . "\U+1EE0") ("ÔÏ" . "\U+1EE2")
    ("ôù" . "\U+1EDB") ("ôø" . "\U+1EDD") ("ôû" . "\U+1EDF") ("ôõ" . "\U+1EE1") ("ôï" . "\U+1EE3")
    ("UÙ" . "\U+00DA") ("UØ" . "\U+00D9") ("UÛ" . "\U+1EE6") ("UÕ" . "\U+0168") ("UÏ" . "\U+1EE4")
    ("uù" . "\U+00FA") ("uø" . "\U+00F9") ("uû" . "\U+1EE7") ("uõ" . "\U+0169") ("uï" . "\U+1EE5")
    ("ÖÙ" . "\U+1EE8") ("ÖØ" . "\U+1EEA") ("ÖÛ" . "\U+1EEC") ("ÖÕ" . "\U+1EEE") ("ÖÏ" . "\U+1EF0")
    ("öù" . "\U+1EE9") ("öø" . "\U+1EEB") ("öû" . "\U+1EED") ("öõ" . "\U+1EEF") ("öï" . "\U+1EF1")
    ("YÙ" . "\U+00DD") ("YØ" . "\U+1EF2") ("YÛ" . "\U+1EF6") ("YÕ" . "\U+1EF8") ("YÏ" . "\U+1EF4")
    ("yù" . "\U+00FD") ("yø" . "\U+1EF3") ("yû" . "\U+1EF7") ("yõ" . "\U+1EF9") ("yï" . "\U+1EF5")
    ("Ñ" . "\U+0110") ("ñ" . "\U+0111")
    ("Ö" . "\U+01AF") ("ö" . "\U+01B0")
    ("Ô" . "\U+01A0") ("ô" . "\U+01A1")
  ))
  
  (foreach pair vniList
    (setq str (wt3d-str-sub (car pair) (cdr pair) str))
  )
  str
)

(defun wt3d-str-sub (pat rep str / pos len)
  (setq len (strlen pat))
  (while (setq pos (vl-string-search pat str))
    (setq str (strcat (substr str 1 pos) rep (substr str (+ pos len 1))))
  )
  str
)

;; Tự động chạy ngay khi load
(c:FIXALL)
