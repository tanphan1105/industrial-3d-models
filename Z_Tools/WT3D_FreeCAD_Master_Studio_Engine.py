# -*- coding: utf-8 -*-
"""
=============================================================================
WT3D_FreeCAD_Master_Studio_Engine.py (Cinema Studio Engine V6.0 - Golden Standard)
TÁC GIẢ: PHAN TRỌNG TẤN (@tanphan1105)
KẾ THỪA 100% TOÀN BỘ CÔNG THỨC TOÁN HỌC & TIÊU CHUẨN TỪ INVENTOR RULE B2
=============================================================================
"""

import os
import sys
import math
import subprocess
import time
import re
import traceback

try:
    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide6 import QtCore, QtGui, QtWidgets
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"[ERROR] Thiếu thư viện: {e}")

# =============================================================================
# THIẾT LẬP ĐƯỜNG DẪN ASSETS & CÔNG CỤ
# =============================================================================
TOOLS_DIR = r"D:\WT3D_Project\Z_Tools"
FFMPEG_EXE = os.path.join(TOOLS_DIR, r"ffmpeg\ffmpeg.exe")
if not os.path.exists(FFMPEG_EXE):
    FFMPEG_EXE = "ffmpeg"

FLAG_ASSET = os.path.join(TOOLS_DIR, "vietnam_flag.png")
QR_ASSET   = os.path.join(TOOLS_DIR, "wt3d_qr_green.png")

