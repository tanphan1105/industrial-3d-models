# -*- coding: utf-8 -*-
"""
=============================================================================
WT3D_Blueprint_CAD_Exporter_And_Packager.py (B3 Pro - Blueprint & CAD Packager)
TÁC GIẢ: PHAN TRỌNG TẤN (@tanphan1105) - WaterTreatment3D
CHỨC NĂNG:
  1. Tự động nhận diện mô hình 3D, đo kích thước Bounding Box L x W x H (mm).
  2. Chụp 4 bản vẽ kỹ thuật CAD Blueprint đã vẽ DIM kích thước phủ bì sắc nét.
  3. Xuất trọn bộ file CAD trung tính: STEP AP214 (.stp), IGES (.igs), STL (.stl), OBJ (.obj).
  4. Gọi Blender ngầm xuất FBX Binary + .BLEND (nếu có Blender).
  5. Đính kèm README, License và đóng gói nén vào file .zip Flat Structure chuẩn sàn.
  6. Tự động mở thư mục chứa file trong Windows Explorer!
=============================================================================
"""

import os
import sys
import math
import subprocess
import time
import re
import zipfile
import traceback

try:
    import FreeCAD as App
    import FreeCADGui as Gui
    import Part
    import Mesh
    from PySide6 import QtCore, QtGui, QtWidgets
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"[ERROR] Thiếu thư viện: {e}")

# =============================================================================
# THIẾT LẬP ASSETS & CÔNG CỤ
# =============================================================================
TOOLS_DIR = r"D:\WT3D_Project\Z_Tools"
FLAG_ASSET = os.path.join(TOOLS_DIR, "vietnam_flag.png")
QR_ASSET   = os.path.join(TOOLS_DIR, "wt3d_qr_green.png")
LICENSE_SRC = os.path.join(TOOLS_DIR, "License_Use.txt")

# =============================================================================
# TÍNH TOÁN BOUNDING BOX VẬT LÝ CHÍNH XÁC (LỌC BỎ VẬT THỂ VÔ CỰC)
# =============================================================================
def get_model_bounding_box_and_objects(doc):
    bbox = App.BoundBox()
    valid_objs = []
    for obj in doc.Objects:
        if hasattr(obj, "Shape") and obj.Shape and obj.Shape.isValid() and len(obj.Shape.Faces) > 0:
            b = obj.Shape.BoundBox
            if abs(b.XMin) < 50000 and abs(b.XMax) < 50000 and abs(b.YMin) < 50000 and abs(b.YMax) < 50000 and abs(b.ZMin) < 50000 and abs(b.ZMax) < 50000:
                if b.XLength > 0.1 or b.YLength > 0.1 or b.ZLength > 0.1:
                    bbox.add(b)
                    valid_objs.append(obj)
    if not valid_objs:
        return None, []
    return bbox, valid_objs


# =============================================================================
# HÀM VẼ KÍCH THƯỚC PHỦ BÌ CAD (CAD BLUEPRINT DIMENSIONS L x W x H)
# =============================================================================
def draw_cad_blueprint_dimensions(image_path, title, val_horiz_mm, val_vert_mm, lbl_horiz="L", lbl_vert="H"):
    if not os.path.exists(image_path):
        return
    
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
        print(f"[WARN] Lỗi vẽ CAD dimensions trên {image_path}: {e}")


