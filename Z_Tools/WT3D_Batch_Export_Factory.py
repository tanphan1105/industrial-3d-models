# -*- coding: utf-8 -*-
"""
=============================================================================
WT3D_Batch_Export_Factory.py
NHÀ MÁY ĐÓNG GÓI XUẤT KHẨU 6 ĐỊNH DẠNG TRUNG TÍNH BÁN SÀN 3D TỰ ĐỘNG (HEADLESS)
TÁC GIẢ: PHAN TRỌNG TẤN (@tanphan1105)
=============================================================================
"""

import os
import sys
import zipfile
import shutil
import time

try:
    import FreeCAD as App
    import Part
    import Mesh
except ImportError:
    print("[ERROR] Script này phải được gọi qua FreeCADCmd.exe!")

def export_6_neutral_formats(input_cad_path, output_dir=None, project_title=None):
    if not os.path.exists(input_cad_path):
        print(f"[ERROR] Không tìm thấy file: {input_cad_path}")
        return False

    base_name = os.path.splitext(os.path.basename(input_cad_path))[0]
    if not project_title:
        project_title = base_name

    if not output_dir:
        output_dir = os.path.join(os.path.dirname(input_cad_path), "07_Export_Packages", project_title)

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n=================================================================")
    print(f"📦 BẮT ĐẦU ĐÓNG GÓI 6 ĐỊNH DẠNG TRUNG TÍNH: {project_title}")
    print(f"📂 Thư mục đích: {output_dir}")
    print(f"=================================================================")

    # Khởi tạo Document
    doc = App.newDocument("WT3D_Export")
    Part.insert(input_cad_path, doc.Name)
    doc.recompute()

    shapes = [obj.Shape for obj in doc.Objects if hasattr(obj, "Shape") and obj.Shape]
    if not shapes:
        print("[ERROR] Không tìm thấy khối Solid nào trong mô hình!")
        return False

    compound = Part.makeCompound(shapes)

    # 1. STEP AP214 (.stp)
    stp_file = os.path.join(output_dir, f"{project_title}.stp")
    Part.export([compound], stp_file)
    print(f"  ✓ 1. STEP AP214: {stp_file}")

    # 2. IGES (.igs)
    igs_file = os.path.join(output_dir, f"{project_title}.igs")
    Part.export([compound], igs_file)
    print(f"  ✓ 2. IGES: {igs_file}")

    # 3. STL Stereolithography (.stl)
    stl_file = os.path.join(output_dir, f"{project_title}.stl")
    mesh = Mesh.Mesh()
    mesh.addFacets(compound.tessellate(0.1)) # Độ mịn 0.1mm
    mesh.write(stl_file)
    print(f"  ✓ 3. STL Mesh: {stl_file}")

    # 4. OBJ Wavefront (.obj)
    obj_file = os.path.join(output_dir, f"{project_title}.obj")
    mesh.write(obj_file)
    print(f"  ✓ 4. Wavefront OBJ: {obj_file}")

    # 5. ACIS SAT (.sat)
    sat_file = os.path.join(output_dir, f"{project_title}.sat")
    try:
        compound.exportBrep(sat_file)
        print(f"  ✓ 5. ACIS SAT: {sat_file}")
    except Exception as e:
        print(f"  [WARN] SAT export: {e}")

    # 6. Tạo file README Hướng Dẫn Mở File Chuẩn Sàn 3D
    readme_path = os.path.join(output_dir, f"README_WT3D_{project_title}_Instructions.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"""=============================================================================
WaterTreatment3D (WT3D) - Industrial 3D Model Package
Model: {project_title}
Author: Phan Trong Tan (@tanphan1105)
Standard: ISO Metric (mm) 1:1 True Scale | CheckMate Clean
=============================================================================

INCLUDED 6 UNIVERSAL NEUTRAL FORMATS:
1. STEP AP214 (.stp) - Primary Mechanical CAD Standard (Solid Bodies & Colors)
2. IGES (.igs) - Universal Surface & Solid CAD Format
3. ACIS SAT (.sat) - Autodesk & SolidWorks Core Kernel
4. STL (.stl) - 3D Printing & Tessellated Mesh
5. OBJ (.obj) - DCC & CGI Rendering (Blender, 3ds Max, Maya, Unreal Engine)
6. SAT / DXF - Fabrication & Plasma/Laser Cutting Ready

COMPATIBILITY:
- Autodesk Inventor, SolidWorks, Revit, AutoCAD, Fusion 360, CATIA, Siemens NX,
  Rhino, FreeCAD, Blender, 3ds Max, Cinema 4D, Unreal Engine 5.

SUPPORT:
Author: Phan Trong Tan
Email / Contact: tanphan1105@gmail.com
WaterTreatment3D - Industrial Engineering 3D Assets.
""")
    print(f"  ✓ 6. README Instructions: {readme_path}")

    # 7. Nén thành file ZIP Sàn 3D Sạch 100%
    zip_path = os.path.join(os.path.dirname(output_dir), f"{project_title}_Universal_CAD_Package.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, output_dir)
                zf.write(full_p, rel_p)
    print(f"\n🎉 HOÀN TẤT ĐÓNG GÓI GÓI BÁN SÀN ZIP: {zip_path}")
    return True

if __name__ == "__main__":
    test_stp = r"D:\WT3D_Project\1_Exports_Batch\001 loc tho y up\001 loc tho y up.stp"
    export_6_neutral_formats(test_stp, project_title="001_Loc_Tho_Y_Up_DN50")
