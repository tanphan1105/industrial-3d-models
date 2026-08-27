# -*- coding: utf-8 -*-
"""
=============================================================================
WT3D_Smart_View_Standardizer.py (BỘ CĂN CHUẨN ĐỒNG BỘ NGUYÊN KHỐI RIGID BODY V3.1)
TÁC GIẢ: PHAN TRỌNG TẤN (@tanphan1105)
KẾ THỪA TOÀN BỘ KINH NGHIỆM THỰC CHIẾN TỪ INVENTOR PROJECTION ENGINE V7.0
=============================================================================
"""

import os
import sys
import math
import time

try:
    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError as e:
    print(f"[ERROR] Thiếu thư viện: {e}")

class WT3DSmartViewStandardizer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(WT3DSmartViewStandardizer, self).__init__(parent)
        self.setWindowTitle("🎯 WT3D - Chuẩn Hóa Góc Nhìn Đồng Bộ Nguyên Khối")
        self.setFixedSize(520, 640)
        self.setStyleSheet("""
            QDialog { background-color: #0A0B10; color: #F5F5F7; font-family: 'Segoe UI', Arial; font-size: 13px; }
            QGroupBox { font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; margin-top: 14px; padding-top: 16px; background-color: rgba(20, 24, 34, 0.9); color: #64D2FF; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 8px; color: #34C759; }
            QPushButton { font-weight: bold; font-size: 13px; border-radius: 8px; padding: 10px; background-color: rgba(255, 255, 255, 0.08); color: #FFF; border: 1px solid rgba(255, 255, 255, 0.12); }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.18); border-color: #34C759; color: #34C759; }
            QPushButton#btnSpecial { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #34C759, stop:1 #189644); color: #000; border: none; font-size: 13.5px; }
            QPushButton#btnSpecial:hover { background: #30D158; }
            QPushButton#btnReset { background-color: rgba(255, 69, 58, 0.2); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.4); }
            QPushButton#btnReset:hover { background-color: rgba(255, 69, 58, 0.35); color: #FFF; }
            QLabel#lblStatus { color: #FFD60A; font-weight: bold; font-size: 12px; }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        # Header
        lbl_title = QtWidgets.QLabel("🎯 CĂN CHUẨN GÓC NHÌN ĐỒNG BỘ NGUYÊN KHỐI")
        lbl_title.setStyleSheet("font-size: 15px; color: #FFF; font-weight: 800; margin-bottom: 2px;")
        layout.addWidget(lbl_title)
        
        lbl_sub = QtWidgets.QLabel("Biến Đổi Vật Thể Cứng (Rigid Body) • Xoay Đồng Bộ 100% Cả Cụm • Tiếp Đất Z=0")
        lbl_sub.setStyleSheet("font-size: 11px; color: #86868B; margin-bottom: 6px;")
        layout.addWidget(lbl_sub)

        # PHẦN 1: CĂN CHỈNH BẰNG MẶT CHỌN TRỰC QUAN (Smart Face Alignment)
        grp_face = QtWidgets.QGroupBox("👆 1. Căn Chuẩn Bằng Mặt Phẳng Được Chọn (Face Selection)")
        v_face = QtWidgets.QVBoxLayout(grp_face)
        
        lbl_face_hint = QtWidgets.QLabel("👉 <i>Click chọn 1 mặt phẳng trên 3D, rồi bấm nút dưới:</i>")
        lbl_face_hint.setStyleSheet("color: #A1A1A6; font-size: 12px;")
        v_face.addWidget(lbl_face_hint)

        h_face_btns = QtWidgets.QHBoxLayout()
        btn_set_bottom = QtWidgets.QPushButton("⚓ ĐẶT MẶT NÀY LÀM ĐÁY (ÚP NGUYÊN KHỐI XUỐNG SÀN Z=0)")
        btn_set_bottom.setObjectName("btnSpecial")
        btn_set_bottom.clicked.connect(self.align_selected_face_to_bottom)
        
        btn_set_front = QtWidgets.QPushButton("🎯 ĐẶT MẶT NÀY LÀM MẶT TRƯỚC (FRONT)")
        btn_set_front.clicked.connect(self.align_selected_face_to_front)
        
        h_face_btns.addWidget(btn_set_bottom)
        h_face_btns.addWidget(btn_set_front)
        v_face.addLayout(h_face_btns)
        layout.addWidget(grp_face)

        # PHẦN 2: MA TRẬN XOAY NGUYÊN KHỐI 90 ĐỘ
        grp_matrix = QtWidgets.QGroupBox("🔄 2. Xoay Đồng Bộ Cả Cụm Lắp Ráp (Rigid Rotation)")
        v_matrix = QtWidgets.QVBoxLayout(grp_matrix)
        
        h_row1 = QtWidgets.QHBoxLayout()
        btn_x90 = QtWidgets.QPushButton("📐 Dựng Đứng Cả Cụm (+90° Trục X)\n[Sửa file nằm ngửa]")
        btn_x90.clicked.connect(lambda: self.rotate_entire_assembly(App.Vector(1, 0, 0), 90))
        btn_x_neg90 = QtWidgets.QPushButton("📐 Dựng Ngược Cả Cụm (-90° Trục X)")
        btn_x_neg90.clicked.connect(lambda: self.rotate_entire_assembly(App.Vector(1, 0, 0), -90))
        h_row1.addWidget(btn_x90)
        h_row1.addWidget(btn_x_neg90)
        v_matrix.addLayout(h_row1)

        h_row2 = QtWidgets.QHBoxLayout()
        btn_z90 = QtWidgets.QPushButton("🔄 Xoay Ngang Cả Cụm +90° (Đổi Mặt)")
        btn_z90.clicked.connect(lambda: self.rotate_entire_assembly(App.Vector(0, 0, 1), 90))
        btn_z180 = QtWidgets.QPushButton("🔄 Lật Cả Cụm 180° (Trước ➔ Sau)")
        btn_z180.clicked.connect(lambda: self.rotate_entire_assembly(App.Vector(0, 0, 1), 180))
        h_row2.addWidget(btn_z90)
        h_row2.addWidget(btn_z180)
        v_matrix.addLayout(h_row2)
        layout.addWidget(grp_matrix)

        # PHẦN 3: TIẾP ĐẤT & KIỂM TRA MẶT CHIẾU
        grp_verify = QtWidgets.QGroupBox("⚓ 3. Tiếp Đất Phẳng Sàn & Kiểm Tra Mặt Chiếu")
        v_verify = QtWidgets.QVBoxLayout(grp_verify)
        
        h_grd_row = QtWidgets.QHBoxLayout()
        btn_ground = QtWidgets.QPushButton("⚓ TIẾP ĐẤT Z = 0 & CĂN TÂM (0, 0, 0)")
        btn_ground.setObjectName("btnSpecial")
        btn_ground.clicked.connect(self.ground_and_center_entire_assembly)
        
        btn_reset = QtWidgets.QPushButton("🔄 KHÔI PHỤC GỐC (0,0,0)")
        btn_reset.setObjectName("btnReset")
        btn_reset.clicked.connect(self.reset_all_placements)
        
        h_grd_row.addWidget(btn_ground)
        h_grd_row.addWidget(btn_reset)
        v_verify.addLayout(h_grd_row)

        h_vbtns = QtWidgets.QHBoxLayout()
        btn_v_front = QtWidgets.QPushButton("Mặt Trước (Front - 1)")
        btn_v_front.clicked.connect(self.view_front)
        btn_v_top = QtWidgets.QPushButton("Mặt Trên (Top - 2)")
        btn_v_top.clicked.connect(self.view_top)
        btn_v_iso = QtWidgets.QPushButton("Trục Đo (Iso 3/4 - 0)")
        btn_v_iso.clicked.connect(self.view_iso)
        h_vbtns.addWidget(btn_v_front)
        h_vbtns.addWidget(btn_v_top)
        h_vbtns.addWidget(btn_v_iso)
        v_verify.addLayout(h_vbtns)
        layout.addWidget(grp_verify)

        # Status bar
        self.lbl_status = QtWidgets.QLabel("Trạng thái: Sẵn sàng.")
        self.lbl_status.setObjectName("lblStatus")
        layout.addWidget(self.lbl_status)

        # Close
        btn_done = QtWidgets.QPushButton("HOÀN TẤT & ĐÓNG")
        btn_done.clicked.connect(self.accept)
        layout.addWidget(btn_done)

    # -------------------------------------------------------------------------
    # TÍNH TOÁN TÂM CHUNG & BOUNDING BOX CỦA TOÀN BỘ CỤM
    # -------------------------------------------------------------------------
    def get_assembly_bounding_box(self):
        doc = App.ActiveDocument
        if not doc: return None
        bbox = None
        for obj in doc.Objects:
            if hasattr(obj, "Shape") and hasattr(obj.Shape, "BoundBox"):
                b = obj.Shape.BoundBox
                if b.isValid():
                    if bbox is None: bbox = App.BoundBox(b)
                    else: bbox.add(b)
        return bbox

    # -------------------------------------------------------------------------
    # CẬP NHẬT GIAO DIỆN & ÉP CAMERA THEO DÕI MÔ HÌNH (FORCE VIEW FIT)
    # -------------------------------------------------------------------------
    def refresh_view(self):
        doc = App.ActiveDocument
        if doc: doc.recompute()
        Gui.updateGui()
        QtWidgets.QApplication.processEvents()
        time.sleep(0.05)
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.fitAll()
            Gui.SendMsgToActiveView("ViewFit")

    # -------------------------------------------------------------------------
    # XOAY NGUYÊN KHỐI TOÀN BỘ CỤM QUANH TÂM CHUNG (RIGID BODY ROTATION)
    # -------------------------------------------------------------------------
    def rotate_entire_assembly(self, axis, deg):
        doc = App.ActiveDocument
        if not doc: return
        bbox = self.get_assembly_bounding_box()
        if not bbox or not bbox.isValid():
            self.lbl_status.setText("⚠️ Không tìm thấy đối tượng 3D nào!")
            return

        center = bbox.Center
        rot = App.Rotation(axis, deg)

        # Phép biến đổi Affine vật thể cứng: P_new = Center + R * (P_old - Center)
        for obj in doc.Objects:
            if hasattr(obj, "Placement") and not obj.InList:
                old_pos = obj.Placement.Base
                rel_pos = old_pos.sub(center)
                new_rel = rot.multVec(rel_pos)
                obj.Placement.Base = center.add(new_rel)
                obj.Placement.Rotation = rot.multiply(obj.Placement.Rotation)

        self.ground_and_center_entire_assembly()
        self.lbl_status.setText(f"✅ Đã xoay nguyên khối {deg}° quanh trục {axis}!")

    # -------------------------------------------------------------------------
    # TIẾP ĐẤT & CĂN TÂM ĐỒNG BỘ NGUYÊN KHỐI
    # -------------------------------------------------------------------------
    def ground_and_center_entire_assembly(self):
        doc = App.ActiveDocument
        if not doc: return
        bbox = self.get_assembly_bounding_box()
        if bbox and bbox.isValid():
            shift = App.Vector(-bbox.Center.x, -bbox.Center.y, -bbox.ZMin)
            for obj in doc.Objects:
                if hasattr(obj, "Placement") and not obj.InList:
                    obj.Placement.Base = obj.Placement.Base.add(shift)
            
            self.refresh_view()
            self.lbl_status.setText("✅ Đã tiếp đất đáy Z=0 & Căn tâm (0,0,0) toàn bộ cụm!")

    # -------------------------------------------------------------------------
    # CĂN MẶT ĐƯỢC CHỌN THÀNH ĐÁY NGUYÊN KHỐI
    # -------------------------------------------------------------------------
    def align_selected_face_to_bottom(self):
        doc = App.ActiveDocument
        if not doc: return
        sel = Gui.Selection.getSelectionEx()
        if not sel or not sel[0].SubObjects:
            self.lbl_status.setText("⚠️ Vui lòng click chọn 1 mặt phẳng trên 3D trước!")
            return

        sub = sel[0].SubObjects[0]
        if hasattr(sub, "normalAt"):
            normal = sub.normalAt(0, 0)
            target = App.Vector(0, 0, -1)
            rot = App.Rotation(normal, target)
            bbox = self.get_assembly_bounding_box()
            center = bbox.Center if bbox else App.Vector(0, 0, 0)

            for obj in doc.Objects:
                if hasattr(obj, "Placement") and not obj.InList:
                    rel_pos = obj.Placement.Base.sub(center)
                    obj.Placement.Base = center.add(rot.multVec(rel_pos))
                    obj.Placement.Rotation = rot.multiply(obj.Placement.Rotation)

            self.ground_and_center_entire_assembly()
            self.lbl_status.setText("✅ Đã đặt mặt chọn làm Đáy và xoay nguyên khối thành công!")
        else:
            self.lbl_status.setText("⚠️ Đối tượng được chọn không phải là mặt phẳng!")

    # -------------------------------------------------------------------------
    # CĂN MẶT ĐƯỢC CHỌN THÀNH MẶT TRƯỚC (FRONT) NGUYÊN KHỐI
    # -------------------------------------------------------------------------
    def align_selected_face_to_front(self):
        doc = App.ActiveDocument
        if not doc: return
        sel = Gui.Selection.getSelectionEx()
        if not sel or not sel[0].SubObjects:
            self.lbl_status.setText("⚠️ Vui lòng click chọn 1 mặt phẳng trên 3D trước!")
            return

        sub = sel[0].SubObjects[0]
        if hasattr(sub, "normalAt"):
            normal = sub.normalAt(0, 0)
            target = App.Vector(0, -1, 0)
            rot = App.Rotation(normal, target)
            bbox = self.get_assembly_bounding_box()
            center = bbox.Center if bbox else App.Vector(0, 0, 0)

            for obj in doc.Objects:
                if hasattr(obj, "Placement") and not obj.InList:
                    rel_pos = obj.Placement.Base.sub(center)
                    obj.Placement.Base = center.add(rot.multVec(rel_pos))
                    obj.Placement.Rotation = rot.multiply(obj.Placement.Rotation)

            self.ground_and_center_entire_assembly()
            self.view_front()
            self.lbl_status.setText("✅ Đã đặt mặt chọn làm Mặt Trước (Front) nguyên khối thành công!")
        else:
            self.lbl_status.setText("⚠️ Đối tượng được chọn không phải là mặt phẳng!")

    # -------------------------------------------------------------------------
    # KHÔI PHỤC VỊ TRÍ GỐC
    # -------------------------------------------------------------------------
    def reset_all_placements(self):
        doc = App.ActiveDocument
        if not doc: return
        for obj in doc.Objects:
            if hasattr(obj, "Placement"):
                obj.Placement = App.Placement()
        self.refresh_view()
        self.lbl_status.setText("🔄 Đã khôi phục toàn bộ Placement về (0,0,0)!")

    def view_front(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewFront()
            self.refresh_view()

    def view_top(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewTop()
            self.refresh_view()

    def view_iso(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewIsometric()
            self.refresh_view()

def run_standardizer():
    if not App.ActiveDocument:
        QtWidgets.QMessageBox.warning(None, "WT3D", "Vui lòng mở một mô hình 3D trong FreeCAD trước!")
        return
    dlg = WT3DSmartViewStandardizer()
    dlg.exec()

if __name__ == "__main__" or "FreeCAD" in sys.modules:
    run_standardizer()