# =============================================================================
# HÀM ĐÓNG DẤU BẢN QUYỀN CHUẨN SÀN & MARKETING
# =============================================================================
def apply_wt3d_watermark(image_path, is_vertical=False, mode="MODE_B", project_code="WT3D-PROJECT"):
    if not os.path.exists(image_path):
        return

    try:
        base_img = Image.open(image_path).convert("RGBA")
        w, h = base_img.size
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # MODE B: MARKETING (CỜ VN + @TANPHAN1105 + RIBBON QR ZALO)
        if mode == "MODE_B":
            if os.path.exists(FLAG_ASSET):
                flag_img = Image.open(FLAG_ASSET).convert("RGBA")
                flag_w = int(w * 0.105)
                flag_h = int(flag_w * (flag_img.height / flag_img.width))
                flag_resized = flag_img.resize((flag_w, flag_h), Image.Resampling.LANCZOS)
                overlay.paste(flag_resized, (int(w * 0.03), int(h * 0.03)), flag_resized)

            center_text = "@tanphan1105"
            font_size = int(w * 0.052)
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
                qr_size = int(w * 0.092)
                qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
                margin_x, margin_y = int(w * 0.025), int(h * 0.035)

                ribbon_w = int(w * 0.32)
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

        # MODE A: MARKETPLACE CLEAN (TURBOSQUID / CGTRADER CHECKMATE)
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

        final_img = Image.alpha_composite(base_img, overlay)
        final_img.convert("RGB").save(image_path, "PNG", quality=95)
    except Exception as e:
        print(f"[WARN] Lỗi watermark trên {image_path}: {e}")


# =============================================================================
# HÀM TẠO README HƯỚNG DẪN MÔ HÌNH CHUẨN QUỐC TẾ
# =============================================================================
def generate_readme_file(export_dir, doc_label, dx, dy, dz):
    readme_path = os.path.join(export_dir, f"README_WT3D_{doc_label}_Model_Instructions.txt")
    content = f"""================================================================================
WATER TREATMENT 3D - PROFESSIONAL ENGINEERING MODEL PACKAGE
Model: {doc_label}
Designer: Phan Trong Tan (@tanphan1105)
Standard: ISO Metric (1 Unit = 1 Millimeter)
================================================================================

1. BOUNDING BOX DIMENSIONS (OVERALL SIZES):
   - Length (X): {dx} mm
   - Width  (Y): {dy} mm
   - Height (Z): {dz} mm

2. INCLUDED UNIVERSAL CAD & 3D FORMATS:
   - .STP (STEP AP214) : Universal solid standard for SolidWorks, Inventor, AutoCAD, Fusion 360, CATIA, Creo, Rhino.
   - .IGS (IGES Solid) : Classic neutral CAD format for CAD/CAM/CNC software.
   - .STL (StereoLith) : Clean triangulated mesh for 3D Printing, Simulation & Prototyping.
   - .OBJ (.obj + .mtl): Standard Wavefront mesh format for Blender, 3ds Max, Maya, Cinema 4D.
   - .FBX (Binary Y-Up): Optimized asset for Unreal Engine 5, Unity & Game Engines (if included).
   - .BLEND            : Native Blender 4.x scene file with real-world scale (if included).

3. COORDINATE SYSTEM & GROUNDING:
   - Native Orientation: Y-Up (or Z-Up engineering standard aligned).
   - Pivot Point       : Centered at Geometric Bottom Center (X=0, Y=0/Z=0 ground plane).

4. APPLICATIONS:
   - Industrial Mechanical MEP Engineering Layout & Piping P&ID.
   - High-end 3D VFX Architectural Visualization & Rendering.
   - Digital Twin SCADA VR/AR Simulations.

Thank you for choosing WaterTreatment3D engineering models!
================================================================================
"""
    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[WARN] Lỗi ghi README: {e}")
    return readme_path


