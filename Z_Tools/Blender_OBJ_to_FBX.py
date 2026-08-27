import bpy
import mathutils
import sys
import traceback
import os
import json
import re
import glob

log_path = r"d:\WT3D_Project\1_Exports_Batch\blender_log.txt"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

with open(log_path, "w", encoding="utf-8") as log:
    try:
        log.write("Blender 4.2 LTS Headless Extraction Script Started...\n")
        argv = sys.argv
        argv = argv[argv.index("--") + 1:]
        
        input_obj = argv[0]
        output_fbx = argv[1]
        log.write(f"Input OBJ: {input_obj}\nOutput FBX: {output_fbx}\n")
        
        bpy.ops.wm.read_factory_settings(use_empty=True)
        log.write("Importing OBJ into Blender...\n")
        
        if hasattr(bpy.ops.wm, 'obj_import'):
            bpy.ops.wm.obj_import(filepath=input_obj)
        else:
            bpy.ops.import_scene.obj(filepath=input_obj)
            
        # ==========================================
        # 1. EXTRACT PRECISE MESH STATS & DIMENSIONS
        # ==========================================
        total_verts = 0
        total_polys = 0
        material_names = set()
        
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')
        has_mesh = False
        
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                has_mesh = True
                mesh = obj.data
                total_verts += len(mesh.vertices)
                total_polys += len(mesh.polygons)
                for mat in obj.material_slots:
                    if mat.material:
                        material_names.add(mat.material.name)
                        
                # Calculate bounding box in world space
                for corner in obj.bound_box:
                    w_pos = obj.matrix_world @ mathutils.Vector(corner)
                    min_x = min(min_x, w_pos.x)
                    max_x = max(max_x, w_pos.x)
                    min_y = min(min_y, w_pos.y)
                    max_y = max(max_y, w_pos.y)
                    min_z = min(min_z, w_pos.z)
                    max_z = max(max_z, w_pos.z)
        
        total_mats = len(material_names)
        
        # Dimensions (Inventor exports OBJ in Millimeters or Centimeters)
        raw_x = (max_x - min_x) if has_mesh else 0
        raw_y = (max_y - min_y) if has_mesh else 0
        raw_z = (max_z - min_z) if has_mesh else 0
        max_dim = max(raw_x, raw_y, raw_z)
        
        # If max dimension is in meters (< 10.0), multiply by 1000 to get mm.
        # If max dimension is in centimeters (< 100.0), multiply by 10 to get mm.
        # If max dimension is already in millimeters (>= 10.0), scale_factor is 1.0!
        if max_dim < 10.0:
            scale_factor = 1000.0  # meters -> mm
        elif max_dim < 100.0:
            scale_factor = 10.0    # cm -> mm
        else:
            scale_factor = 1.0     # already in mm

        # Sanity check: if max_dim * scale_factor exceeds 10000 mm for small components, force 1.0
        if raw_x > 50.0 and raw_y > 50.0 and raw_z > 50.0:
            scale_factor = 1.0

        dim_x_mm = round(raw_x * scale_factor)
        dim_y_mm = round(raw_y * scale_factor)
        dim_z_mm = round(raw_z * scale_factor)
        
        # Handle coordinate system orientation (Length x Width x Height)
        dim_l = max(dim_x_mm, dim_y_mm)
        dim_w = min(dim_x_mm, dim_y_mm)
        dim_h = dim_z_mm
        
        dim_str_mm = f"{dim_l:,} × {dim_w:,} × {dim_h:,} mm"
        dim_str_in = f"{round(dim_l/25.4, 1)}″ × {round(dim_w/25.4, 1)}″ × {round(dim_h/25.4, 1)}″"
        
        log.write(f"Mesh Stats: Vertices={total_verts:,} | Polygons={total_polys:,} | Materials={total_mats}\n")
        log.write(f"Dimensions: {dim_str_mm} ({dim_str_in})\n")
        
        # ==========================================
        # 2. EXPORT COMPLIANT Y-UP FBX & NATIVE .BLEND
        # ==========================================
        log.write("Exporting FBX (Y-Up Standard)...\n")
        bpy.ops.export_scene.fbx(
            filepath=output_fbx, 
            use_selection=False, 
            global_scale=1.0, 
            apply_unit_scale=True, 
            apply_scale_options='FBX_SCALE_ALL',
            mesh_smooth_type='FACE',
            use_mesh_modifiers=True,
            use_mesh_edges=False,
            use_tspace=False,
            path_mode='COPY',
            embed_textures=True
        )
        log.write("FBX export SUCCESS.\n")
        
        # Save Native Blender .blend file
        output_blend = os.path.splitext(output_fbx)[0] + ".blend"
        output_blend1 = output_blend + "1"
        try:
            bpy.ops.wm.save_as_mainfile(filepath=output_blend, compress=True)
            if os.path.exists(output_blend1):
                try:
                    os.remove(output_blend1)
                except Exception:
                    pass
            log.write(f"Native .blend export SUCCESS: {output_blend}\n")
        except Exception as ex_blend:
            log.write(f"Native .blend export warning: {ex_blend}\n")
        
        # ==========================================
        # 3. AUTO INJECT DIRECTLY INTO HTML STUDIO & JSON
        # ==========================================
        export_dir = os.path.dirname(output_fbx)
        project_root = os.path.dirname(export_dir)
        if not os.path.exists(os.path.join(project_root, "01_Assemblies")):
            # Maybe inside 06_Renders_and_Media
            if os.path.basename(project_root) == "06_Renders_and_Media":
                project_root = os.path.dirname(project_root)
                
        # Search HTML Studio files in 05_SEO_and_Marketing_Docs
        seo_docs_dir = os.path.join(project_root, "06_Renders_and_Media", "05_SEO_and_Marketing_Docs")
        html_candidates = []
        if os.path.exists(seo_docs_dir):
            html_candidates.extend(glob.glob(os.path.join(seo_docs_dir, "*Publishing_Studio*.html")))
            html_candidates.extend(glob.glob(os.path.join(seo_docs_dir, "*.html")))
        
        # Also search in project root and WT3D_Project root
        html_candidates.extend(glob.glob(os.path.join(project_root, "*Publishing_Studio*.html")))
        
        for html_file in set(html_candidates):
            try:
                with open(html_file, "r", encoding="utf-8") as hf:
                    html_content = hf.read()
                
                # Replace Dimensions / Polys / Verts in HTML content
                # 1. Update Polygons & Vertices in text
                new_html = re.sub(r'(Polygons?\s*:\s*)[\d,\.]+', rf'\g<1>{total_polys:,}', html_content, flags=re.IGNORECASE)
                new_html = re.sub(r'(Vertices?\s*:\s*)[\d,\.]+', rf'\g<1>{total_verts:,}', new_html, flags=re.IGNORECASE)
                new_html = re.sub(r'(Materials?\s*:\s*)[\d,\.]+', rf'\g<1>{total_mats}', new_html, flags=re.IGNORECASE)
                
                if new_html != html_content:
                    with open(html_file, "w", encoding="utf-8") as hf:
                        hf.write(new_html)
                    log.write(f"Successfully injected Blender specs into HTML: {html_file}\n")
            except Exception as ex_html:
                log.write(f"HTML injection warning ({html_file}): {ex_html}\n")

        # Also inject into README.txt, README_Model_Instructions.txt and README.md
        readme_candidates = [
            os.path.join(export_dir, "README.txt"),
            os.path.join(export_dir, "README_Model_Instructions.txt"),
            os.path.join(project_root, "README.md")
        ]
        for r_path in readme_candidates:
            if os.path.exists(r_path):
                try:
                    with open(r_path, "r", encoding="utf-8") as rf:
                        r_txt = rf.read()
                    
                    new_r = re.sub(r'\{{1,2}DIMENSIONS_MM\}{1,2}', f"{dim_l} x {dim_w} x {dim_h}", r_txt)
                    new_r = re.sub(r'\{{1,2}POLYGONS\}{1,2}', f"{total_polys:,}", new_r)
                    new_r = re.sub(r'\{{1,2}VERTICES\}{1,2}', f"{total_verts:,}", new_r)
                    new_r = re.sub(r'(Dimensions\s*\(L\s*x\s*W\s*x\s*H\)\s*:\s*)[^\n\r]+', rf'\g<1>{dim_l} x {dim_w} x {dim_h} mm', new_r, flags=re.IGNORECASE)
                    new_r = re.sub(r'(Polygons?\s*:\s*)[\d,\.]+', rf'\g<1>{total_polys:,}', new_r, flags=re.IGNORECASE)
                    new_r = re.sub(r'(Vertices?\s*:\s*)[\d,\.]+', rf'\g<1>{total_verts:,}', new_r, flags=re.IGNORECASE)
                    
                    if new_r != r_txt:
                        with open(r_path, "w", encoding="utf-8") as rf:
                            rf.write(new_r)
                        log.write(f"Injected specs into README: {r_path}\n")
                except Exception as ex_readme:
                    log.write(f"README injection warning ({r_path}): {ex_readme}\n")
                
        # Update JSON Master Data
        candidate_jsons = [
            os.path.join(export_dir, "project_master_data.json"),
            os.path.join(project_root, "project_master_data.json"),
            os.path.join(seo_docs_dir, "project_master_data.json") if os.path.exists(seo_docs_dir) else "",
            r"d:\WT3D_Project\Z_Tools\project_master_data.json"
        ]
        
        for json_path in candidate_jsons:
            if json_path and os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as jf:
                        p_data = json.load(jf)
                    if "specs" not in p_data:
                        p_data["specs"] = {}
                    p_data["specs"]["polygons"] = total_polys
                    p_data["specs"]["vertices"] = total_verts
                    p_data["specs"]["materials"] = total_mats
                    p_data["specs"]["dimensions_mm"] = f"{dim_l} x {dim_w} x {dim_h} mm"
                    p_data["specs"]["geometry"] = "Polygonal Mesh"
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(p_data, jf, indent=2, ensure_ascii=False)
                    log.write(f"Injected stats into JSON: {json_path}\n")
                except Exception as ex_json:
                    log.write(f"JSON injection warning ({json_path}): {ex_json}\n")

        log.write("Blender background processing completed successfully with Auto HTML Update.\n")

    except Exception as e:
        log.write("ERROR:\n")
        log.write(traceback.format_exc())

sys.exit(0)