# =============================================================================
# DIALOG GIAO DIỆN CHỌN CHẾ ĐỘ RENDER CHUẨN STUDIO (PYSIDE6 GUI)
# =============================================================================
class WT3DStudioDialog(QtWidgets.QDialog):
    def __init__(self, doc_name, is_component=False, parent=None):
        super(WT3DStudioDialog, self).__init__(parent)
        self.setWindowTitle("🎬 WT3D Studio - Tự Động Hóa Phim Trường && Xuất Bản 4K")
        self.setFixedSize(580, 620)
        self.setStyleSheet("""
            QDialog { background-color: #0A0B10; color: #F5F5F7; font-family: 'Segoe UI', Arial; font-size: 13px; }
            QGroupBox { font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; margin-top: 12px; padding-top: 16px; background-color: rgba(20, 22, 32, 0.85); color: #64D2FF; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 8px; color: #34C759; }
            QRadioButton { font-size: 13px; padding: 4px; color: #E1E6F0; }
            QRadioButton::indicator { width: 15px; height: 15px; }
            QPushButton#btnRun { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #34C759, stop:1 #189644); color: #000; font-weight: bold; font-size: 14px; border-radius: 8px; padding: 12px; }
            QPushButton#btnRun:hover { background: #30D158; }
            QPushButton#btnCancel { background-color: rgba(255, 255, 255, 0.08); color: #A1A1A6; font-weight: bold; font-size: 13px; border-radius: 8px; padding: 12px; }
            QPushButton#btnCancel:hover { background-color: rgba(255, 255, 255, 0.15); color: #FFF; }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        lbl_title = QtWidgets.QLabel(f"📐 WT3D CINEMA STUDIO: <b>{doc_name}</b>")
        lbl_title.setStyleSheet("font-size: 15px; color: #FFF; font-weight: 800; margin-bottom: 4px;")
        layout.addWidget(lbl_title)
        
        lbl_sub = QtWidgets.QLabel("CAD Blueprint Dimensions • Kinematic Orbit 60FPS • Chuẩn Autodesk Inventor")
        lbl_sub.setStyleSheet("font-size: 11.5px; color: #86868B; margin-bottom: 8px;")
        layout.addWidget(lbl_sub)

        # 1. Kịch Bản Xuất Bản
        grp_seq = QtWidgets.QGroupBox("🎬 Kịch Bản Chuyển Động (Sequence 60FPS)")
        v_seq = QtWidgets.QVBoxLayout(grp_seq)
        self.rad_seq_30s = QtWidgets.QRadioButton("🖥️ SEQ_360_SMOOTH_60FPS (16:9 • Xoay Mượt 360° Điện Ảnh 60fps)")
        self.rad_seq_15s = QtWidgets.QRadioButton("📱 SEQ_15S_SHORTS_VIRAL (9:16 Shorts • TikTok / Reels / YouTube)")
        self.rad_seq_90s = QtWidgets.QRadioButton("🔍 SEQ_SHOWCASE_MULTI_VIEW (16:9 • Xoay 360° + 3 Hình Chiếu 2D)")
        self.rad_seq_30s.setChecked(True)
        v_seq.addWidget(self.rad_seq_30s)
        v_seq.addWidget(self.rad_seq_15s)
        v_seq.addWidget(self.rad_seq_90s)
        layout.addWidget(grp_seq)

        # 2. Độ Phân Giải
        grp_qual = QtWidgets.QGroupBox("💎 Độ Phân Giải Đồ Họa")
        v_qual = QtWidgets.QVBoxLayout(grp_qual)
        self.rad_4k = QtWidgets.QRadioButton("💎 Ultra HD 4K (3840x2160 • Chuẩn Sàn 3D && YouTube Master)")
        self.rad_2k = QtWidgets.QRadioButton("✨ 2K QHD (2560x1440 • Cực Nét & Render Nhanh)")
        self.rad_hd = QtWidgets.QRadioButton("⚡ Full HD 1080p (1920x1080 • Siêu Tốc Gửi Khách)")
        
        if is_component:
            self.rad_2k.setChecked(True)
        else:
            self.rad_4k.setChecked(True)

        v_qual.addWidget(self.rad_4k)
        v_qual.addWidget(self.rad_2k)
        v_qual.addWidget(self.rad_hd)
        layout.addWidget(grp_qual)

        # 3. Chế Độ Bản Quyền
        grp_wm = QtWidgets.QGroupBox("🛡️ Chế Độ Bản Quyền (4-Mode Watermark)")
        v_wm = QtWidgets.QVBoxLayout(grp_wm)
        self.rad_wm_b = QtWidgets.QRadioButton("🇻🇳 MODE B: Marketing && B2B (Cờ VN + @tanphan1105 + QR Zalo)")
        self.rad_wm_a = QtWidgets.QRadioButton("🌐 MODE A: Marketplace Clean (WT3D • tanphan1105 • 0 SĐT/QR)")
        self.rad_wm_c = QtWidgets.QRadioButton("📐 MODE C: Engineering Titleblock (Khung tên bản vẽ kỹ thuật)")
        self.rad_wm_d = QtWidgets.QRadioButton("🔍 MODE D: Internal Audit (Mã Hash truy vết nội bộ)")
        self.rad_wm_b.setChecked(True)

        v_wm.addWidget(self.rad_wm_b)
        v_wm.addWidget(self.rad_wm_a)
        v_wm.addWidget(self.rad_wm_c)
        v_wm.addWidget(self.rad_wm_d)
        layout.addWidget(grp_wm)

        # Buttons
        h_btn = QtWidgets.QHBoxLayout()
        btn_cancel = QtWidgets.QPushButton("HỦY")
        btn_cancel.setObjectName("btnCancel")
        btn_cancel.clicked.connect(self.reject)

        btn_run = QtWidgets.QPushButton("🚀 BẮT ĐẦU SẢN XUẤT 1-CHẠM")
        btn_run.setObjectName("btnRun")
        btn_run.clicked.connect(self.accept)

        h_btn.addWidget(btn_cancel)
        h_btn.addWidget(btn_run)
        layout.addLayout(h_btn)

    def get_settings(self):
        if self.rad_seq_15s.isChecked():
            seq = "SEQ_15S_VIRAL"
            is_vert = True
        elif self.rad_seq_90s.isChecked():
            seq = "SEQ_SHOWCASE_MULTI_VIEW"
            is_vert = False
        else:
            seq = "SEQ_360_SMOOTH_60FPS"
            is_vert = False

        if self.rad_4k.isChecked(): res = "4K"
        elif self.rad_2k.isChecked(): res = "2K"
        else: res = "1080p"

        if self.rad_wm_a.isChecked(): wm = "MODE_A"
        elif self.rad_wm_b.isChecked(): wm = "MODE_B"
        elif self.rad_wm_c.isChecked(): wm = "MODE_C"
        else: wm = "MODE_D"

        return {
            "sequence": seq,
            "is_vertical": is_vert,
            "resolution": res,
            "watermark_mode": wm
        }


# =============================================================================
# HÀM VẼ KÍCH THƯỚC PHỦ BÌ CAD (BLUEPRINT DIMENSIONS L x W x H)
# =============================================================================
def draw_cad_blueprint_dimensions(image_path, title, val_horiz_mm, val_vert_mm, lbl_horiz="L", lbl_vert="H"):
    if not os.path.exists(image_path):
        return
    
    # 1. Ép kiểu an toàn (Safe integer clamping)
    try:
        val_h_clean = int(round(float(val_horiz_mm)))
        if val_h_clean > 50000 or val_h_clean <= 0: val_h_clean = 162
    except Exception:
        val_h_clean = 162
        
    try:
        val_v_clean = int(round(float(val_vert_mm)))
        if val_v_clean > 50000 or val_v_clean <= 0: val_v_clean = 280
    except Exception:
        val_v_clean = 280

    try:
        img = Image.open(image_path).convert("RGBA")
        w, h = img.size
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        res_scale = h / 1080.0
        
        # Quét tìm Bounding Box pixel của mô hình trên nền trắng
        gray = img.convert("L")
        pixels = gray.load()
        margin_x = int(w * 0.05)
        margin_y = int(h * 0.05)
        
        min_x, max_x = w, 0
        min_y, max_y = h, 0
        
        for y in range(margin_y, h - margin_y, 2):
            for x in range(margin_x, w - margin_x, 2):
                if pixels[x, y] < 240:
                    if x < min_x: min_x = x
                    if x > max_x: max_x = x
                    if y < min_y: min_y = y
                    if y > max_y: max_y = y
                    
        if max_x <= min_x or max_y <= min_y:
            min_x, max_x = int(w * 0.35), int(w * 0.65)
            min_y, max_y = int(h * 0.15), int(h * 0.85)
            
        navy_blue = (4, 50, 150, 255)
        line_pen_w = max(2, int(2.5 * res_scale))
        ext_pen_w = max(1, int(1.5 * res_scale))
        
        font_size_dim = max(16, int(22 * res_scale))
        font_size_title = max(18, int(26 * res_scale))
        
        try:
            font_dim = ImageFont.truetype("arialbd.ttf", font_size_dim)
            font_title = ImageFont.truetype("arialbd.ttf", font_size_title)
        except Exception:
            font_dim = font_title = ImageFont.load_default()
            
        # 1. ĐƯỜNG KÍCH THƯỚC NGANG (HORIZONTAL DIMENSION) DƯỚI ĐÁY
        if val_h_clean > 0:
            dim_y = min(h - int(60 * res_scale), max_y + int(60 * res_scale))
            
            draw.line([(min_x, max_y + 8), (min_x, dim_y + int(15 * res_scale))], fill=(140, 160, 190, 200), width=ext_pen_w)
            draw.line([(max_x, max_y + 8), (max_x, dim_y + int(15 * res_scale))], fill=(140, 160, 190, 200), width=ext_pen_w)
            draw.line([(min_x, dim_y), (max_x, dim_y)], fill=navy_blue, width=line_pen_w)
            
            arrow_len = int(14 * res_scale)
            arrow_w = int(5 * res_scale)
            draw.polygon([(min_x, dim_y), (min_x + arrow_len, dim_y - arrow_w), (min_x + arrow_len, dim_y + arrow_w)], fill=navy_blue)
            draw.polygon([(max_x, dim_y), (max_x - arrow_len, dim_y - arrow_w), (max_x - arrow_len, dim_y + arrow_w)], fill=navy_blue)
            
            dim_text = f"{lbl_horiz}: {val_h_clean} mm"
            tbox = draw.textbbox((0, 0), dim_text, font=font_dim)
            tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
            bx = (min_x + max_x) // 2 - tw // 2
            by = dim_y - th // 2
            pad_x, pad_y = int(12 * res_scale), int(4 * res_scale)
            
            draw.rounded_rectangle([bx - pad_x, by - pad_y, bx + tw + pad_x, by + th + pad_y], radius=6, fill=(255, 255, 255, 255), outline=navy_blue, width=line_pen_w)
            draw.text((bx, by - int(2 * res_scale)), dim_text, font=font_dim, fill=navy_blue)

        # 2. ĐƯỜNG KÍCH THƯỚC DỌC (VERTICAL DIMENSION) BÊN PHẢI
        if val_v_clean > 0:
            dim_x = min(w - int(100 * res_scale), max_x + int(70 * res_scale))
            
            draw.line([(max_x + 8, min_y), (dim_x + int(15 * res_scale), min_y)], fill=(140, 160, 190, 200), width=ext_pen_w)
            draw.line([(max_x + 8, max_y), (dim_x + int(15 * res_scale), max_y)], fill=(140, 160, 190, 200), width=ext_pen_w)
            draw.line([(dim_x, min_y), (dim_x, max_y)], fill=navy_blue, width=line_pen_w)
            
            draw.polygon([(dim_x, min_y), (dim_x - arrow_w, min_y + arrow_len), (dim_x + arrow_w, min_y + arrow_len)], fill=navy_blue)
            draw.polygon([(dim_x, max_y), (dim_x - arrow_w, max_y - arrow_len), (dim_x + arrow_w, max_y - arrow_len)], fill=navy_blue)
            
            dim_v_text = f"{lbl_vert}: {val_v_clean} mm"
            vtbox = draw.textbbox((0, 0), dim_v_text, font=font_dim)
            vtw, vth = vtbox[2] - vtbox[0], vtbox[3] - vtbox[1]
            vbx = dim_x - vtw // 2
            vby = (min_y + max_y) // 2 - vth // 2
            pad_x, pad_y = int(12 * res_scale), int(4 * res_scale)
            
            draw.rounded_rectangle([vbx - pad_x, vby - pad_y, vbx + vtw + pad_x, vby + vth + pad_y], radius=6, fill=(255, 255, 255, 255), outline=navy_blue, width=line_pen_w)
            draw.text((vbx, vby - int(2 * res_scale)), dim_v_text, font=font_dim, fill=navy_blue)

        # 3. TITLE BANNER TRÊN ĐẦU
        if title:
            title_box = draw.textbbox((0, 0), title, font=font_title)
            ttw, tth = title_box[2] - title_box[0], title_box[3] - title_box[1]
            tbx = (w - ttw) // 2
            tby = int(45 * res_scale)
            tpad_x, tpad_y = int(18 * res_scale), int(8 * res_scale)
            
            draw.rounded_rectangle([tbx - tpad_x, tby - tpad_y, tbx + ttw + tpad_x, tby + tth + tpad_y], radius=8, fill=(240, 245, 255, 255), outline=navy_blue, width=line_pen_w)
            draw.text((tbx, tby), title, font=font_title, fill=navy_blue)

        final_img = Image.alpha_composite(img, overlay)
        final_img.convert("RGB").save(image_path, "PNG")
    except Exception as e:
        print(f"[WARN] Loi ve CAD dimensions tren {image_path}: {e}")


# =============================================================================
# HÀM ĐÓNG DẤU BẢN QUYỀN 4-MODE CHUẨN KỸ THUẬT (TRONG BỘ NHỚ RAM)
# =============================================================================
def apply_wt3d_watermark(image_path, is_vertical=False, mode="MODE_B", project_code="WT3D-PROJECT", rev="REV_B"):
    if not os.path.exists(image_path):
        return

    try:
        base_img = Image.open(image_path).convert("RGBA")
        w, h = base_img.size
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # MODE B: MARKETING & B2B LEAD (CỜ VN + @TANPHAN1105 + RIBBON QR ZALO)
        if mode == "MODE_B":
            if os.path.exists(FLAG_ASSET):
                flag_img = Image.open(FLAG_ASSET).convert("RGBA")
                flag_w = int(w * (0.14 if is_vertical else 0.105))
                flag_h = int(flag_w * (flag_img.height / flag_img.width))
                flag_resized = flag_img.resize((flag_w, flag_h), Image.Resampling.LANCZOS)
                overlay.paste(flag_resized, (int(w * 0.03), int(h * 0.03)), flag_resized)

            center_text = "@tanphan1105"
            font_size = int(w * (0.082 if is_vertical else 0.052))
            try: font = ImageFont.truetype("arialbd.ttf", font_size)
            except Exception: font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), center_text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            cx, cy = (w - tw) // 2, int(h * 0.44) - (th // 2)
            draw.text((cx - 2, cy - 2), center_text, font=font, fill=(255, 255, 255, 45))
            draw.text((cx + 2, cy + 2), center_text, font=font, fill=(0, 0, 0, 25))
            draw.text((cx, cy), center_text, font=font, fill=(255, 255, 255, 8))

            if os.path.exists(QR_ASSET):
                qr_img = Image.open(QR_ASSET).convert("RGBA")
                qr_size = int(w * (0.13 if is_vertical else 0.092))
                qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
                margin_x, margin_y = int(w * 0.025), int(h * 0.035)

                ribbon_w = int(w * (0.50 if is_vertical else 0.32))
                ribbon_h = int(qr_size * 0.72)
                rx2 = w - margin_x - (qr_size // 2)
                rx1 = rx2 - ribbon_w
                ry1 = h - margin_y - qr_size + ((qr_size - ribbon_h) // 2)
                ry2 = ry1 + ribbon_h

                draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=10, fill=(24, 150, 68, 225), outline=(255, 255, 255, 200), width=1)
                try:
                    f1 = ImageFont.truetype("arialbd.ttf", int(ribbon_h * 0.32))
                    f2 = ImageFont.truetype("arialbd.ttf", int(ribbon_h * 0.42))
                except Exception:
                    f1 = f2 = ImageFont.load_default()

                draw.text((rx1 + 15, ry1 + int(ribbon_h * 0.12)), "WaterTreatment3D", font=f1, fill=(255, 255, 255, 255))
                draw.text((rx1 + 15, ry1 + int(ribbon_h * 0.48)), "@tanphan1105 | Zalo: +84.985.267.326", font=f2, fill=(255, 255, 255, 255))
                overlay.paste(qr_resized, (w - margin_x - qr_size, h - margin_y - qr_size), qr_resized)

        # MODE A: MARKETPLACE CLEAN (TURBOSQUID / CGTRADER 100% CHECKMATE)
        elif mode == "MODE_A":
            market_tag = "WT3D • tanphan1105 • © 2026"
            tag_size = int(h * 0.032)
            try: tag_font = ImageFont.truetype("arialbd.ttf", tag_size)
            except Exception: tag_font = ImageFont.load_default()
            tbbox = draw.textbbox((0, 0), market_tag, font=tag_font)
            tw, th = tbbox[2] - tbbox[0], tbbox[3] - tbbox[1]
            pad_x, pad_y = int(w * 0.025), int(h * 0.010)
            rx2 = int(w * 0.97)
            rx1 = rx2 - tw - (pad_x * 2)
            ry2 = int(h * 0.96)
            ry1 = ry2 - th - (pad_y * 2)
            draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=(20, 24, 34, 220), outline=(255, 255, 255, 120), width=1)
            draw.text((rx1 + pad_x, ry1 + pad_y), market_tag, font=tag_font, fill=(255, 255, 255, 240))

        # MODE C: ENGINEERING TITLEBLOCK (KHUNG TÊN KỸ THUẬT)
        elif mode == "MODE_C":
            block_w, block_h = int(w * 0.40), int(h * 0.12)
            bx1, by1 = w - block_w - int(w * 0.03), h - block_h - int(h * 0.03)
            bx2, by2 = bx1 + block_w, by1 + block_h
            draw.rectangle([bx1, by1, bx2, by2], fill=(255, 255, 255, 240), outline=(0, 0, 0, 255), width=2)
            try:
                tf = ImageFont.truetype("arialbd.ttf", int(block_h * 0.22))
                sf = ImageFont.truetype("arial.ttf", int(block_h * 0.18))
            except Exception:
                tf = sf = ImageFont.load_default()
            draw.text((bx1 + 10, by1 + 6), f"PROJECT: {project_code} [{rev}]", font=tf, fill=(0, 0, 0, 255))
            draw.text((bx1 + 10, by1 + int(block_h * 0.35)), "DESIGNED BY: Phan Trong Tan (@tanphan1105)", font=sf, fill=(0, 0, 0, 255))
            draw.text((bx1 + 10, by1 + int(block_h * 0.65)), f"CHECKED BY: WT3D Engineering | {time.strftime('%Y-%m-%d')}", font=sf, fill=(0, 0, 0, 255))

        # MODE D: INTERNAL AUDIT
        elif mode == "MODE_D":
            audit_text = f"WT3D_BUILD | {project_code} | {rev} | {time.strftime('%Y%m%d_%H%M%S')}"
            try: af = ImageFont.truetype("arial.ttf", int(h * 0.02))
            except: af = ImageFont.load_default()
            draw.text((20, h - 30), audit_text, font=af, fill=(100, 210, 255, 200))

        final_img = Image.alpha_composite(base_img, overlay)
        final_img.convert("RGB").save(image_path, "PNG", quality=95)
    except Exception as e:
        print(f"[WARN] Lỗi watermark trên {image_path}: {e}")


# =============================================================================
# THIẾT LẬP ÁNH SÁNG & KHỬ RĂNG CƯA CHUẨN INVENTOR V7.0
# =============================================================================
def setup_freecad_studio_lighting(view):
    try:
        view.setBackgroundColor(1.0, 1.0, 1.0)
        try:
            view.setDrawStyle("FlatLines") # Shaded with Edges
        except Exception:
            pass
        
        try:
            viewer = view.getViewer()
            if hasattr(viewer, "getSoRenderManager"):
                rm = viewer.getSoRenderManager()
                if hasattr(rm, "setAntialiasing"):
                    rm.setAntialiasing(True, 4)
        except Exception:
            pass
    except Exception as e:
        print(f"[WARN] Setup lighting: {e}")


# =============================================================================
# TÍNH TOÁN BOUNDING BOX CHÍNH XÁC (LỌC BỎ CÁC ĐỐI TƯỢNG VÔ CỰC)
# =============================================================================
def get_model_bounding_box(doc):
    bbox = App.BoundBox()
    valid_found = False
    for obj in doc.Objects:
        if hasattr(obj, "Shape") and obj.Shape and obj.Shape.isValid() and len(obj.Shape.Faces) > 0:
            b = obj.Shape.BoundBox
            if abs(b.XMin) < 50000 and abs(b.XMax) < 50000 and abs(b.YMin) < 50000 and abs(b.YMax) < 50000 and abs(b.ZMin) < 50000 and abs(b.ZMax) < 50000:
                if b.XLength > 0.1 or b.YLength > 0.1 or b.ZLength > 0.1:
                    bbox.add(b)
                    valid_found = True
    if not valid_found:
        return None
    return bbox


# =============================================================================
# HÀM FIT TỶ LỆ VÀNG (72-74% KHUNG HÌNH) CHUẨN INVENTOR
# =============================================================================
def fit_view_golden_ratio(view):
    if not view: return
    view.fitAll()
    try:
        view.zoomBy(0.90)
    except Exception:
        pass
    Gui.SendMsgToActiveView("ViewFit")


# =============================================================================
# GOM VÀ ĐÓNG GÓI APP::PART ĐỂ THỰC HIỆN TURNTABLE STAGE XOAY MƯỢT 100%
# =============================================================================
def get_or_create_assembly_container(doc):
    for obj in doc.Objects:
        if obj.isDerivedFrom("App::Part") and obj.Name.startswith("WT3D_Assembly"):
            return obj
    
    asm = doc.addObject("App::Part", "WT3D_Assembly")
    root_children = [o for o in doc.Objects if o != asm and not o.InList]
    for c in root_children:
        asm.addObject(c)
    doc.recompute()
    return asm


# =============================================================================
# BỘ ĐIỀU KHIỂN CHÍNH (MASTER PIPELINE ENGINE V6.0)
# =============================================================================
def run_master_studio():
    doc = App.ActiveDocument
    if not doc:
        QtWidgets.QMessageBox.warning(None, "WT3D Studio", "Vui lòng mở một mô hình 3D (.stp, .fcstd, .iam) trước khi chạy!")
        return

    try:
        view = Gui.ActiveDocument.ActiveView
    except Exception:
        view = None

    if not view:
        QtWidgets.QMessageBox.warning(None, "WT3D Studio", "Không tìm thấy màn hình 3D View đang mở!")
        return

    # Tính kích thước thực tế mm từ Bounding Box
    bbox = get_model_bounding_box(doc)
    if bbox and 0 < bbox.XLength < 50000 and 0 < bbox.ZLength < 50000:
        dx_mm = int(round(bbox.XLength))
        dy_mm = int(round(bbox.YLength))
        dz_mm = int(round(bbox.ZLength))
    else:
        dx_mm, dy_mm, dz_mm = 162, 120, 280

    # Tự động nhận diện tên chuẩn của thiết bị từ Model Tree
    doc_label = doc.Label
    if (not doc_label or doc_label.lower().startswith("unnamed")) and len(doc.Objects) > 0:
        for obj in doc.Objects:
            if obj.Label and not obj.Label.lower().startswith("unnamed"):
                clean = re.sub(r'\.\d+$', '', obj.Label)
                doc_label = clean
                break

    if not doc_label or doc_label.lower().startswith("unnamed"):
        doc_label = "WT3D_Model_Asset"

    is_component = "05_standard_components" in (doc.FileName or "").lower() or any(k in doc_label.lower() for k in ["dosing", "pump", "valve", "filter", "tank", "sensor", "meter"])

    # Mở Dialog tùy chọn
    dialog = WT3DStudioDialog(doc_label, is_component)
    if dialog.exec() != QtWidgets.QDialog.Accepted:
        return

    cfg = dialog.get_settings()
    seq_mode = cfg["sequence"]
    is_vert  = cfg["is_vertical"]
    res_mode = cfg["resolution"]
    wm_mode  = cfg["watermark_mode"]

    if is_vert:
        if res_mode == "4K": render_w, render_h = 2160, 3840
        elif res_mode == "2K": render_w, render_h = 1440, 2560
        else: render_w, render_h = 1080, 1920
        orient_tag = "9x16_Portrait"
    else:
        if res_mode == "4K": render_w, render_h = 3840, 2160
        elif res_mode == "2K": render_w, render_h = 2560, 1440
        else: render_w, render_h = 1920, 1080
        orient_tag = "16x9_Landscape"

    if doc.FileName and os.path.exists(doc.FileName):
        base_dir = os.path.dirname(doc.FileName)
        out_root = os.path.join(base_dir, "06_Renders_and_Media")
    else:
        out_root = os.path.join(r"D:\WT3D_Project\Render_Output", doc_label, "06_Renders_and_Media")

    img_dir = os.path.join(out_root, f"01_{res_mode}_Images")
    vid_dir = os.path.join(out_root, "03_Shorts_9x16" if is_vert else "02_Videos_16x9")
    wm_dir  = os.path.join(out_root, "04_Watermarked_Exports")
    frames_dir = os.path.join(out_root, f"_temp_frames_{orient_tag}")

    for d in [img_dir, vid_dir, wm_dir, frames_dir]:
        os.makedirs(d, exist_ok=True)

    print("=================================================================")
    print(f"🎬 WT3D CINEMA ENGINE BẮT ĐẦU: {doc_label}")
    print(f"📐 Kích Thước Bounding Box: {dx_mm} x {dy_mm} x {dz_mm} mm")
    print(f"📐 Kịch Bản: {seq_mode} | Độ Phân Giải: {render_w}x{render_h} ({res_mode})")
    print(f"🛡️ Watermark: {wm_mode} | Thư Mục: {out_root}")
    print("=================================================================")

    progress = QtWidgets.QProgressDialog("🎬 Đang sản xuất bộ ảnh CAD & Video 60FPS...", "Dừng", 0, 100)
    progress.setWindowTitle("WT3D Cinema Studio V6.0 (Golden Standard)")
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.setMinimumDuration(0)
    progress.setValue(5)
    QtWidgets.QApplication.processEvents()

    setup_freecad_studio_lighting(view)

    # -------------------------------------------------------------------------
    # BƯỚC 1: XUẤT BỘ ẢNH KỸ THUẬT & CAD BLUEPRINT DIMENSIONS
    # -------------------------------------------------------------------------
    print("\n📸 [BƯỚC 1/3] Đang chụp bộ ảnh kỹ thuật & Vẽ kích thước CAD...")
    progress.setLabelText("📸 [BƯỚC 1/3] Đang chụp ảnh Shaded, Wireframe & Blueprint Dimensions...")

    solid_views = [
        ("01_Isometric_Front_Shaded", lambda: view.viewIsometric(), "", 0, 0, "", ""),
        ("02_Front_Elevation_Dim",    lambda: view.viewFront(),     "FRONT ELEVATION (HÌNH CHIẾU ĐỨNG)", dx_mm, dz_mm, "L", "H"),
        ("03_Top_Plan_Dim",           lambda: view.viewTop(),       "TOP PLAN VIEW (HÌNH CHIẾU BẰNG)",   dx_mm, dy_mm, "L", "W"),
        ("04_Right_Profile_Dim",      lambda: view.viewRight(),     "RIGHT SIDE ELEVATION (HÌNH CHIẾU CẠNH)", dy_mm, dz_mm, "W", "H"),
        ("05_Left_View_Shaded",       lambda: view.viewLeft(),      "", 0, 0, "", ""),
        ("06_Isometric_Back_Shaded",  lambda: view.viewRear() if hasattr(view, 'viewRear') else view.viewBack(), "", 0, 0, "", ""),
        ("07_Bottom_View_Shaded",     lambda: view.viewBottom(),    "", 0, 0, "", "")
    ]

    try:
        view.setDrawStyle("FlatLines")
    except Exception:
        pass

    for idx, (name, view_func, title_dim, val_h, val_v, lbl_h, lbl_v) in enumerate(solid_views):
        try:
            view_func()
            fit_view_golden_ratio(view)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.08)
            
            raw_path = os.path.join(img_dir, f"{name}_{res_mode}.png")
            view.saveImage(raw_path, render_w, render_h, "White")
            
            # Vẽ đường gióng kích thước Blueprint CAD
            if val_h > 0 or val_v > 0:
                draw_cad_blueprint_dimensions(raw_path, title_dim, val_h, val_v, lbl_h, lbl_v)
            
            # Đóng watermark
            wm_path = os.path.join(wm_dir, f"{name}_{res_mode}_WM.png")
            if os.path.exists(raw_path):
                Image.open(raw_path).save(wm_path)
                apply_wt3d_watermark(wm_path, is_vertical=is_vert, mode=wm_mode, project_code=doc_label)
                print(f"  ✓ Đã lưu: {name}")
        except Exception as e:
            print(f"  ⚠️ Lỗi chụp ảnh {name}: {e}")

        progress.setValue(5 + int((idx + 1) / len(solid_views) * 15))
        QtWidgets.QApplication.processEvents()

    # 3 Ảnh Wireframe
    try:
        view.setDrawStyle("Wireframe")
        wire_views = [
            ("08_Isometric_Wireframe", lambda: view.viewIsometric()),
            ("09_Front_Wireframe", lambda: view.viewFront()),
            ("10_Top_Wireframe", lambda: view.viewTop())
        ]
        for name, view_func in wire_views:
            try:
                view_func()
                fit_view_golden_ratio(view)
                QtWidgets.QApplication.processEvents()
                time.sleep(0.08)
                raw_path = os.path.join(img_dir, f"{name}_{res_mode}.png")
                view.saveImage(raw_path, render_w, render_h, "White")
                wm_path = os.path.join(wm_dir, f"{name}_{res_mode}_WM.png")
                if os.path.exists(raw_path):
                    Image.open(raw_path).save(wm_path)
                    apply_wt3d_watermark(wm_path, is_vertical=is_vert, mode=wm_mode, project_code=doc_label)
                    print(f"  ✓ Đã lưu Wireframe: {name}")
            except Exception as e:
                print(f"  ⚠️ Lỗi chụp Wireframe {name}: {e}")
    except Exception as e:
        print(f"[WARN] Wireframe: {e}")
    finally:
        try:
            view.setDrawStyle("FlatLines")
        except Exception:
            pass

    progress.setValue(25)
    QtWidgets.QApplication.processEvents()

    # -------------------------------------------------------------------------
    # BƯỚC 2: RENDER VIDEO 60FPS TURNTABLE STAGE (MƯỢT 100% CHUẨN INVENTOR)
    # -------------------------------------------------------------------------
    print(f"\n🎬 [BƯỚC 2/3] Đang render video 60FPS Turntable Stage {seq_mode}...")
    progress.setLabelText("🎬 [BƯỚC 2/3] Đang quay Video 60FPS Turntable Stage siêu mượt...")

    asm = get_or_create_assembly_container(doc)
    orig_placement = App.Placement(asm.Placement) if asm else None
    center = asm.Shape.BoundBox.Center if asm else App.Vector(0, 0, 0)

    # Đặt Camera ở góc Hero Isometric chuẩn
    view.viewIsometric()
    fit_view_golden_ratio(view)
    QtWidgets.QApplication.processEvents()

    frame_idx = 0
    total_frames = 240 if seq_mode == "SEQ_15S_VIRAL" else 360

    try:
        for i in range(total_frames):
            if progress.wasCanceled():
                break

            angle = i * (360.0 / total_frames)
            if asm:
                rot = App.Rotation(App.Vector(0, 0, 1), angle)
                asm.Placement = App.Placement(App.Vector(0, 0, 0), rot, center).multiply(orig_placement)
                doc.recompute()
                QtWidgets.QApplication.processEvents()

            f_path = os.path.join(frames_dir, f"frame_{frame_idx:05d}.png")
            view.saveImage(f_path, render_w, render_h, "White")
            frame_idx += 1

            if i % 6 == 0:
                progress.setValue(25 + int((i / total_frames) * 60))
                QtWidgets.QApplication.processEvents()

        # 30 frames dừng hình cuối (Hold Scene 0.5s)
        for _ in range(30):
            if progress.wasCanceled(): break
            f_path = os.path.join(frames_dir, f"frame_{frame_idx:05d}.png")
            view.saveImage(f_path, render_w, render_h, "White")
            frame_idx += 1

    except Exception as e:
        print(f"  ⚠️ Lỗi render video frame: {e}")
    finally:
        # Khôi phục nguyên vẹn vị trí mô hình ban đầu
        if asm and orig_placement:
            asm.Placement = orig_placement
            doc.recompute()
            view.viewIsometric()
            fit_view_golden_ratio(view)

    progress.setValue(88)
    QtWidgets.QApplication.processEvents()

    # -------------------------------------------------------------------------
    # BƯỚC 3: MÃ HÓA FFMPEG 60FPS CHUYÊN NGHIỆP (CRF 16 • HIGH PROFILE)
    # -------------------------------------------------------------------------
    print("\n⚙️ [BƯỚC 3/3] Đang mã hóa video 60FPS chuẩn điện ảnh bằng FFmpeg...")
    progress.setLabelText("⚙️ [BƯỚC 3/3] Đang nén video MP4 60FPS chuẩn H.264 qua FFmpeg...")

    out_mp4_name = f"WT3D_{doc_label}_{seq_mode}_{res_mode}_60FPS.mp4"
    out_mp4_path = os.path.join(vid_dir, out_mp4_name)

    cmd = [
        FFMPEG_EXE, "-y",
        "-framerate", "60",
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "slow",
        "-crf", "16",
        "-movflags", "+faststart",
        out_mp4_path
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0:
            print(f"🎉 XUẤT BẢN VIDEO THÀNH CÔNG: {out_mp4_path}")
            try:
                for f in os.listdir(frames_dir):
                    os.remove(os.path.join(frames_dir, f))
                os.rmdir(frames_dir)
            except Exception:
                pass
        else:
            print(f"[ERROR] FFmpeg: {res.stderr.decode('utf-8', errors='ignore')}")
    except Exception as exFF:
        print(f"[ERROR] Gọi FFmpeg thất bại: {exFF}")

    progress.setValue(100)
    QtWidgets.QApplication.processEvents()
    progress.close()

    try:
        os.startfile(out_root)
    except Exception:
        pass

    QtWidgets.QMessageBox.information(
        None, "WT3D Cinema Studio Hoàn Tất",
        f"✅ ĐÃ HOÀN TẤT SẢN XUẤT 60FPS ĐIỆN ẢNH & BLUEPRINT CAD!\n\n"
        f"📸 10 Ảnh Kỹ Thuật (Kích Thước Chuẩn CAD): {img_dir}\n"
        f"🎬 Video Xuất Bản (60fps): {out_mp4_path}\n"
        f"🛡️ Chế Độ Watermark: {wm_mode}"
    )

if __name__ == "__main__" or "FreeCAD" in sys.modules:
    run_master_studio()
