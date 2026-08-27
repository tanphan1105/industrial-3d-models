# -*- coding: utf-8 -*-
"""
=============================================================================
WT3D_FreeCAD_Align_And_Orient.py
Công cụ Căn Chỉnh Mặt Nhìn, Dựng Đứng & Tiếp Đất 1-Chạm Trên FreeCAD
TÁC GIẢ: PHAN TRỌNG TẤN (@tanphan1105)
KẾ THỪA TỪ iLOGIC TOOL B1_Align_Selected_Face_To_XZ_Ground V7.0
=============================================================================
"""

import os
import sys
import math

try:
    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError as e:
    print(f"[ERROR] Thiếu thư viện: {e}")

class WT3DOrientationDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(WT3DOrientationDialog, self).__init__(parent)
        self.setWindowTitle("🧭 WT3D - Định Hướng & Căn Chỉnh Mặt Nhìn 3D")
        self.setFixedSize(480, 520)
        self.setStyleSheet("""
            QDialog { background-color: #0F1117; color: #F5F5F7; font-family: 'Segoe UI', Arial; font-size: 13px; }
            QGroupBox { font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; margin-top: 14px; padding-top: 16px; background-color: rgba(26, 29, 41, 0.9); color: #64D2FF; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 8px; color: #34C759; }
            QPushButton { font-weight: bold; font-size: 13px; border-radius: 8px; padding: 10px; background-color: rgba(255, 255, 255, 0.08); color: #FFF; border: 1px solid rgba(255, 255, 255, 0.1); }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.18); border-color: #34C759; color: #34C759; }
            QPushButton#btnGround { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #34C759, stop:1 #189644); color: #000; border: none; font-size: 14px; }
            QPushButton#btnGround:hover { background: #30D158; }
            QPushButton#btnClose { background-color: rgba(255, 255, 255, 0.05); color: #A1A1A6; }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        # Header
        lbl_title = QtWidgets.QLabel("🧭 BỘ ĐỊNH HƯỚNG & CĂN MẶT 3D CHUẨN KỸ THUẬT")
        lbl_title.setStyleSheet("font-size: 15px; color: #FFF; font-weight: 800; margin-bottom: 2px;")
        layout.addWidget(lbl_title)
        
        lbl_sub = QtWidgets.QLabel("Khắc phục lệch trục Y-Up / Z-Up • Tiếp đất Z=0 • Căn tâm (0,0,0)")
        lbl_sub.setStyleSheet("font-size: 11.5px; color: #86868B; margin-bottom: 8px;")
        layout.addWidget(lbl_sub)

        # 1. Dựng Đứng & Xoay Nhanh (Orientation Presets)
        grp_orient = QtWidgets.QGroupBox("🔄 1. Dựng Đứng & Xoay Hướng Mô Hình (3D Transform)")
        v_orient = QtWidgets.QVBoxLayout(grp_orient)
        
        h_row1 = QtWidgets.QHBoxLayout()
        btn_rot_x90 = QtWidgets.QPushButton("📐 Dựng đứng (+90° Trục X)\n(Sửa file Inventor bị nằm ngửa)")
        btn_rot_x90.clicked.connect(lambda: self.rotate_model(App.Vector(1, 0, 0), 90))
        btn_rot_x_neg90 = QtWidgets.QPushButton("📐 Dựng ngược (-90° Trục X)")
        btn_rot_x_neg90.clicked.connect(lambda: self.rotate_model(App.Vector(1, 0, 0), -90))
        h_row1.addWidget(btn_rot_x90)
        h_row1.addWidget(btn_rot_x_neg90)
        v_orient.addLayout(h_row1)

        h_row2 = QtWidgets.QHBoxLayout()
        btn_rot_z90 = QtWidgets.QPushButton("🔄 Xoay ngang +90° (Đổi Mặt Trước/Hông)")
        btn_rot_z90.clicked.connect(lambda: self.rotate_model(App.Vector(0, 0, 1), 90))
        btn_rot_z180 = QtWidgets.QPushButton("🔄 Lật 180° (Đổi Trước ➔ Sau)")
        btn_rot_z180.clicked.connect(lambda: self.rotate_model(App.Vector(0, 0, 1), 180))
        h_row2.addWidget(btn_rot_z90)
        h_row2.addWidget(btn_rot_z180)
        v_orient.addLayout(h_row2)
        layout.addWidget(grp_orient)

        # 2. Tiếp Đất & Căn Tâm (Ground & Center)
        grp_ground = QtWidgets.QGroupBox("⚓ 2. Tiếp Đất Phẳng Sàn & Căn Tâm Gốc Tọa Độ")
        v_ground = QtWidgets.QVBoxLayout(grp_ground)
        btn_ground = QtWidgets.QPushButton("🚀 TIẾP ĐẤT Z = 0 & CĂN TÂM (0, 0, 0)")
        btn_ground.setObjectName("btnGround")
        btn_ground.clicked.connect(self.ground_and_center_model)
        v_ground.addWidget(btn_ground)
        layout.addWidget(grp_ground)

        # 3. Phím Xem Nhanh & Fit To View
        grp_views = QtWidgets.QGroupBox("👁️ 3. Kiểm Tra Góc Nhìn & Fit To View")
        v_views = QtWidgets.QVBoxLayout(grp_views)
        h_views = QtWidgets.QHBoxLayout()
        
        btn_v_front = QtWidgets.QPushButton("Mặt Trước (Front)")
        btn_v_front.clicked.connect(self.view_front)
        btn_v_top = QtWidgets.QPushButton("Mặt Trên (Top)")
        btn_v_top.clicked.connect(self.view_top)
        btn_v_iso = QtWidgets.QPushButton("Trục Đo (Iso 3/4)")
        btn_v_iso.clicked.connect(self.view_iso)
        
        h_views.addWidget(btn_v_front)
        h_views.addWidget(btn_v_top)
        h_views.addWidget(btn_v_iso)
        v_views.addLayout(h_views)
        layout.addWidget(grp_views)

        # Close button
        btn_close = QtWidgets.QPushButton("ĐÓNG")
        btn_close.setObjectName("btnClose")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def rotate_model(self, axis, degrees):
        doc = App.ActiveDocument
        if not doc: return
        rot = App.Rotation(axis, degrees)
        for obj in doc.Objects:
            if hasattr(obj, "Placement"):
                obj.Placement.Rotation = rot.multiply(obj.Placement.Rotation)
        doc.recompute()
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.fitAll()

    def ground_and_center_model(self):
        doc = App.ActiveDocument
        if not doc: return
        bbox = None
        for obj in doc.Objects:
            if hasattr(obj, "Shape") and hasattr(obj.Shape, "BoundBox"):
                if bbox is None:
                    bbox = App.BoundBox(obj.Shape.BoundBox)
                else:
                    bbox.add(obj.Shape.BoundBox)

        if bbox and bbox.isValid():
            # Dịch chuyển sao cho tâm X=0, Y=0 và đáy thấp nhất chạm đúng Z=0
            shift = App.Vector(-bbox.Center.x, -bbox.Center.y, -bbox.ZMin)
            for obj in doc.Objects:
                if hasattr(obj, "Placement"):
                    obj.Placement.Base = obj.Placement.Base.add(shift)
            doc.recompute()
            if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
                Gui.ActiveDocument.ActiveView.viewIsometric()
                Gui.ActiveDocument.ActiveView.fitAll()
            QtWidgets.QMessageBox.information(self, "WT3D", "✅ Đã tiếp đất đáy Z=0 và căn tâm (0,0,0) hoàn tất!")

    def view_front(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewFront()
            Gui.ActiveDocument.ActiveView.fitAll()

    def view_top(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewTop()
            Gui.ActiveDocument.ActiveView.fitAll()

    def view_iso(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewIsometric()
            Gui.ActiveDocument.ActiveView.fitAll()

def run_align_tool():
    if not App.ActiveDocument:
        QtWidgets.QMessageBox.warning(None, "WT3D", "Vui lòng mở một mô hình 3D trong FreeCAD trước!")
        return
    dlg = WT3DOrientationDialog()
    dlg.exec()

if __name__ == "__main__" or "FreeCAD" in sys.modules:
    run_align_tool()
