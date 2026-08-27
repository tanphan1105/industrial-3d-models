# -*- coding: utf-8 -*-
"""
=============================================================================
WT3D_FreeCAD_Auto_Render_Engine.py
Hệ Thống Tự Động Hóa Chụp Ảnh 4K & Quay Video 360° Cho FreeCAD 1.1
Dự Án: WaterTreatment3D (WT3D_Project) - Tác giả: Phan Trọng Tấn
=============================================================================
"""

import os
import sys
import math
import subprocess
import time

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except ImportError:
    print("[ERROR] Script này phải được chạy bên trong FreeCAD hoặc qua FreeCADCmd.exe!")
    sys.exit(1)

def run_wt3d_render_pipeline(output_dir=None, export_video=True, total_frames=180, fps=60):
    doc = App.ActiveDocument
    if not doc:
        print("[ERROR] Không có file mô hình nào đang mở trong FreeCAD!")
        return

    # Xác định thư mục xuất file
    if not output_dir:
        doc_path = doc.FileName
        if doc_path and os.path.exists(doc_path):
            base_dir = os.path.dirname(doc_path)
            output_dir = os.path.join(base_dir, "06_Renders_and_Media")
        else:
            output_dir = "D:/WT3D_Project/Render_Output"

    img_4k_dir = os.path.join(output_dir, "01_4K_Images")
    video_dir = os.path.join(output_dir, "02_Videos_16x9")
    frames_dir = os.path.join(output_dir, "_temp_frames_360")

    os.makedirs(img_4k_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)

    view = Gui.ActiveDocument.ActiveView
    if not view:
        print("[ERROR] Không tìm thấy 3D Active View!")
        return

    print("=========================================================")
    print(f"🚀 BẮT ĐẦU PIPELINE RENDER TỰ ĐỘNG CHO: {doc.Label}")
    print(f"📂 Thư mục xuất: {output_dir}")
    print("=========================================================")

    # Bật chế độ hiển thị bóng mờ mượt mà
    try:
        view.viewIsometric()
        view.fitAll()
    except Exception as e:
        print(f"[WARN] FitView: {e}")

    # 1. BỘ 6 ẢNH KỸ THUẬT 4K SOLID SHADED
    print("\n📸 [BƯỚC 1/3] Đang chụp bộ ảnh 4K Solid (3840x2160)...")
    solid_views = [
        ("01_Isometric_Front_4K", (1, -1, 1), (0, 0, 1)),
        ("02_Front_View_4K", (0, -1, 0), (0, 0, 1)),
        ("03_Top_View_4K", (0, 0, 1), (0, 1, 0)),
        ("04_Right_View_4K", (1, 0, 0), (0, 0, 1)),
        ("05_Left_View_4K", (-1, 0, 0), (0, 0, 1)),
        ("06_Isometric_Back_4K", (-1, 1, 1), (0, 0, 1))
    ]

    for name, dir_vec, up_vec in solid_views:
        view.setViewDirection(App.Vector(*dir_vec))
        view.setUpDirection(App.Vector(*up_vec))
        view.fitAll()
        img_path = os.path.join(img_4k_dir, f"{name}.png")
        view.saveImage(img_path, 3840, 2160, "White")
        print(f"  ✓ Đã lưu: {img_path}")

    # 2. BỘ 2 ẢNH 4K WIREFRAME (KHUNG DÂY NGHỆ THUẬT BÁN SÀN)
    print("\n📐 [BƯỚC 2/3] Đang chụp bộ ảnh 4K Wireframe...")
    try:
        # Chuyển chế độ sang Wireframe
        Gui.runCommand("Std_DrawStyle", 2)  # 2: Wireframe mode
        
        wireframe_views = [
            ("07_Isometric_Wireframe_4K", (1, -1, 1), (0, 0, 1)),
            ("08_Front_Wireframe_4K", (0, -1, 0), (0, 0, 1))
        ]
        for name, dir_vec, up_vec in wireframe_views:
            view.setViewDirection(App.Vector(*dir_vec))
            view.setUpDirection(App.Vector(*up_vec))
            view.fitAll()
            img_path = os.path.join(img_4k_dir, f"{name}.png")
            view.saveImage(img_path, 3840, 2160, "White")
            print(f"  ✓ Đã lưu Wireframe: {img_path}")
            
        # Trả về chế độ As Is / Shaded
        Gui.runCommand("Std_DrawStyle", 0)  # 0: As Is
    except Exception as e:
        print(f"[WARN] Wireframe render: {e}")
        try:
            Gui.runCommand("Std_DrawStyle", 0)
        except Exception:
            pass

    # 3. RENDER VIDEO XOAY 360° (TURNTABLE 360 2K 60FPS)
    if export_video:
        print(f"\n🎬 [BƯỚC 3/3] Đang render {total_frames} khung hình xoay 360° (2560x1440 2K)...")
        camera_elevation = math.radians(25)  # Nghiêng 25 độ nhìn từ trên xuống

        for frame in range(total_frames):
            theta = math.radians(frame * (360.0 / total_frames))
            x = math.cos(theta) * math.cos(camera_elevation)
            y = math.sin(theta) * math.cos(camera_elevation)
            z = math.sin(camera_elevation)

            view.setViewDirection(App.Vector(x, y, z))
            view.setUpDirection(App.Vector(0, 0, 1))
            
            frame_path = os.path.join(frames_dir, f"frame_{frame:04d}.png")
            view.saveImage(frame_path, 2560, 1440, "White")
            if frame % 30 == 0 or frame == total_frames - 1:
                print(f"  -> Tiến độ khung hình: {frame+1}/{total_frames}")

        # Tìm FFmpeg
        ffmpeg_exe = r"D:\WT3D_Project\Z_Tools\ffmpeg\ffmpeg.exe"
        if not os.path.exists(ffmpeg_exe):
            ffmpeg_exe = "ffmpeg"

        output_video = os.path.join(video_dir, f"WT3D_{doc.Label}_Turntable_360_2K.mp4")
        print("\n⚙️ Đang mã hóa video siêu nét bằng FFmpeg (H.264 60fps CRF=17)...")

        cmd = [
            ffmpeg_exe, "-y",
            "-framerate", str(fps),
            "-i", os.path.join(frames_dir, "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "slow",
            "-crf", "17",
            output_video
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0:
            print(f"🎉 XUẤT BẢN VIDEO THÀNH CÔNG: {output_video}")
            # Dọn dẹp frame tạm
            try:
                for f in os.listdir(frames_dir):
                    os.remove(os.path.join(frames_dir, f))
                os.rmdir(frames_dir)
            except Exception:
                pass
        else:
            print(f"[ERROR] FFmpeg error: {res.stderr.decode('utf-8', errors='ignore')}")

    print("\n=========================================================")
    print("✅ TOÀN BỘ QUÁ TRÌNH TỰ ĐỘNG HÓA 4K & VIDEO ĐÃ HOÀN TẤT!")
    print("=========================================================")

if __name__ == "__main__" or "FreeCAD" in sys.modules:
    run_wt3d_render_pipeline()