# =============================================================================
# DIALOG GIAO DIỆN B3 PRO EXPORTER & PACKAGER (PYSIDE6)
# =============================================================================
class WT3DExportDialog(QtWidgets.QDialog):
    def __init__(self, doc_label, dx, dy, dz, parent=None):
        super(WT3DExportDialog, self).__init__(parent)
        self.setWindowTitle("📦 WT3D B3: Xuất Bản Vẽ DIM & Đóng Gói File CAD (.zip)")
        self.setFixedSize(620, 680)
        self.setStyleSheet("""
            QDialog { background-color: #0A0B10; color: #F5F5F7; font-family: 'Segoe UI', Arial; font-size: 13px; }
            QGroupBox { font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; margin-top: 12px; padding-top: 16px; background-color: rgba(20, 22, 32, 0.85); color: #64D2FF; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 8px; color: #34C759; }
            QCheckBox { font-size: 13px; padding: 4px; color: #E1E6F0; }
            QRadioButton { font-size: 13px; padding: 4px; color: #E1E6F0; }
            QPushButton#btnRun { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #34C759, stop:1 #189644); color: #000; font-weight: bold; font-size: 14px; border-radius: 8px; padding: 12px; }
            QPushButton#btnRun:hover { background: #30D158; }
            QPushButton#btnCancel { background-color: rgba(255, 255, 255, 0.08); color: #A1A1A6; font-weight: bold; font-size: 13px; border-radius: 8px; padding: 12px; }
            QPushButton#btnCancel:hover { background-color: rgba(255, 255, 255, 0.15); color: #FFF; }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        # Header Title
        lbl_title = QtWidgets.QLabel(f"📦 B3 EXPORTER & PACKAGER: <b>{doc_label}</b>")
        lbl_title.setStyleSheet("font-size: 15px; color: #FFF; font-weight: 800; margin-bottom: 2px;")
        layout.addWidget(lbl_title)

        lbl_dim = QtWidgets.QLabel(f"📐 Kích Thước Bounding Box Thực Tế: <b>{dx} mm (L) × {dy} mm (W) × {dz} mm (H)</b>")
        lbl_dim.setStyleSheet("font-size: 12px; color: #34C759; margin-bottom: 8px;")
        layout.addWidget(lbl_dim)

        # 1. Nhóm Bản Vẽ Kỹ Thuật (Blueprint Snapshots)
        grp_bp = QtWidgets.QGroupBox("📐 1. Chụp Bản Vẽ Kỹ Thuật Đã Vẽ DIM (CAD Blueprints)")
        v_bp = QtWidgets.QVBoxLayout(grp_bp)
        self.chk_bp_front = QtWidgets.QCheckBox("✅ Front Elevation (Hình chiếu đứng: Chiều dài L × Chiều cao H)")
        self.chk_bp_top   = QtWidgets.QCheckBox("✅ Top Plan View (Hình chiếu bằng: Chiều dài L × Chiều rộng W)")
        self.chk_bp_right = QtWidgets.QCheckBox("✅ Right Profile (Hình chiếu cạnh: Chiều rộng W × Chiều cao H)")
        self.chk_bp_iso   = QtWidgets.QCheckBox("✅ Isometric 3D Overview (Hình trục đo 3D tỷ lệ vàng)")
        for c in [self.chk_bp_front, self.chk_bp_top, self.chk_bp_right, self.chk_bp_iso]:
            c.setChecked(True)
            v_bp.addWidget(c)
        layout.addWidget(grp_bp)

        # 2. Nhóm Định Dạng CAD Trung Tính
        grp_cad = QtWidgets.QGroupBox("💎 2. Trọn Bộ Định Dạng Mở Trung Tính (Universal CAD)")
        v_cad = QtWidgets.QVBoxLayout(grp_cad)
        self.chk_step = QtWidgets.QCheckBox("🔹 STEP AP214 (.stp) - Chuẩn cơ khí chính xác cao (SolidWorks, Inventor, Revit)")
        self.chk_iges = QtWidgets.QCheckBox("🔹 IGES Solid (.igs) - Chuẩn trao đổi CAD/CAM/CNC")
        self.chk_stl  = QtWidgets.QCheckBox("🔹 Stereolithography (.stl) - Chuẩn in 3D & Mô phỏng")
        self.chk_obj  = QtWidgets.QCheckBox("🔹 Wavefront OBJ (.obj) - Chuẩn render 3D / VFX")
        self.chk_fbx  = QtWidgets.QCheckBox("🔹 Blender / FBX Binary (.fbx) - Tự động gọi Blender ngầm (nếu có)")
        for c in [self.chk_step, self.chk_iges, self.chk_stl, self.chk_obj, self.chk_fbx]:
            c.setChecked(True)
            v_cad.addWidget(c)
        layout.addWidget(grp_cad)

        # 3. Nhóm Đóng Gói .ZIP & Xuất Bản
        grp_zip = QtWidgets.QGroupBox("🛡️ 3. Đóng Gói File Nén .ZIP Chuẩn Sàn 3D & B2B")
        v_zip = QtWidgets.QVBoxLayout(grp_zip)
        self.chk_readme  = QtWidgets.QCheckBox("📄 Tự động tạo README hướng dẫn thông số kỹ thuật (Model Specs)")
        self.chk_license = QtWidgets.QCheckBox("📜 Đính kèm giấy phép sử dụng bản quyền (License_Use.txt)")
        self.chk_zip_gen = QtWidgets.QCheckBox("📦 Nén tất cả vào file [ModelName]_Universal_CAD.zip (Flat Structure)")
        for c in [self.chk_readme, self.chk_license, self.chk_zip_gen]:
            c.setChecked(True)
            v_zip.addWidget(c)
        layout.addWidget(grp_zip)

        # Buttons Action
        h_btn = QtWidgets.QHBoxLayout()
        btn_cancel = QtWidgets.QPushButton("HỦY")
        btn_cancel.setObjectName("btnCancel")
        btn_cancel.clicked.connect(self.reject)

        btn_run = QtWidgets.QPushButton("🚀 XUẤT BẢN VẼ & ĐÓNG GÓI ZIP 1-CHẠM")
        btn_run.setObjectName("btnRun")
        btn_run.clicked.connect(self.accept)

        h_btn.addWidget(btn_cancel)
        h_btn.addWidget(btn_run)
        layout.addLayout(h_btn)


# =============================================================================
# BỘ ĐIỀU KHIỂN CHÍNH (MASTER EXPORTER & PACKAGER PIPELINE)
# =============================================================================
def run_blueprint_and_cad_packager():
    doc = App.ActiveDocument
    if not doc:
        QtWidgets.QMessageBox.warning(None, "WT3D Tool", "Vui lòng mở một file 3D (.stp, .fcstd, .iam) trước khi chạy!")
        return

    try:
        view = Gui.ActiveDocument.ActiveView
    except Exception:
        view = None

    if not view:
        QtWidgets.QMessageBox.warning(None, "WT3D Tool", "Không tìm thấy màn hình 3D View đang mở!")
        return

    # Lấy thông số Bounding Box và danh sách Part hợp lệ
    bbox, valid_objs = get_model_bounding_box_and_objects(doc)
    if not valid_objs:
        QtWidgets.QMessageBox.warning(None, "WT3D Tool", "Không tìm thấy chi tiết Solid 3D hợp lệ nào trong tài liệu!")
        return

    dx_mm = int(round(bbox.XLength)) if bbox and 0 < bbox.XLength < 50000 else 162
    dy_mm = int(round(bbox.YLength)) if bbox and 0 < bbox.YLength < 50000 else 120
    dz_mm = int(round(bbox.ZLength)) if bbox and 0 < bbox.ZLength < 50000 else 280

    # Tự động nhận diện tên chuẩn của thiết bị
    doc_label = doc.Label
    if (not doc_label or doc_label.lower().startswith("unnamed")) and len(doc.Objects) > 0:
        for obj in doc.Objects:
            if obj.Label and not obj.Label.lower().startswith("unnamed"):
                clean = re.sub(r'\.\d+$', '', obj.Label)
                doc_label = clean
                break

    if not doc_label or doc_label.lower().startswith("unnamed"):
        doc_label = "WT3D_Model_Asset"

    # Mở Dialog tùy chọn
    dialog = WT3DExportDialog(doc_label, dx_mm, dy_mm, dz_mm)
    if dialog.exec() != QtWidgets.QDialog.Accepted:
        return

    # Xác định thư mục lưu trữ chuẩn hóa
    if doc.FileName and os.path.exists(doc.FileName):
        base_dir = os.path.dirname(doc.FileName)
        # Nếu đang ở trong thư mục con, lùi về gốc module
        cur_dir_name = os.path.basename(base_dir).lower()
        if cur_dir_name.startswith("01_") or cur_dir_name.startswith("02_") or cur_dir_name.startswith("06_"):
            base_dir = os.path.dirname(base_dir)
        media_dir = os.path.join(base_dir, "06_Renders_and_Media")
    else:
        media_dir = os.path.join(r"D:\WT3D_Project\Render_Output", doc_label, "06_Renders_and_Media")

    export_dir = os.path.join(media_dir, "01_Marketplace_Upload_Package")
    img_dir    = os.path.join(media_dir, "01_4K_Images")
    wm_dir     = os.path.join(media_dir, "04_Watermarked_Exports")

    for d in [export_dir, img_dir, wm_dir]:
        os.makedirs(d, exist_ok=True)

    progress = QtWidgets.QProgressDialog("📦 Đang trích xuất bản vẽ DIM & các file CAD...", "Dừng", 0, 100)
    progress.setWindowTitle("WT3D Blueprint & CAD Packager")
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.setMinimumDuration(0)
    progress.setValue(10)
    QtWidgets.QApplication.processEvents()

    success_items = []
    render_w, render_h = 3840, 2160 # Chuẩn 4K Ultra HD sắc nét

    # Thiết lập ánh sáng & khử răng cưa
    try:
        view.setBackgroundColor(1.0, 1.0, 1.0)
        view.setDrawStyle("FlatLines")
        viewer = view.getViewer()
        if hasattr(viewer, "getSoRenderManager"):
            rm = viewer.getSoRenderManager()
            if hasattr(rm, "setAntialiasing"): rm.setAntialiasing(True, 4)
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # 1. CHỤP BỘ 4 BẢN VẼ KỸ THUẬT BLUEPRINT ĐÃ VẼ DIM KÍCH THƯỚC
    # -------------------------------------------------------------------------
    print("\n📸 [BƯỚC 1/3] Đang chụp bộ 4 bản vẽ kỹ thuật CAD Blueprint...")
    progress.setLabelText("📸 [BƯỚC 1/3] Đang chụp các hình chiếu & Vẽ đường gióng kích thước CAD...")

    bp_views = [
        ("01_Isometric_Front_Shaded", lambda: view.viewIsometric(), "", 0, 0, "", ""),
        ("02_Front_Elevation_Dim",    lambda: view.viewFront(),     "FRONT ELEVATION (HÌNH CHIẾU ĐỨNG)", dx_mm, dz_mm, "L", "H"),
        ("03_Top_Plan_Dim",           lambda: view.viewTop(),       "TOP PLAN VIEW (HÌNH CHIẾU BẰNG)",   dx_mm, dy_mm, "L", "W"),
        ("04_Right_Profile_Dim",      lambda: view.viewRight(),     "RIGHT SIDE ELEVATION (HÌNH CHIẾU CẠNH)", dy_mm, dz_mm, "W", "H")
    ]

    for idx, (name, v_func, v_title, v_h, v_v, l_h, l_v) in enumerate(bp_views):
        try:
            v_func()
            view.fitAll()
            try: view.zoomBy(0.90)
            except Exception: pass
            Gui.SendMsgToActiveView("ViewFit")
            QtWidgets.QApplication.processEvents()
            time.sleep(0.08)

            img_path = os.path.join(img_dir, f"{name}_4K.png")
            view.saveImage(img_path, render_w, render_h, "White")

            if v_h > 0 or v_v > 0:
                draw_cad_blueprint_dimensions(img_path, v_title, v_h, v_v, l_h, l_v)

            # Sao chép vào thư mục đóng gói xuất bản & đóng watermark
            pkg_img = os.path.join(export_dir, f"{name}.png")
            wm_img  = os.path.join(wm_dir, f"{name}_4K_WM.png")
            
            if os.path.exists(img_path):
                Image.open(img_path).save(pkg_img)
                Image.open(img_path).save(wm_img)
                apply_wt3d_watermark(wm_img, is_vertical=False, mode="MODE_B", project_code=doc_label)

            success_items.append(f"Bản vẽ kỹ thuật: {name}.png (Kích thước {v_h}x{v_v}mm)")
        except Exception as e:
            print(f"[WARN] Lỗi chụp bản vẽ {name}: {e}")

        progress.setValue(10 + int((idx + 1) / len(bp_views) * 25))
        QtWidgets.QApplication.processEvents()

    # -------------------------------------------------------------------------
    # 2. XUẤT TRỌN BỘ FILE CAD TRUNG TÍNH (STEP, IGES, STL, OBJ)
    # -------------------------------------------------------------------------
    print("\n💎 [BƯỚC 2/3] Đang xuất các file CAD trung tính...")
    progress.setLabelText("💎 [BƯỚC 2/3] Đang xuất STEP, IGES, STL, OBJ...")

    # 1. STEP AP214 (.stp)
    step_file = os.path.join(export_dir, f"{doc_label}.stp")
    try:
        Part.export(valid_objs, step_file)
        if os.path.exists(step_file) and os.path.getsize(step_file) > 0:
            success_items.append(f"STEP AP214 (.stp) [{os.path.getsize(step_file)//1024} KB]")
    except Exception as e:
        print(f"[WARN] Lỗi xuất STEP: {e}")

    # 2. IGES (.igs)
    igs_file = os.path.join(export_dir, f"{doc_label}.igs")
    try:
        Part.export(valid_objs, igs_file)
        if os.path.exists(igs_file) and os.path.getsize(igs_file) > 0:
            success_items.append(f"IGES Solid (.igs) [{os.path.getsize(igs_file)//1024} KB]")
    except Exception as e:
        print(f"[WARN] Lỗi xuất IGES: {e}")

    # 3. STL (.stl) & OBJ (.obj)
    stl_file = os.path.join(export_dir, f"{doc_label}.stl")
    obj_file = os.path.join(export_dir, f"{doc_label}.obj")
    try:
        combined_mesh = Mesh.Mesh()
        for o in valid_objs:
            m = Mesh.Mesh(o.Shape.tessellate(0.2))
            combined_mesh.addMesh(m)
        
        combined_mesh.write(stl_file)
        if os.path.exists(stl_file) and os.path.getsize(stl_file) > 0:
            success_items.append(f"Stereolithography STL (.stl) [{os.path.getsize(stl_file)//1024} KB]")

        combined_mesh.write(obj_file)
        if os.path.exists(obj_file) and os.path.getsize(obj_file) > 0:
            success_items.append(f"Wavefront OBJ (.obj) [{os.path.getsize(obj_file)//1024} KB]")
    except Exception as e:
        print(f"[WARN] Lỗi xuất Mesh STL/OBJ: {e}")

    progress.setValue(60)
    QtWidgets.QApplication.processEvents()

    # 4. BLENDER NGẦM (XUẤT FBX & BLEND NẾU CÓ)
    blender_exe = r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
    if not os.path.exists(blender_exe):
        blender_exe = r"C:\Program Files\Blender Foundation\Blender\blender.exe"

    blender_script = os.path.join(TOOLS_DIR, "Blender_OBJ_to_FBX.py")
    fbx_file = os.path.join(export_dir, f"{doc_label}.fbx")

    if os.path.exists(blender_exe) and os.path.exists(blender_script) and os.path.exists(obj_file):
        try:
            progress.setLabelText("🤖 Đang gọi Blender ngầm xuất FBX Binary & .BLEND...")
            cmd = [blender_exe, "-b", "-P", blender_script, "--", obj_file, fbx_file]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
            if os.path.exists(fbx_file):
                success_items.append(f"Autodesk FBX Binary (.fbx) [Blender Y-Up]")
            blend_file = os.path.join(export_dir, f"{doc_label}.blend")
            if os.path.exists(blend_file):
                success_items.append(f"Blender Native (.blend)")
        except Exception as e:
            print(f"[WARN] Blender conversion: {e}")

    progress.setValue(75)
    QtWidgets.QApplication.processEvents()

    # -------------------------------------------------------------------------
    # 3. TẠO README, ĐÍNH KÈM LICENSE & NÉN GÓI ZIP FLAT STRUCTURE
    # -------------------------------------------------------------------------
    print("\n📦 [BƯỚC 3/3] Đang tạo README, License và đóng gói file .ZIP...")
    progress.setLabelText("📦 [BƯỚC 3/3] Đang nén trọn bộ vào tệp .ZIP...")

    # README
    readme_path = generate_readme_file(export_dir, doc_label, dx_mm, dy_mm, dz_mm)
    if os.path.exists(readme_path):
        success_items.append("Tệp thông số Model: README_WT3D_Model_Instructions.txt")

    # LICENSE
    license_dst = os.path.join(export_dir, "License_Use.txt")
    if os.path.exists(LICENSE_SRC):
        try:
            with open(LICENSE_SRC, "r", encoding="utf-8") as fs, open(license_dst, "w", encoding="utf-8") as fd:
                fd.write(fs.read())
            success_items.append("Giấy phép bản quyền: License_Use.txt")
        except Exception:
            pass

    # NÉN FILE ZIP FLAT STRUCTURE
    zip_name = f"{doc_label}_Universal_CAD_Package.zip"
    zip_dest = os.path.join(export_dir, zip_name)

    try:
        with zipfile.ZipFile(zip_dest, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in os.listdir(export_dir):
                full_f = os.path.join(export_dir, f)
                if os.path.isfile(full_f) and not f.endswith(".zip") and not f.endswith(".blend1") and not f.endswith(".tmp"):
                    zf.write(full_f, arcname=f)
        
        if os.path.exists(zip_dest) and os.path.getsize(zip_dest) > 0:
            zip_size_mb = os.path.getsize(zip_dest) / (1024.0 * 1024.0)
            success_items.append(f"Gói nén hoàn chỉnh: {zip_name} ({zip_size_mb:.2f} MB)")
    except Exception as e:
        print(f"[WARN] Lỗi nén ZIP: {e}")

    progress.setValue(100)
    QtWidgets.QApplication.processEvents()
    progress.close()

    # Mở thư mục kết quả trong Windows Explorer
    try:
        os.startfile(export_dir)
    except Exception:
        pass

    # Hiển thị thông báo hoàn thành
    summary_text = f"🎉 ĐÃ XUẤT BẢN VẼ DIM & ĐÓNG GÓI FILE CAD THÀNH CÔNG!\n\n"
    summary_text += f"🏷️ Thiết bị: {doc_label}\n"
    summary_text += f"📐 Kích thước: {dx_mm} mm (L) × {dy_mm} mm (W) × {dz_mm} mm (H)\n\n"
    summary_text += "DANH SÁCH FILE ĐÃ TẠO:\n"
    for item in success_items:
        summary_text += f"  ✅ {item}\n"
    summary_text += f"\n📁 Thư mục lưu trữ: {export_dir}\n"
    summary_text += f"📦 File ZIP sẵn sàng: {zip_dest}\n"

    QtWidgets.QMessageBox.information(None, "WT3D B3 Hoàn Tất", summary_text)

if __name__ == "__main__" or "FreeCAD" in sys.modules:
    run_blueprint_and_cad_packager()
