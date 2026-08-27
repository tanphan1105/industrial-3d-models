# -*- coding: utf-8 -*-
"""
=============================================================================
WT3D_FreeCAD_View_Manager.py (BẢN V13.0 ALIGN TO SELECTION MASTER)
TÁC GIẢ: PHAN TRỌNG TẤN (@tanphan1105)
TÍCH HỢP FREECAD ALIGN TO SELECTION & PRO ORIENTATION STUDIO
=============================================================================
"""

import sys
import math
import time
import traceback

try:
    import FreeCAD as App
    import FreeCADGui as Gui
    import Part
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError as e:
    print(f"[ERROR] Thiếu thư viện: {e}")

class WT3DProViewWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #0F111A;
                color: #F5F5F7;
                font-family: 'Segoe UI', Arial;
                font-size: 12px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #2B3045;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px 6px 6px 6px;
                background-color: #171A26;
                color: #34C759;
                font-size: 11.5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
            }
            QPushButton {
                font-weight: bold;
                font-size: 12px;
                border-radius: 6px;
                padding: 8px 10px;
                border: 1px solid #2B3045;
                background-color: #202538;
                color: #E5E5EA;
                text-align: left;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #2D344E;
                border-color: #34C759;
                color: #34C759;
            }
            QPushButton#btnGreen {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #34C759, stop:1 #189644);
                color: #000;
                border: none;
                font-size: 12.5px;
            }
            QPushButton#btnGreen:hover { background: #30D158; }
            QPushButton#btnBlue {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0A84FF, stop:1 #0058B6);
                color: #FFF;
                border: none;
                font-size: 12.5px;
            }
            QPushButton#btnBlue:hover { background: #409CFF; }
            QPushButton#btnSub {
                background-color: #1E2335;
                font-size: 11.5px;
                min-height: 28px;
            }
            QPushButton#btnSub:hover {
                background-color: #28324E;
                color: #64D2FF;
                border-color: #64D2FF;
            }
            QPushButton#btnUndo {
                background: rgba(255, 69, 58, 0.2);
                color: #FF453A;
                border: 1px solid rgba(255, 69, 58, 0.4);
                text-align: center;
                font-size: 11.5px;
                min-height: 28px;
            }
            QPushButton#btnUndo:hover { background: rgba(255, 69, 58, 0.4); color: #FFF; }
            QPushButton#btnFit {
                background: #232A3E;
                color: #64D2FF;
                border: 1px solid #0A84FF;
                font-size: 12px;
                text-align: center;
            }
            QPushButton#btnFit:hover { background: #0A84FF; color: #FFF; }
            QLabel#lblHint {
                color: #8E94A8;
                font-size: 11px;
                font-style: italic;
                padding: 2px 0;
            }
            QLabel#lblStatus {
                color: #FFD60A;
                font-weight: bold;
                font-size: 11.5px;
                padding: 4px 2px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)

        # Header
        lbl_title = QtWidgets.QLabel("🎯 WT3D MASTER PRO STUDIO V13.0")
        lbl_title.setStyleSheet("font-size: 12px; color:#FFF; font-weight:800;")
        layout.addWidget(lbl_title)

        lbl_sub = QtWidgets.QLabel("Align To Selection • Định Hướng 90° Chuẩn Kỹ Thuật")
        lbl_sub.setObjectName("lblHint")
        layout.addWidget(lbl_sub)

        # ── KHỐI 1: ALIGN TO SELECTION (LOOK AT) ─────────────────────────────
        grp1 = QtWidgets.QGroupBox("👁️ 1. Căn góc nhìn vuông góc (Align to Selection)")
        v1 = QtWidgets.QVBoxLayout(grp1)
        v1.setSpacing(4)
        
        btn_look_at = QtWidgets.QPushButton("👁️ ALIGN TO SELECTION — NHÌN VUÔNG GÓC (F7)")
        btn_look_at.setObjectName("btnBlue")
        btn_look_at.clicked.connect(self.align_to_selection)
        v1.addWidget(btn_look_at)
        layout.addWidget(grp1)

        # ── KHỐI 2: ĐỊNH HƯỚNG CỖ MÁY 90° ───────────────────────────────────
        grp2 = QtWidgets.QGroupBox("📐 2. Định hướng cỗ máy (Quy chuẩn 90°)")
        v2 = QtWidgets.QVBoxLayout(grp2)
        v2.setSpacing(5)

        btn_up90 = QtWidgets.QPushButton("📐 DỰNG ĐỨNG CẢ CỤM (+90° TRỤC X)\n     (Chuyển file nằm ngửa thành đứng thẳng Z=0)")
        btn_up90.setObjectName("btnGreen")
        btn_up90.clicked.connect(lambda: self.rotate_assembly(App.Vector(1, 0, 0), 90))
        v2.addWidget(btn_up90)

        h_rot = QtWidgets.QHBoxLayout()
        btn_rot_z_plus = QtWidgets.QPushButton("🔄 Xoay +90° Z\n(Mặt Trước)")
        btn_rot_z_plus.setObjectName("btnSub")
        btn_rot_z_plus.clicked.connect(lambda: self.rotate_assembly(App.Vector(0, 0, 1), 90))
        
        btn_rot_z_minus = QtWidgets.QPushButton("🔄 Xoay -90° Z\n(Quay ngược)")
        btn_rot_z_minus.setObjectName("btnSub")
        btn_rot_z_minus.clicked.connect(lambda: self.rotate_assembly(App.Vector(0, 0, 1), -90))
        
        h_rot.addWidget(btn_rot_z_plus)
        h_rot.addWidget(btn_rot_z_minus)
        v2.addLayout(h_rot)

        btn_ground = QtWidgets.QPushButton("⚓ TIẾP ĐẤT SÀN Z = 0 & CĂN TÂM (0, 0, 0)")
        btn_ground.clicked.connect(self.ground_assembly)
        v2.addWidget(btn_ground)

        layout.addWidget(grp2)

        # ── KHỐI 3: GÓC NHÌN CHUẨN NAVIGATION CUBE ───────────────────────────
        grp3 = QtWidgets.QGroupBox("⚡ 3. Góc nhìn chuẩn FreeCAD Navigation Cube")
        grid = QtWidgets.QGridLayout(grp3)
        grid.setSpacing(4)
        
        std_views = [
            ("📐 Iso 3/4 (0)",   self.view_iso,    0, 0),
            ("🟦 Trước (1)",     self.view_front,  0, 1),
            ("⬆️ Trên (2)",      self.view_top,    1, 0),
            ("➡️ Phải (3)",      self.view_right,  1, 1),
            ("⬅️ Trái (4)",      self.view_left,   2, 0),
            ("🔙 Sau (5)",       self.view_rear,   2, 1),
        ]
        for label, slot, row, col in std_views:
            btn = QtWidgets.QPushButton(label)
            btn.clicked.connect(slot)
            grid.addWidget(btn, row, col)

        layout.addWidget(grp3)

        # ── Fit to View & Undo ──────────────────────────────────────────────
        h_tools = QtWidgets.QHBoxLayout()
        btn_fit = QtWidgets.QPushButton("🔍 FIT TO VIEW (V ➔ F)")
        btn_fit.setObjectName("btnFit")
        btn_fit.clicked.connect(self.fit_all)
        
        btn_undo = QtWidgets.QPushButton("↩️ HOÀN TÁC (Ctrl+Z)")
        btn_undo.setObjectName("btnUndo")
        btn_undo.clicked.connect(self.undo_action)
        
        h_tools.addWidget(btn_fit)
        h_tools.addWidget(btn_undo)
        layout.addLayout(h_tools)

        # Status
        self.lbl_status = QtWidgets.QLabel("Sẵn sàng. Click chọn 1 mặt phẳng trên 3D rồi bấm Align to Selection.")
        self.lbl_status.setObjectName("lblStatus")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        layout.addStretch()

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Z:
            self.undo_action()
            event.accept()
        else:
            super().keyPressEvent(event)

    # ── Helpers ─────────────────────────────────────────────────────────────
    def _get_view(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            return Gui.ActiveDocument.ActiveView
        return None

    def _get_or_create_assembly(self):
        doc = App.ActiveDocument
        if not doc: return None
        for obj in doc.Objects:
            if obj.isDerivedFrom("App::Part") and obj.Name.startswith("WT3D_Assembly"):
                return obj
        
        asm = doc.addObject("App::Part", "WT3D_Assembly")
        root_children = [o for o in doc.Objects if o != asm and not o.InList]
        for c in root_children:
            asm.addObject(c)
        doc.recompute()
        return asm

    # ── 1. ALIGN TO SELECTION (LOOK AT CHUẨN XÁC CỦA FREECAD) ───────────────
    def align_to_selection(self):
        sel = Gui.Selection.getSelectionEx()
        if not sel:
            self.lbl_status.setText("⚠️ Chưa chọn mặt nào! Click vào 1 mặt phẳng trên 3D trước.")
            return

        # 1. Thử gọi lệnh C++ Native của FreeCAD
        try:
            Gui.SendMsgToActiveView("ViewSelection")
        except Exception:
            pass

        # 2. Đồng thời áp dụng thuật toán ma trận Coin3D để đảm bảo 100% không trượt
        view = self._get_view()
        if not view: return
        
        try:
            for s in sel:
                obj = s.Object
                for sub in s.SubObjects:
                    if hasattr(sub, "normalAt") and hasattr(sub, "ParameterRange"):
                        pr = sub.ParameterRange
                        u_mid = (pr[0] + pr[1]) / 2.0
                        v_mid = (pr[2] + pr[3]) / 2.0
                        local_n = sub.normalAt(u_mid, v_mid)
                        
                        if hasattr(sub, "Orientation") and sub.Orientation == "Reversed":
                            local_n = App.Vector(-local_n.x, -local_n.y, -local_n.z)
                        
                        length = math.sqrt(local_n.x**2 + local_n.y**2 + local_n.z**2)
                        if length > 1e-6:
                            local_n = App.Vector(local_n.x/length, local_n.y/length, local_n.z/length)
                        
                        if obj and hasattr(obj, "getGlobalPlacement"):
                            world_n = obj.getGlobalPlacement().Rotation.multVec(local_n)
                        elif obj and hasattr(obj, "Placement") and hasattr(obj.Placement, "Rotation"):
                            world_n = obj.Placement.Rotation.multVec(local_n)
                        else:
                            world_n = local_n
                        
                        D = App.Vector(-world_n.x, -world_n.y, -world_n.z)
                        if abs(D.z) > 0.9:
                            Up = App.Vector(0, 1, 0) if D.z < 0 else App.Vector(0, -1, 0)
                        else:
                            Up = App.Vector(0, 0, 1)
                            
                        Z_cam = App.Vector(-D.x, -D.y, -D.z)
                        X_cam = App.Vector(
                            Up.y * Z_cam.z - Up.z * Z_cam.y,
                            Up.z * Z_cam.x - Up.x * Z_cam.z,
                            Up.x * Z_cam.y - Up.y * Z_cam.x
                        )
                        x_len = math.sqrt(X_cam.x**2 + X_cam.y**2 + X_cam.z**2)
                        if x_len > 1e-6: X_cam = App.Vector(X_cam.x/x_len, X_cam.y/x_len, X_cam.z/x_len)
                        else: X_cam = App.Vector(1, 0, 0)
                        
                        Y_cam = App.Vector(
                            Z_cam.y * X_cam.z - Z_cam.z * X_cam.y,
                            Z_cam.z * X_cam.x - Z_cam.x * X_cam.z,
                            Z_cam.x * X_cam.y - Z_cam.y * X_cam.x
                        )
                        
                        mat = App.Matrix(
                            X_cam.x, Y_cam.x, Z_cam.x, 0.0,
                            X_cam.y, Y_cam.y, Z_cam.y, 0.0,
                            X_cam.z, Y_cam.z, Z_cam.z, 0.0,
                            0.0,     0.0,     0.0,     1.0
                        )
                        
                        rot = App.Placement(mat).Rotation
                        view.setCameraOrientation(rot)
                        view.fitAll()
                        Gui.SendMsgToActiveView("ViewFit")
                        self.lbl_status.setText("✅ Align to Selection thành công! Camera đã nhìn vuông góc vào mặt chọn.")
                        return
        except Exception as e:
            self.lbl_status.setText(f"⚠️ Lỗi Align: {e}")

    # ── 2. XOAY CỤM LẮP RÁP CHUẨN XÁC ──────────────────────────────────────
    def rotate_assembly(self, axis, deg):
        doc = App.ActiveDocument
        if not doc: return
        asm = self._get_or_create_assembly()
        if not asm: return

        doc.openTransaction(f"Rotate {deg} around {axis}")
        try:
            rot = App.Rotation(axis, deg)
            center = asm.Shape.BoundBox.Center
            asm.Placement = App.Placement(App.Vector(0, 0, 0), rot, center).multiply(asm.Placement)
            doc.recompute()

            bbox = asm.Shape.BoundBox
            shift = App.Vector(-bbox.Center.x, -bbox.Center.y, -bbox.ZMin)
            asm.Placement = App.Placement(shift, App.Rotation()).multiply(asm.Placement)
            doc.recompute()
            doc.commitTransaction()

            self.fit_all()
            self.lbl_status.setText(f"✅ Đã xoay cỗ máy {deg}° và tiếp đất Z=0 hoàn hảo!")
        except Exception as e:
            doc.abortTransaction()
            self.lbl_status.setText(f"⚠️ Lỗi: {e}")

    def ground_assembly(self):
        doc = App.ActiveDocument
        if not doc: return
        asm = self._get_or_create_assembly()
        if not asm: return

        doc.openTransaction("Ground Assembly")
        try:
            bbox = asm.Shape.BoundBox
            shift = App.Vector(-bbox.Center.x, -bbox.Center.y, -bbox.ZMin)
            asm.Placement = App.Placement(shift, App.Rotation()).multiply(asm.Placement)
            doc.recompute()
            doc.commitTransaction()

            self.fit_all()
            self.lbl_status.setText("✅ Đã tiếp đất phẳng sàn Z=0 & Căn giữa tâm (0,0,0)!")
        except Exception as e:
            doc.abortTransaction()
            self.lbl_status.setText(f"⚠️ Lỗi: {e}")

    def undo_action(self):
        try:
            Gui.runCommand("Std_Undo", 0)
            if App.ActiveDocument:
                App.ActiveDocument.recompute()
            self.fit_all()
            self.lbl_status.setText("↩️ Đã hoàn tác thao tác vừa rồi (Undo)!")
        except Exception as e:
            self.lbl_status.setText(f"⚠️ Không có thao tác để Undo: {e}")

    # ── CÁC HƯỚNG NHÌN CHUẨN ────────────────────────────────────────────────
    def view_iso(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewIsometric()
            self.fit_all()
            self.lbl_status.setText("📐 Isometric (Trục đo 3/4)")

    def view_front(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewFront()
            self.fit_all()
            self.lbl_status.setText("🟦 Front View (Mặt Trước — Phím 1)")

    def view_top(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewTop()
            self.fit_all()
            self.lbl_status.setText("⬆️ Top View (Mặt Trên — Phím 2)")

    def view_right(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewRight()
            self.fit_all()
            self.lbl_status.setText("➡️ Right View (Mặt Phải — Phím 3)")

    def view_left(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.viewLeft()
            self.fit_all()
            self.lbl_status.setText("⬅️ Left View (Mặt Trái — Phím 4)")

    def view_rear(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            try: Gui.ActiveDocument.ActiveView.viewRear()
            except: 
                try: Gui.ActiveDocument.ActiveView.viewBack()
                except: pass
            self.fit_all()
            self.lbl_status.setText("🔙 Rear View (Mặt Sau — Phím 5)")

    def fit_all(self):
        if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
            Gui.ActiveDocument.ActiveView.fitAll()
            Gui.SendMsgToActiveView("ViewFit")

def run_view_manager():
    if not App.ActiveDocument:
        QtWidgets.QMessageBox.warning(None, "WT3D", "Vui lòng mở một mô hình 3D trong FreeCAD trước!")
        return

    main_win = Gui.getMainWindow()
    dock_name = "WT3D_ViewManager_Dock"

    for child in main_win.findChildren(QtWidgets.QDockWidget):
        if child.objectName() == dock_name:
            main_win.removeDockWidget(child)
            child.deleteLater()

    dock = QtWidgets.QDockWidget("🎯 WT3D Master Pro Studio V13.0", main_win)
    dock.setObjectName(dock_name)
    dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
    
    widget = WT3DProViewWidget(dock)
    dock.setWidget(widget)
    
    main_win.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
    dock.show()
    dock.raise_()
    print("✅ Đã kích hoạt WT3D Master Pro Studio V13.0 (Align To Selection Native)!")

if __name__ == "__main__" or "FreeCAD" in sys.modules:
    run_view_manager()
