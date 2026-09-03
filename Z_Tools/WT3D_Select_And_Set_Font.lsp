; ==============================================================================
; WT3D PRO LISP: QUÉT CHỌN VÙNG BẢN VẼ VÀ ĐỔI FONT TÙY Ý (INTERACTIVE FONT CHANGER)
; Tác giả: Phan Trọng Tấn - WaterTreatment3D
; Lệnh: CHFONT hoặc SF (Set Font)
; ==============================================================================

(defun c:CHFONT () (c:SF))

(defun c:SF (/ ss opt fontFile styleName doc acadObj i ent obj count)
  (vl-load-com)
  (setq acadObj (vlax-get-acad-object))
  (setq doc (vla-get-ActiveDocument acadObj))
  
  (princ "
=======================================================")
  (princ "
👉 QUÉT CHỌN CÁC ĐỐI TƯỢNG CHỮ TRÊN BẢN VẼ (HOẶC NHẤN ENTER ĐỂ CHỌN TẤT CẢ): ")
  (setq ss (ssget '((0 . "TEXT,MTEXT,INSERT,DIMENSION"))))
  
  (if (not ss)
    (progn
      (princ "
-> Đang chọn toàn bộ đối tượng chữ trong bản vẽ...")
      (setq ss (ssget "_X" '((0 . "TEXT,MTEXT,INSERT,DIMENSION"))))
    )
  )
  
  (if (not ss)
    (progn
      (princ "
❌ Không tìm thấy đối tượng chữ nào trong bản vẽ!")
      (exit)
    )
  )
  
  (princ (strcat "
🎯 Đã chọn " (itoa (sslength ss)) " đối tượng."))
  (princ "
-------------------------------------------------------")
  (princ "
CHỌN FONT BẠN MUỐN GÁN:")
  (princ "
  [1] Arial.ttf           (Font Unicode chuẩn đẹp, rõ nét)")
  (princ "
  [2] Times New Roman     (Font Unicode có chân chuẩn văn bản)")
  (princ "
  [3] .VnTime             (Font TCVN3 ABC TrueType)")
  (princ "
  [4] vntime.shx          (Font đơn nét CAD TCVN3 truyền thống)")
  (princ "
  [5] Tự nhập tên font khác (.ttf hoặc .shx)")
  (princ "
-------------------------------------------------------")
  
  (initget "1 2 3 4 5")
  (setq opt (getkword "
👉 Nhập lựa chọn [1/2/3/4/5] <1 - Arial>: "))
  (if (not opt) (setq opt "1"))
  
  (cond
    ((= opt "1")
      (setq fontFile "Arial.ttf")
      (setq styleName "WT3D_Arial")
    )
    ((= opt "2")
      (setq fontFile "times.ttf")
      (setq styleName "WT3D_Times")
    )
    ((= opt "3")
      (setq fontFile ".VnTime")
      (setq styleName "WT3D_VnTime")
    )
    ((= opt "4")
      (setq fontFile "vntime.shx")
      (setq styleName "WT3D_VnTimeSHX")
    )
    ((= opt "5")
      (setq fontFile (getstring "
👉 Nhập tên file font (ví dụ: Tahoma.ttf hoặc romans.shx): "))
      (setq styleName (strcat "WT3D_" (vl-filename-base fontFile)))
    )
  )
  
  ;; Tạo hoặc lấy TextStyle tương ứng
  (setq textStyles (vla-get-TextStyles doc))
  (setq targetStyle (vl-catch-all-apply 'vla-Item (list textStyles styleName)))
  (if (vl-catch-all-error-p targetStyle)
    (progn
      (setq targetStyle (vla-Add textStyles styleName))
      (vl-catch-all-apply 'vla-put-fontfile (list targetStyle fontFile))
      (if (vl-string-search ".shx" (strcase fontFile))
        (vl-catch-all-apply 'vla-put-BigFontFile (list targetStyle ""))
      )
    )
    (progn
      (vl-catch-all-apply 'vla-put-fontfile (list targetStyle fontFile))
    )
  )
  
  (princ (strcat "
⚡ Đang gán font [" fontFile "] cho các đối tượng đã chọn..."))
  
  (setq count 0)
  (setq i 0)
  (while (< i (sslength ss))
    (setq ent (ssname ss i))
    (setq obj (vlax-ename->vla-object ent))
    (setq entType (vla-get-ObjectName obj))
    
    ;; Xử lý Text & MText
    (if (or (= entType "AcDbText") (= entType "AcDbMText"))
      (progn
        (vl-catch-all-apply 'vla-put-StyleName (list obj styleName))
        (setq count (1+ count))
      )
    )
    
    ;; Xử lý Block Attributes
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
  (princ "
🚀 HOÀN TẤT TRONG 1 GIÂY!
")
  (princ)
)
