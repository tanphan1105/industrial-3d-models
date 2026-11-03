import bpy
import gc
import mathutils
import sys
import traceback
import os
import json
import re
import glob
import shlex

tools_dir = os.path.dirname(os.path.abspath(__file__))
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

import wt3d_pbr_and_decal_master as pbr_decal
import wt3d_component_passport_manager as comp_passport

# Disable _wt3d_auto_sync_imported_materials depsgraph handler during batch export so EU Realistic materials are not overwritten
try:
    bpy.app.handlers.depsgraph_update_post.clear()
except Exception:
    pass


def _keep_only_resolvable_mtl_maps(mtl_path, log):
    """Keep valid Inventor texture links; remove unresolved maps; and enrich transparent MTL blocks with Tr/Tf/Ni/illum 4."""
    with open(mtl_path, "r", encoding="utf-8", errors="replace") as material_file:
        lines = material_file.readlines()

    material_dir = os.path.dirname(mtl_path)
    kept, removed, clean_lines = 0, 0, []
    metal_textured_mtls = set()
    cur_mtl_scan = ""
    texture_prefixes = ("map_", "bump ", "refl ")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("newmtl "):
            cur_mtl_scan = stripped[7:].strip()
        if not stripped.lower().startswith(texture_prefixes):
            clean_lines.append(line)
            continue
        low_s = stripped.lower()
        if any(k in low_s for k in ("steelplt", "stainless", "metals.", "ornamental", "chrome", "aluminum")):
            if cur_mtl_scan:
                metal_textured_mtls.add(cur_mtl_scan)
        if "wt3d_b3_tmp" in low_s or any(k in low_s for k in ("steelplt", "stainless", "metals.", "ornamental")):
            removed += 1
            log.write(f"Removed temporary ATF texture reference ({cur_mtl_scan}): {stripped}\n")
            continue
        try:
            tokens = shlex.split(stripped, posix=False)
            texture_ref = tokens[-1].strip('"') if tokens else ""
            texture_path = texture_ref if os.path.isabs(texture_ref) else os.path.join(material_dir, texture_ref)
            if texture_ref and os.path.isfile(texture_path):
                clean_lines.append(line)
                kept += 1
            else:
                removed += 1
                log.write(f"Removed unresolved MTL texture reference: {texture_ref}\n")
        except Exception:
            removed += 1
            log.write(f"Removed unreadable MTL texture reference: {stripped}\n")

    # Enrich each material block so transparent / clear materials have full MTL optical tags (d, Tr, Tf, Ni, illum 4)
    blocks = []
    cur_block = []
    for ln in clean_lines:
        if ln.strip().startswith("newmtl ") and cur_block:
            blocks.append(cur_block)
            cur_block = [ln]
        else:
            cur_block.append(ln)
    if cur_block:
        blocks.append(cur_block)

    enriched_lines = []
    for blk in blocks:
        header = blk[0].strip()
        if not header.startswith("newmtl "):
            enriched_lines.extend(blk)
            continue
        mat_name = header[7:].strip()
        rgb = pbr_decal._parse_rgb_from_mat_name(mat_name)
        name_lower = mat_name.lower()
        is_clear_kw = any(k in name_lower for k in ("clear", "glass", "transpar", "acrylic", "polycarbonate", "rotameter", "sight", "_trans"))
        d_val = 1.0
        for ln in blk:
            s = ln.strip()
            if s.startswith("d "):
                try:
                    d_val = float(s.split()[1])
                except Exception:
                    pass
        if d_val >= 0.98 and (rgb in pbr_decal.TRANSLUCENT_FORCE_RGB or is_clear_kw):
            d_val = pbr_decal.TRANSLUCENT_FORCE_RGB.get(rgb, 0.45 if name_lower.endswith("_trans") else 0.38)

        # Unify uPVC pipe fittings in MTL to exact uPVC Slate Grey Sch80 (#5E6A76 -> Kd 0.368627 0.415686 0.462745)
        upvc_fitting_rgbs = {
            (47, 47, 47), (80, 80, 80), (89, 96, 114),
            (97, 103, 121), (110, 125, 161), (123, 124, 127), (128, 128, 128),
            (148, 166, 184), (43, 54, 119), (45, 54, 107), (46, 138, 87),
            (33, 138, 33), (78, 86, 94),
        }
        if d_val >= 0.98 and (rgb == (235, 235, 235) or mat_name in ("235,235,235", "WT3D_Pipe_Arrow_Mark", "WT3D_Flow_Arrow_White_Mat")):
            blk = [
                "Kd 0.960000 0.960000 0.960000\n" if ln.strip().startswith("Kd ") else
                "Ks 0.200000 0.200000 0.200000\n" if ln.strip().startswith("Ks ") else
                "Ns 40.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and rgb in ((48, 135, 227), (16, 105, 204)):
            blk = [
                "Kd 0.368627 0.415686 0.462745\n" if ln.strip().startswith("Kd ") else
                "Ks 0.160000 0.160000 0.160000\n" if ln.strip().startswith("Ks ") else
                "Ns 50.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb in upvc_fitting_rgbs or mat_name in ("78,86,94")):
            blk = [
                "Kd 0.368627 0.415686 0.462745\n" if ln.strip().startswith("Kd ") else
                "Ks 0.160000 0.160000 0.160000\n" if ln.strip().startswith("Ks ") else
                "Ns 50.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (mat_name in metal_textured_mtls or rgb in pbr_decal.METALLIC_STAINLESS_RGB or rgb in ((215, 220, 225), (225, 230, 235), (128, 0, 128), (255, 251, 240))):
            blk = [
                "Kd 0.784314 0.803922 0.815686\n" if ln.strip().startswith("Kd ") else
                "Ks 0.550000 0.550000 0.550000\n" if ln.strip().startswith("Ks ") else
                "Ns 70.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb == (191, 191, 191) or mat_name == "WT3D_Van10_Orig_White_Mat"):
            blk = [
                "Kd 0.847059 0.866667 0.886275\n" if ln.strip().startswith("Kd ") else
                "Ks 0.200000 0.200000 0.200000\n" if ln.strip().startswith("Ks ") else
                "Ns 45.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb == (244, 119, 33) or mat_name.startswith("244,119,33")):
            blk = [
                "Kd 0.956863 0.466667 0.129412\n" if ln.strip().startswith("Kd ") else
                "Ks 0.220000 0.220000 0.220000\n" if ln.strip().startswith("Ks ") else
                "Ns 50.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb == (214, 40, 40) or mat_name.startswith("214,40,40")):
            blk = [
                "Kd 0.839216 0.156863 0.156863\n" if ln.strip().startswith("Kd ") else
                "Ks 0.220000 0.220000 0.220000\n" if ln.strip().startswith("Ks ") else
                "Ns 50.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb == (29, 91, 158) or mat_name.startswith("29,91,158") or mat_name == "WT3D_Van10_Orig_Blue_Mat"):
            blk = [
                "Kd 0.113725 0.356863 0.619608\n" if ln.strip().startswith("Kd ") else
                "Ks 0.220000 0.220000 0.220000\n" if ln.strip().startswith("Ks ") else
                "Ns 50.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb == (170, 45, 255) or mat_name in ("WT3D_UV_Purple_LED", "170,45,255")):
            blk = [
                "Kd 0.666667 0.176471 1.000000\n" if ln.strip().startswith("Kd ") else
                "Ks 0.350000 0.350000 0.350000\n" if ln.strip().startswith("Ks ") else
                "Ns 80.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb == (155, 173, 136) or "frp" in name_lower or mat_name.startswith("155,173,136")):
            # High-Gloss Gelcoat Composite FRP Column (#5B7B54)
            blk = [
                "Kd 0.356863 0.482353 0.329412\n" if ln.strip().startswith("Kd ") else
                "Ks 0.150000 0.150000 0.150000\n" if ln.strip().startswith("Ks ") else
                "Ns 45.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and rgb == (242, 242, 255):
            blk = [
                "Kd 0.815686 0.831373 0.843137\n" if ln.strip().startswith("Kd ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and (rgb in ((42, 48, 54), (66, 74, 82)) or mat_name.startswith(("42,48,54", "66,74,82"))):
            blk = [
                "Kd 0.258824 0.290196 0.321569\n" if ln.strip().startswith("Kd ") else
                "Ks 0.160000 0.160000 0.160000\n" if ln.strip().startswith("Ks ") else
                "Ns 50.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and rgb in ((64, 64, 64), (28, 30, 33), (32, 35, 38)):
            blk = [
                "Kd 0.141176 0.156863 0.172549\n" if ln.strip().startswith("Kd ") else
                "Ks 0.120000 0.120000 0.120000\n" if ln.strip().startswith("Ks ") else
                "Ns 35.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and rgb in ((244, 246, 248), (242, 242, 255), (255, 255, 255)):
            # RO Pressure Vessels, Vessel End Caps & Electrical Cabinet: Glossy White (#F2F5F8)
            # CRITICAL FIX: Clamp Ks=0.15 and Ns=45 so OBJ viewers DO NOT render them as black chrome mirror!
            blk = [
                "Kd 0.949020 0.960784 0.972549\n" if ln.strip().startswith("Kd ") else
                "Ks 0.150000 0.150000 0.150000\n" if ln.strip().startswith("Ks ") else
                "Ns 45.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and rgb == (230, 233, 236):
            blk = [
                "Kd 0.956863 0.964706 0.972549\n" if ln.strip().startswith("Kd ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98 and rgb in ((5, 5, 5), (0, 0, 0)):
            blk = [
                "Kd 0.109804 0.117647 0.129412\n" if ln.strip().startswith("Kd ") else
                "Ks 0.150000 0.150000 0.150000\n" if ln.strip().startswith("Ks ") else
                "Ns 40.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]
        elif d_val >= 0.98:
            # Universal Poka-Yoke: Keep exact Inventor Default view Kd diffuse color, but clamp ATF's Ns 1000 / Ks 1.0 mirror glare!
            blk = [
                "Ks 0.220000 0.220000 0.220000\n" if ln.strip().startswith("Ks ") else
                "Ns 55.000000\n" if ln.strip().startswith("Ns ") else ln
                for ln in blk
            ]

        # Universal Final Poka-Yoke on every opaque/translucent MTL block:
        # Never allow Autodesk ATF's raw 'Ns 1000.000000' or 'Ks 1.000000 1.000000 1.000000' to survive in .mtl!
        clamped_blk = []
        for ln in blk:
            s_ln = ln.strip()
            if s_ln.startswith("Ns "):
                try:
                    ns_v = float(s_ln.split()[1])
                    if ns_v > 85.0:
                        ln = "Ns 55.000000\n"
                except Exception:
                    ln = "Ns 55.000000\n"
            elif s_ln.startswith("Ks "):
                try:
                    ks_parts = [float(x) for x in s_ln.split()[1:4]]
                    if max(ks_parts) > 0.60:
                        ln = "Ks 0.220000 0.220000 0.220000\n"
                except Exception:
                    ln = "Ks 0.220000 0.220000 0.220000\n"
            clamped_blk.append(ln)
        blk = clamped_blk

        if d_val < 0.98:
            tr_val = round(1.0 - d_val, 6)
            new_blk = []
            for ln in blk:
                s = ln.strip()
                if s.startswith(("Tr ", "Tf ", "Ni ", "illum ")):
                    continue
                elif s.startswith("d "):
                    new_blk.append(f"d {d_val:.6f}\n")
                    new_blk.append(f"Tr {tr_val:.6f}\n")
                    new_blk.append(f"Tf {tr_val:.6f} {tr_val:.6f} {tr_val:.6f}\n")
                    new_blk.append("Ni 1.490000\n")
                    new_blk.append("illum 4\n")
                else:
                    new_blk.append(ln)
            enriched_lines.extend(new_blk)
        else:
            enriched_lines.extend(blk)

    with open(mtl_path, "w", encoding="utf-8") as material_file:
        material_file.writelines(enriched_lines)
    log.write(f"MTL texture references preserved={kept}, removed_unresolved={removed}\n")


def _scale_obj_vertices_in_place(obj_path, scale, log):
    """Scale vertex coordinates ('v x y z') in OBJ file by `scale` and normalize to Bottom-Center Origin (0,0,0)."""
    if not os.path.isfile(obj_path):
        return
    try:
        with open(obj_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        verts = [None]
        used_v = set()
        for line in lines:
            if line.startswith("v "):
                parts = line.split()
                if len(parts) >= 4:
                    verts.append((float(parts[1]) * scale, float(parts[2]) * scale, float(parts[3]) * scale))
                else:
                    verts.append((0.0, 0.0, 0.0))
            elif line.startswith("f "):
                for tok in line.split()[1:]:
                    vi = int(tok.split("/")[0])
                    used_v.add(vi if vi > 0 else len(verts) + vi)

        active_coords = [verts[i] for i in used_v if 0 < i < len(verts)] or verts[1:]
        if not active_coords:
            return
        min_vx = min(c[0] for c in active_coords); max_vx = max(c[0] for c in active_coords)
        min_vy = min(c[1] for c in active_coords); max_vy = max(c[1] for c in active_coords)
        min_vz = min(c[2] for c in active_coords); max_vz = max(c[2] for c in active_coords)
        shift_x = -(min_vx + max_vx) * 0.5
        shift_y = -min_vy
        shift_z = -(min_vz + max_vz) * 0.5

        out_lines = []
        v_scaled = 0
        for line in lines:
            if line.startswith("v "):
                parts = line.split()
                if len(parts) >= 4:
                    vx = float(parts[1]) * scale + shift_x
                    vy = float(parts[2]) * scale + shift_y
                    vz = float(parts[3]) * scale + shift_z
                    rest = (" " + " ".join(parts[4:])) if len(parts) > 4 else ""
                    out_lines.append(f"v {vx:.6f} {vy:.6f} {vz:.6f}{rest}\n")
                    v_scaled += 1
                else:
                    out_lines.append(line)
            else:
                out_lines.append(line)
        with open(obj_path, "w", encoding="utf-8") as f:
            f.writelines(out_lines)
        log.write(f"Normalized {v_scaled:,} OBJ vertices (scale={scale}, Bottom-Center Origin 0,0,0).\n")
    except Exception as ex:
        log.write(f"OBJ vertex scale/origin warning: {ex}\n")


def _ensure_pipe_segment_mtl(mtl_path, log):
    """Ensure canonical Schedule 80 Straight Pipe material (`48,135,227`) exists in `mtl_path`."""
    if not os.path.isfile(mtl_path):
        return
    try:
        with open(mtl_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        if any(ln.strip() == "newmtl 48,135,227" for ln in lines):
            return
        with open(mtl_path, "a", encoding="utf-8") as f:
            f.write("\nnewmtl 48,135,227\nKa 0.313725 0.352941 0.407843\nKd 0.313725 0.352941 0.407843\nKs 0.250000 0.250000 0.250000\nNs 35.000000\nd 1.000000\nillum 2\n")
        log.write("Created canonical Schedule 80 Pipe Segment MTL: 48,135,227\n")
    except Exception as ex:
        log.write(f"Pipe segment MTL warning: {ex}\n")


def _ensure_transparent_mtl_variant(mtl_path, orig_mtl, log):
    """Ensure `<orig_mtl>_trans` exists in `mtl_path` with `d 0.450000` (Inventor Transparent mode)."""
    if not os.path.isfile(mtl_path):
        return
    trans_name = f"{orig_mtl}_trans"
    try:
        with open(mtl_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        if any(ln.strip() == f"newmtl {trans_name}" for ln in lines):
            return
        # Find orig_mtl block
        block = []
        in_orig = False
        for ln in lines:
            s = ln.strip()
            if s.startswith("newmtl "):
                if in_orig:
                    break
                if s == f"newmtl {orig_mtl}":
                    in_orig = True
                    block.append(f"newmtl {trans_name}\n")
                    continue
            elif in_orig:
                if s.startswith("d "):
                    val = float(s.split()[1])
                    block.append(f"d {min(val, 0.45):.6f}\n")
                else:
                    block.append(ln)
        if block:
            with open(mtl_path, "a", encoding="utf-8") as f:
                f.write("\n" + "".join(block))
            log.write(f"Created transparent MTL variant: {trans_name} (d=0.45)\n")
    except Exception as ex:
        log.write(f"Transparent MTL variant warning: {ex}\n")


def _apply_passport_studio_to_obj_and_mtl(obj_path, passport_payload, log):
    """
    Synchronizes exported Wavefront .obj and .mtl on disk with Studio V2.8 Component Passport
    AFTER Blender has imported the raw OBJ (so internal face islands are preserved during import).
    """
    if not os.path.isfile(obj_path) or not passport_payload:
        return
    vis_bodies = passport_payload.get("visible_bodies") or []
    if not vis_bodies:
        return
    mtl_path = os.path.splitext(obj_path)[0] + ".mtl"

    uniform_roles = {
        "SKID_FRAME", "PIPE_SEGMENT", "FITTING_UPVC", "FITTING_THREADED",
        "UNION_RACCO_BODY", "UNION_RACCO_RIB", "UNION_RACCO_ORING", "FITTING_NIPPLE_SS304",
        "PIPE_CLAMP_BODY", "PIPE_CLAMP_BOLT", "FASTENER_ISO", "CABLE_TRAY",
        "VALVE_BALL", "VALVE_GLOBE", "VALVE_CHECK", "VALVE_HANDLE",
        "FILTER_7CORE_SHELL", "FILTER_7CORE", "UF_HOUSING", "RO_VESSEL", "CASTER_AND_RUBBER",
    }

    by_comp_id = {it.get("comp_id"): it for it in vis_bodies if it.get("comp_id")}
    needed_mtl_defs = {}

    try:
        with open(obj_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        cur_tag = ""
        changed_usemtl = 0
        for i, ln in enumerate(lines):
            if ln.startswith("g COMP_"):
                cid = ln[2:].strip().split("__")[0]
                it = by_comp_id.get(cid)
                if it:
                    role = it.get("role", "")
                    tag = it.get("mat_slot_tag", "")
                    if tag and (role in uniform_roles or tag in ("WT3D_Clear_Housing", "WT3D_UV_Purple_LED")):
                        cur_tag = tag
                        needed_mtl_defs[tag] = it
                    else:
                        cur_tag = ""
                else:
                    cur_tag = ""
            elif ln.startswith("g "):
                cur_tag = ""
            elif ln.startswith("usemtl ") and cur_tag:
                lines[i] = f"usemtl {cur_tag}\n"
                changed_usemtl += 1

        if False and changed_usemtl > 0:
            with open(obj_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

        if os.path.isfile(mtl_path) and needed_mtl_defs:
            with open(mtl_path, "r", encoding="utf-8", errors="replace") as f:
                mtl_lines = f.readlines()
            existing_mtls = {ln.strip()[7:].strip() for ln in mtl_lines if ln.strip().startswith("newmtl ")}
            append_blocks = []
            for tag, it in needed_mtl_defs.items():
                if tag in existing_mtls:
                    continue
                h = (it.get("pbr_hex") or "#CCCCCC").lstrip("#")
                r = int(h[0:2], 16) / 255.0 if len(h) == 6 else 0.8
                g = int(h[2:4], 16) / 255.0 if len(h) == 6 else 0.8
                b = int(h[4:6], 16) / 255.0 if len(h) == 6 else 0.8
                op = float(it.get("opacity", 1.0))
                rough = float(it.get("roughness", 0.20))
                met = float(it.get("metallic", 0.0))
                ns = max(10.0, ((1.0 - rough) * 10.0) ** 2)
                ks = 0.85 if met >= 0.5 else 0.35
                illum = 4 if op < 0.98 else 2
                append_blocks.append(
                    f"\nnewmtl {tag}\n"
                    f"Ka {r:.6f} {g:.6f} {b:.6f}\n"
                    f"Kd {r:.6f} {g:.6f} {b:.6f}\n"
                    f"Ks {ks:.6f} {ks:.6f} {ks:.6f}\n"
                    f"Ns {ns:.6f}\n"
                    f"Ni {float(it.get('ior', 1.50)):.6f}\n"
                    f"d {op:.6f}\n"
                    f"illum {illum}\n"
                )
            if append_blocks:
                with open(mtl_path, "a", encoding="utf-8") as f:
                    f.write("".join(append_blocks))
        log.write(f"Synchronized Studio V2.8 Passport materials into OBJ/MTL ({changed_usemtl} groups).\n")
    except Exception as ex:
        log.write(f"OBJ/MTL Studio V2.8 sync warning: {ex}\n")


def _strip_hidden_obj_groups(obj_path, hidden_json_path, log):
    """Remove OBJ groups ('g Solid*') that correspond to hidden Inventor occurrences/bodies."""
    if not os.path.isfile(hidden_json_path) or not os.path.isfile(obj_path):
        return 0
    try:
        with open(hidden_json_path, "r", encoding="utf-8") as jf:
            manifest = json.loads(jf.read(), strict=False)
    except Exception as ex:
        log.write(f"Hidden manifest read warning: {ex}\n")
        return 0

    if isinstance(manifest, list):
        hidden_bodies = manifest
        visible_bodies = []
        transparent_bodies = []
    elif isinstance(manifest, dict):
        hidden_bodies = manifest.get("hidden_bodies") or []
        visible_bodies = manifest.get("visible_bodies") or []
        raw_trans = manifest.get("transparent_bodies") or []
        transparent_bodies = [
            tb for tb in raw_trans
            if 0.01 < float(tb.get("opacity", 1.0)) < 0.98
            or any(k in (tb.get("occ_name") or "").lower() for k in ("2 than phin loc", "vo uv aquapro", "ong thach anh"))
        ]
    else:
        return 0

    if not hidden_bodies and not transparent_bodies and not visible_bodies:
        return 0

    def _bbox_match(b_min, b_max, t_min, t_max, tol=2.0):
        return (
            abs(b_min[0] - t_min[0]) <= tol and abs(b_min[1] - t_min[1]) <= tol and abs(b_min[2] - t_min[2]) <= tol and
            abs(b_max[0] - t_max[0]) <= tol and abs(b_max[1] - t_max[1]) <= tol and abs(b_max[2] - t_max[2]) <= tol
        )

    def _bbox_rotated_match(g_min, g_max, t_min, t_max, tol=3.0):
        """Fallback when t_min/t_max came from rotated B-Rep sb.RangeBox (which inflates rotated 45-deg elbows by up to 45mm)."""
        for i in range(3):
            if g_min[i] < t_min[i] - tol or g_max[i] > t_max[i] + tol:
                return False
            t_span = max(t_max[i] - t_min[i], 1e-6)
            g_span = max(g_max[i] - g_min[i], 0.0)
            if g_span < t_span * 0.50:
                return False
        tight_axes = sum(1 for i in range(3) if abs(g_min[i] - t_min[i]) <= tol and abs(g_max[i] - t_max[i]) <= tol)
        return tight_axes >= 1

    with open(obj_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    verts = [None]
    groups = []  # list of (g_name, base_name, start_line_idx, end_line_idx, min_pt, max_pt, has_faces)
    cur_g = None
    cur_start = 0
    cur_min = [1e18, 1e18, 1e18]
    cur_max = [-1e18, -1e18, -1e18]
    cur_has_faces = False

    for idx, line in enumerate(lines):
        if line.startswith("v "):
            parts = line.split()
            if len(parts) >= 4:
                verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
            else:
                verts.append((0.0, 0.0, 0.0))
        elif line.startswith("g "):
            if cur_g is not None:
                base_n = cur_g[2:].strip().split(":")[0]
                groups.append((cur_g, base_n, cur_start, idx, cur_min, cur_max, cur_has_faces))
            cur_g = line.strip()
            cur_start = idx
            cur_min = [1e18, 1e18, 1e18]
            cur_max = [-1e18, -1e18, -1e18]
            cur_has_faces = False
        elif line.startswith("f ") and cur_g is not None:
            cur_has_faces = True
            for tok in line.split()[1:]:
                vi = int(tok.split("/")[0])
                v = verts[vi] if vi > 0 else verts[len(verts) + vi]
                if v[0] < cur_min[0]: cur_min[0] = v[0]
                if v[1] < cur_min[1]: cur_min[1] = v[1]
                if v[2] < cur_min[2]: cur_min[2] = v[2]
                if v[0] > cur_max[0]: cur_max[0] = v[0]
                if v[1] > cur_max[1]: cur_max[1] = v[1]
                if v[2] > cur_max[2]: cur_max[2] = v[2]

    if cur_g is not None:
        base_n = cur_g[2:].strip().split(":")[0]
        groups.append((cur_g, base_n, cur_start, len(lines), cur_min, cur_max, cur_has_faces))

    # Determine scale of OBJ vertices relative to mm in manifest
    all_max_span = 0.0
    for _, _, _, _, gmin, gmax, has_f in groups:
        if has_f:
            all_max_span = max(all_max_span, gmax[0] - gmin[0], gmax[1] - gmin[1], gmax[2] - gmin[2])
    obj_to_mm = 1.0
    if 0 < all_max_span < 10.0:
        obj_to_mm = 1000.0
    elif 10.0 <= all_max_span < 100.0:
        obj_to_mm = 10.0

    # Auto-detect if manifest bboxes were accidentally written in cm instead of mm
    manifest_max_span = 0.0
    for b in (hidden_bodies + visible_bodies):
        bmin = b.get("min") or [0, 0, 0]
        bmax = b.get("max") or [0, 0, 0]
        manifest_max_span = max(manifest_max_span, bmax[0] - bmin[0], bmax[1] - bmin[1], bmax[2] - bmin[2])
    manifest_to_mm = 10.0 if (0 < manifest_max_span < (all_max_span * obj_to_mm * 0.25)) else 1.0

    drop_ranges = []
    kept_counts_by_hid_idx = {}

    for g_name, base_n, s_idx, e_idx, gmin, gmax, has_f in groups:
        if not has_f:
            continue
        gmin_mm = [gmin[0] * obj_to_mm, gmin[1] * obj_to_mm, gmin[2] * obj_to_mm]
        gmax_mm = [gmax[0] * obj_to_mm, gmax[1] * obj_to_mm, gmax[2] * obj_to_mm]

        matched_hid = None
        for h_i, hb in enumerate(hidden_bodies):
            hb_name = (hb.get("name") or "").strip()
            if hb_name and hb_name.startswith("Solid") and base_n.startswith("Solid") and hb_name != base_n:
                continue
            hb_min = [c * manifest_to_mm for c in hb["min"]]
            hb_max = [c * manifest_to_mm for c in hb["max"]]
            if _bbox_match(gmin_mm, gmax_mm, hb_min, hb_max, tol=2.5):
                matched_hid = (h_i, hb)
                break
        if matched_hid is None:
            # Fallback for rotated B-Rep RangeBox (only if not matching any visible body tightly)
            matches_any_vis_tight = False
            for vb in visible_bodies:
                vb_name = (vb.get("name") or "").strip()
                if vb_name and vb_name.startswith("Solid") and base_n.startswith("Solid") and vb_name != base_n:
                    continue
                vb_min = [c * manifest_to_mm for c in vb["min"]]
                vb_max = [c * manifest_to_mm for c in vb["max"]]
                if _bbox_match(gmin_mm, gmax_mm, vb_min, vb_max, tol=2.5):
                    matches_any_vis_tight = True
                    break
            if not matches_any_vis_tight:
                for h_i, hb in enumerate(hidden_bodies):
                    hb_name = (hb.get("name") or "").strip()
                    if hb_name and hb_name.startswith("Solid") and base_n.startswith("Solid") and hb_name != base_n:
                        continue
                    hb_min = [c * manifest_to_mm for c in hb["min"]]
                    hb_max = [c * manifest_to_mm for c in hb["max"]]
                    if _bbox_rotated_match(gmin_mm, gmax_mm, hb_min, hb_max, tol=3.0):
                        matched_hid = (h_i, hb)
                        break

        if matched_hid is not None:
            h_i, hb = matched_hid
            # Check how many visible bodies share this exact (name, min, max)
            vis_same = 0
            for vb in visible_bodies:
                vb_name = (vb.get("name") or "").strip()
                if vb_name and vb_name.startswith("Solid") and base_n.startswith("Solid") and vb_name != base_n:
                    continue
                vb_min = [c * manifest_to_mm for c in vb["min"]]
                vb_max = [c * manifest_to_mm for c in vb["max"]]
                if _bbox_match(gmin_mm, gmax_mm, vb_min, vb_max, tol=2.5):
                    vis_same += 1
            seen_so_far = kept_counts_by_hid_idx.get(h_i, 0)
            if seen_so_far < vis_same:
                kept_counts_by_hid_idx[h_i] = seen_so_far + 1
            else:
                drop_ranges.append((s_idx, e_idx, g_name, hb.get("occ_name") or hb.get("name") or ""))
            continue

        # Check if this visible group belongs to a Tube & Pipe Runs / Pipe Segment in visible_bodies
        # so its material slot is unified to Schedule 80 Straight Pipe (`48,135,227`) without colliding with Cable Tray (`128,0,128`) or Fittings (`33,138,33`)
        if visible_bodies:
            for vb_i, vb in enumerate(visible_bodies, 1):
                vb_name = (vb.get("name") or "").strip()
                if vb_name and vb_name.startswith("Solid") and base_n.startswith("Solid") and vb_name != base_n:
                    continue
                vb_min = [c * manifest_to_mm for c in vb["min"]]
                vb_max = [c * manifest_to_mm for c in vb["max"]]
                if _bbox_match(gmin_mm, gmax_mm, vb_min, vb_max, tol=2.5):
                    vb_occ = (vb.get("occ_name") or "").upper()
                    vb_role = (vb.get("role") or "").upper()
                    comp_id = vb.get("comp_id") or f"COMP_{vb_i:04d}"
                    # Tag OBJ group header with COMP_xxxx Passport ID + semantic Inventor tree identity & role
                    clean_occ = re.sub(r'[^A-Za-z0-9_]+', '_', vb.get("occ_name") or base_n).strip('_')
                    clean_role = re.sub(r'[^A-Za-z0-9_]+', '_', vb_role or "PART").strip('_')
                    lines[s_idx] = f"g {comp_id}__{clean_role}__{clean_occ}__{base_n}\n"
                    is_pipe_seg = (
                        vb_role == "PIPE_SEGMENT"
                        or ("TUBE & PIPE RUNS" in vb_occ and "FLEXIBLE HOSE" not in vb_occ)
                        or "PIPE SEGMENT" in vb_occ
                    )
                    if False and is_pipe_seg:
                        for k in range(s_idx, e_idx):
                            if lines[k].startswith("usemtl "):
                                orig_m = lines[k][7:].strip()
                                if not orig_m.endswith("_trans") and orig_m != "48,135,227":
                                    lines[k] = "usemtl 48,135,227\n"
                                    _ensure_pipe_segment_mtl(os.path.splitext(obj_path)[0] + ".mtl", log)
                    break

        # Check if this visible group belongs to an occurrence with Inventor 'Transparent' mode enabled
        if transparent_bodies:
            for tb in transparent_bodies:
                tb_name = (tb.get("name") or "").strip()
                if tb_name and tb_name.startswith("Solid") and base_n.startswith("Solid") and tb_name != base_n:
                    continue
                tb_min = [c * manifest_to_mm for c in tb["min"]]
                tb_max = [c * manifest_to_mm for c in tb["max"]]
                if _bbox_match(gmin_mm, gmax_mm, tb_min, tb_max, tol=2.5):
                    # Mark usemtl lines inside this group to use a transparent material variant
                    for k in range(s_idx, e_idx):
                        if lines[k].startswith("usemtl "):
                            orig_mtl = lines[k][7:].strip()
                            if not orig_mtl.endswith("_trans"):
                                lines[k] = f"usemtl {orig_mtl}_trans\n"
                                _ensure_transparent_mtl_variant(os.path.splitext(obj_path)[0] + ".mtl", orig_mtl, log)
                    break

    if not drop_ranges:
        with open(obj_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return 0

    drop_line_flags = bytearray(len(lines))
    for s_idx, e_idx, g_name, occ_label in drop_ranges:
        for k in range(s_idx, e_idx):
            # Keep vertex ('v ', 'vn ', 'vt ') definitions so vertex indices of later groups never shift!
            if not lines[k].startswith(("v ", "vn ", "vt ")):
                drop_line_flags[k] = 1
        log.write(f"Excluded hidden Inventor part group from OBJ/FBX: {g_name} ({occ_label})\n")

    new_lines = [line for idx, line in enumerate(lines) if not drop_line_flags[idx]]
    with open(obj_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    log.write(f"Removed {len(drop_ranges)} hidden part group(s) from OBJ before FBX/GLB export.\n")
    return len(drop_ranges)

log_path = r"d:\WT3D_Project\1_Exports_Batch\blender_log.txt"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

with open(log_path, "w", encoding="utf-8") as log:
    try:
        log.write("Blender 4.2 LTS Headless Extraction Script Started...\n")
        argv = sys.argv
        argv = argv[argv.index("--") + 1:]
        
        input_obj = argv[0]
        output_fbx = argv[1]
        export_dir = argv[2] if len(argv) >= 3 else os.path.dirname(output_fbx)
        true_model_name = argv[3] if len(argv) >= 4 else os.path.splitext(os.path.basename(output_fbx))[0]
        log.write(f"Input OBJ: {input_obj}\nOutput FBX: {output_fbx}\nModel Name: {true_model_name}\n")
        
        bpy.ops.wm.read_factory_settings(use_empty=False)
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for m in list(bpy.data.meshes):
            bpy.data.meshes.remove(m, do_unlink=True)
        for mat in list(bpy.data.materials):
            bpy.data.materials.remove(mat, do_unlink=True)
        log.write("Importing OBJ into Blender...\n")

        # Strip any hidden Inventor occurrences/bodies & apply transparent_bodies before importing OBJ into Blender
        hidden_json_candidate = os.path.join(os.path.dirname(input_obj), "wt3d_hidden_bboxes.json")
        if os.path.exists(hidden_json_candidate):
            try:
                _strip_hidden_obj_groups(input_obj, hidden_json_candidate, log)
            except Exception as ex_hid:
                log.write(f"Hidden group filter warning: {ex_hid}\n")

        # Preserve valid Inventor texture links, remove broken paths, and enrich transparent MTL blocks (d, Tr, Tf, Ni, illum 4).
        input_mtl = os.path.splitext(input_obj)[0] + ".mtl"
        if os.path.exists(input_mtl):
            try:
                _keep_only_resolvable_mtl_maps(input_mtl, log)
            except Exception as ex_mtl:
                log.write(f"MTL texture validation warning: {ex_mtl}\n")
        
        if hasattr(bpy.ops.wm, 'obj_import'):
            bpy.ops.wm.obj_import(filepath=input_obj)
        else:
            bpy.ops.import_scene.obj(filepath=input_obj)

        # Remove any hidden objects or non-mesh objects, and remove any Edit Mode hidden polygons
        for obj in list(bpy.context.scene.objects):
            if obj.type != 'MESH' or obj.hide_get() or obj.hide_viewport or obj.hide_render:
                bpy.data.objects.remove(obj, do_unlink=True)
        for obj in list(bpy.context.scene.objects):
            if obj.type == 'MESH' and obj.data and any(p.hide for p in obj.data.polygons):
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.context.tool_settings.mesh_select_mode = (False, False, True)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.reveal(select=True)
                bpy.ops.mesh.delete(type='FACE')
                bpy.ops.object.mode_set(mode='OBJECT')
                if len(obj.data.polygons) == 0:
                    bpy.data.objects.remove(obj, do_unlink=True)

        # Rename object(s) to true_model_name and bake rotation so Z-Up is (0,0,0) in Blender
        bpy.ops.object.select_all(action='DESELECT')
        mesh_idx = 0
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.name = true_model_name if mesh_idx == 0 else f"{true_model_name}_{mesh_idx}"
                if obj.data:
                    obj.data.name = obj.name
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                mesh_idx += 1
        if mesh_idx > 0:
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
        # ==========================================
        # 1. EXTRACT PRECISE MESH STATS & DIMENSIONS
        # ==========================================
        total_verts = 0
        total_edges = 0
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
                total_edges += len(mesh.edges)
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
        
        if max_dim < 10.0:
            scale_factor = 1000.0  # meters -> mm
        elif max_dim < 100.0:
            scale_factor = 10.0    # cm -> mm
        else:
            scale_factor = 1.0     # already in mm

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
        
        log.write(f"Mesh Stats: Vertices={total_verts:,} | Edges={total_edges:,} | Polygons={total_polys:,} | Materials={total_mats}\n")
        log.write(f"Dimensions: {dim_str_mm} ({dim_str_in})\n")
        
        # ==========================================
        # 2. NORMALIZE TO BOTTOM-CENTER ORIGIN (0,0,0), EXPORT Z-UP STL (IN MM) & TRUE METERS FOR BLENDER / GLB / FBX
        # ==========================================
        if has_mesh:
            shift_bx = -(min_x + max_x) * 0.5
            shift_by = -(min_y + max_y) * 0.5
            shift_bz = -min_z
            bpy.ops.object.select_all(action='DESELECT')
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH':
                    obj.location.x += shift_bx
                    obj.location.y += shift_by
                    obj.location.z += shift_bz
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Export Z-Up Binary STL (.stl) in Millimeters (standard for 3D Slicers / CAD)
        output_stl = os.path.splitext(output_fbx)[0] + ".stl"
        try:
            if hasattr(bpy.ops.wm, 'stl_export'):
                bpy.ops.wm.stl_export(filepath=output_stl, global_scale=scale_factor)
            else:
                bpy.ops.export_mesh.stl(filepath=output_stl, global_scale=scale_factor)
            log.write(f"Z-Up STL export SUCCESS: {output_stl}\n")
        except Exception as ex_stl:
            log.write(f"STL export warning: {ex_stl}\n")

        # Convert raw mm coordinates to Blender native Meters (1 unit = 1m) so it NEVER clips in Blender/GLB/FBX viewports!
        to_meters = scale_factor * 0.001
        if abs(to_meters - 1.0) > 1e-6:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH':
                    obj.scale = (to_meters, to_meters, to_meters)
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # Also normalize the exported Wavefront OBJ vertices to true Meters (1 unit = 1m) & Bottom-Center Origin (0,0,0)!
        _scale_obj_vertices_in_place(input_obj, to_meters, log)

        # Restore 100% True-to-Inventor V3.0 Photoreal PBR Materials & 28-deg Crisp CAD Normals (Zero-Decal)
        try:
            mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
            if len(mesh_objs) > 1:
                bpy.ops.object.select_all(action='DESELECT')
                for o in mesh_objs:
                    o.select_set(True)
                bpy.context.view_layer.objects.active = mesh_objs[0]
                bpy.ops.object.join()
            pbr_cnt = pbr_decal.apply_inventor_pbr_materials()
            log.write(f"V3.0 Ultra-Photoreal PBR & 28-deg Crisp Normals Restored: {pbr_cnt} materials\n")
        except Exception as ex_pbr:
            log.write(f"PBR warning: {ex_pbr}\n")

        # Generate <ModelName>_Component_Passport.json + .csv, apply Studio V2.8 PBR, & bind ROLE__* / SUB__* Vertex Groups
        try:
            passport_manifest = None
            if os.path.exists(hidden_json_candidate):
                with open(hidden_json_candidate, "r", encoding="utf-8") as hjf:
                    passport_manifest = json.loads(hjf.read(), strict=False)
            if not passport_manifest or not passport_manifest.get("visible_bodies"):
                mesh_objs_for_pass = [o for o in bpy.context.scene.objects if o.type == 'MESH']
                if mesh_objs_for_pass:
                    passport_manifest = comp_passport.extract_passport_from_blender_mesh(mesh_objs_for_pass[0], true_model_name)
            if passport_manifest:
                s_vec = (shift_bx, shift_by, shift_bz) if has_mesh else (0.0, 0.0, 0.0)
                j_out, c_out, p_payload = comp_passport.export_component_passport_files(
                    passport_manifest, export_dir, true_model_name, shift_vec=s_vec, to_meters=to_meters
                )
                vg_cnt = comp_passport.bind_component_passport_to_blender_scene(p_payload)
                _apply_passport_studio_to_obj_and_mtl(input_obj, p_payload, log)
                log.write(f"Component Passport V2.8 exported: {j_out} & {c_out} | Bound {vg_cnt} Vertex Groups & Studio V2.8 PBR\n")
        except Exception as ex_pass:
            log.write(f"Component Passport warning: {ex_pass}\n")

        # Patch Blender's in-memory FBX Material Exporter so Fab/Sketchfab/Unreal read exact PBR properties:
        # 1) EmissiveColor = (0,0,0) when emission_strength == 0 (fixes white EmissiveColor=(1,1,1) washout in FBX)
        # 2) TransparentColor = (1-alpha, 1-alpha, 1-alpha) for all alpha < 0.98 (fixes dark blue/green housings turning opaque)
        # 3) SpecularColor = (0.90, 0.90, 0.90) for dielectrics (metallic < 0.5) so dark plastics/motors have crisp specular highlights
        try:
            from io_scene_fbx import export_fbx_bin
            from bpy_extras import node_shader_utils

            def _lin_to_srgb_c(c):
                c = max(0.0, min(1.0, float(c)))
                return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055

            def _lin_to_srgb_rgb(col):
                return (_lin_to_srgb_c(col[0]), _lin_to_srgb_c(col[1]), _lin_to_srgb_c(col[2]))

            def _wt3d_fbx_data_material_elements(root, ma, scene_data):
                ambient_color = (0.0, 0.0, 0.0)
                if scene_data.data_world:
                    ambient_color = next(iter(scene_data.data_world.keys())).color

                ma_wrap = node_shader_utils.PrincipledBSDFWrapper(ma, is_readonly=True)
                ma_key, _objs = scene_data.data_materials[ma]
                ma_type = b"Phong"

                fbx_ma = export_fbx_bin.elem_data_single_int64(root, b"Material", export_fbx_bin.get_fbx_uuid_from_key(ma_key))
                fbx_ma.add_string(export_fbx_bin.fbx_name_class(ma.name.encode(), b"Material"))
                fbx_ma.add_string(b"")

                export_fbx_bin.elem_data_single_int32(fbx_ma, b"Version", export_fbx_bin.FBX_MATERIAL_VERSION)
                export_fbx_bin.elem_data_single_string(fbx_ma, b"ShadingModel", ma_type)
                export_fbx_bin.elem_data_single_int32(fbx_ma, b"MultiLayer", 0)

                tmpl = export_fbx_bin.elem_props_template_init(scene_data.templates, b"Material")
                props = export_fbx_bin.elem_properties(fbx_ma)

                srgb_base = _lin_to_srgb_rgb(ma_wrap.base_color)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_string", b"ShadingModel", ma_type.decode())
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_color", b"DiffuseColor", srgb_base)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"DiffuseFactor", 1.0)

                em_str = float(ma_wrap.emission_strength or 0.0)
                em_col = ma_wrap.emission_color if em_str > 1e-4 else (0.0, 0.0, 0.0)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_color", b"EmissiveColor", em_col)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"EmissiveFactor", em_str)

                export_fbx_bin.elem_props_template_set(tmpl, props, "p_color", b"AmbientColor", ambient_color)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"AmbientFactor", 0.0)

                alpha_val = max(0.0, min(1.0, float(ma_wrap.alpha)))
                trans_fac = 1.0 - alpha_val
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_color", b"TransparentColor", (trans_fac, trans_fac, trans_fac))
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"TransparencyFactor", trans_fac)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"Opacity", alpha_val)

                export_fbx_bin.elem_props_template_set(tmpl, props, "p_vector_3d", b"NormalMap", (0.0, 0.0, 0.0))
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_double", b"BumpFactor", ma_wrap.normalmap_strength)

                met_val = max(0.0, min(1.0, float(ma_wrap.metallic)))
                spec_col = ma_wrap.base_color if met_val >= 0.5 else (0.90, 0.90, 0.90)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_color", b"SpecularColor", spec_col)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"SpecularFactor", ma_wrap.specular / 2.0)

                rough_val = max(0.0, min(1.0, float(ma_wrap.roughness)))
                shininess = ((1.0 - rough_val) * 10.0) ** 2
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"Shininess", shininess)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"ShininessExponent", shininess)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_color", b"ReflectionColor", ma_wrap.base_color)
                export_fbx_bin.elem_props_template_set(tmpl, props, "p_number", b"ReflectionFactor", met_val)

                export_fbx_bin.elem_props_template_finalize(tmpl, props)
                if scene_data.settings.use_custom_props:
                    export_fbx_bin.fbx_data_element_custom_properties(props, ma)

            export_fbx_bin.fbx_data_material_elements = _wt3d_fbx_data_material_elements
            log.write("Patched FBX Material Exporter for Fab/Sketchfab V3.0 PBR fidelity.\n")
        except Exception as ex_fbx_patch:
            log.write(f"FBX material patch warning: {ex_fbx_patch}\n")

        # Configure all 3D Viewports in .blend: zero clipping, Material Color shading, and framed camera matrix
        cx = 0.0
        cy = 0.0
        cz = (dim_h * 0.001) * 0.5 if has_mesh else 0.8
        max_m = max(dim_l, dim_w, dim_h) * 0.001
        ideal_dist = max(max_m * 1.85, 1.8)
        target_vec = mathutils.Vector((cx, cy, cz))
        rot_quat = mathutils.Euler((1.1, 0.0, 0.6), 'XYZ').to_quaternion()
        rot_mat = rot_quat.to_matrix().to_4x4()
        trans_mat = mathutils.Matrix.Translation(-target_vec)
        framed_view_mat = rot_mat.inverted() @ trans_mat

        # Configure Canonical 3-Point Studio Lighting (`WT3D_KeyLight`, `WT3D_FillLight`, `WT3D_RimLight`)
        # + Dual-Path Bright Inventor Slate-Blue World in the exported .blend file
        try:
            sc_b3 = bpy.context.scene
            sc_b3.view_settings.view_transform = "AgX"
            sc_b3.view_settings.look = "AgX - Medium High Contrast"
            sc_b3.view_settings.exposure = -0.15
            master_pbr_dir = r"D:\WT3D_Project\WT3D_BLENDER_MASTER"
            if os.path.isdir(master_pbr_dir) and master_pbr_dir not in sys.path:
                sys.path.insert(0, master_pbr_dir)
            import importlib
            pbr_eng = importlib.import_module("00_Smart_RealWorld_PBR_Engine")
            pbr_eng.setup_hdri_studio_world(sc_b3, hdri_strength=0.75)
        except Exception:
            pass

        try:
            r_scale = max(max_m / 2.2, 0.75)
            def _add_b3_light(lname, lpos, ltgt, lenergy, lsx, lsy, lcol):
                if lname in bpy.data.objects:
                    bpy.data.objects.remove(bpy.data.objects[lname], do_unlink=True)
                ld = bpy.data.lights.new(name=lname, type='AREA')
                ld.energy = lenergy * (r_scale ** 2.0)
                ld.shape = 'RECTANGLE'
                ld.size = lsx * r_scale
                ld.size_y = lsy * r_scale
                ld.color = lcol
                lo = bpy.data.objects.new(name=lname, object_data=ld)
                bpy.context.collection.objects.link(lo)
                lo.location = mathutils.Vector(lpos)
                d_vec = mathutils.Vector(ltgt) - mathutils.Vector(lpos)
                if d_vec.length > 1e-6:
                    lo.rotation_euler = d_vec.to_track_quat('-Z', 'Y').to_euler()
                return lo

            _add_b3_light("WT3D_KeyLight",  (-2.55 * r_scale, -2.25 * r_scale, 2.15 * r_scale), (cx, cy, cz), 180.0, 1.85, 2.55, (1.0, 0.99, 0.97))
            _add_b3_light("WT3D_FillLight", ( 2.25 * r_scale, -2.05 * r_scale, 1.55 * r_scale), (cx, cy, cz), 85.0, 1.80, 2.40, (0.95, 0.97, 1.00))
            _add_b3_light("WT3D_RimLight",  ( 0.00 * r_scale,  2.35 * r_scale, 2.45 * r_scale), (cx, cy, cz), 95.0, 2.10, 1.65, (1.0, 1.0, 1.0))
        except Exception as ex_lgt:
            log.write(f"3-Point Studio Light warning: {ex_lgt}\n")

        # Bake exact '1-Click: Môi Trường Chuẩn Inventor' into every .blend file so it opens crisp & non-glaring immediately!
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.clip_start = 0.05
                            space.clip_end = 10000.0
                            try:
                                space.shading.type = 'SOLID'
                                space.shading.light = 'STUDIO'
                                space.shading.color_type = 'MATERIAL'
                                space.shading.show_cavity = True
                                space.shading.cavity_type = 'WORLD'
                                space.shading.cavity_ridge_factor = 1.0
                                space.shading.cavity_valley_factor = 1.0
                                space.shading.show_object_outline = True
                                space.shading.object_outline_color = (0.15, 0.15, 0.15)
                                space.shading.show_shadows = False
                                space.shading.background_type = 'THEME'
                                space.shading.use_scene_lights = False
                                space.shading.use_scene_world = False
                                space.shading.studiolight_intensity = 0.85
                                space.shading.show_specular_highlight = True
                                space.shading.show_backface_culling = False
                                space.shading.show_xray = False
                            except Exception:
                                pass
                            try:
                                space.overlay.show_floor = False
                                space.overlay.show_axis_x = False
                                space.overlay.show_axis_y = False
                                space.overlay.show_ortho_grid = False
                                space.overlay.show_relationship_lines = False
                                space.overlay.show_extras = False
                            except Exception:
                                pass
                            if space.region_3d:
                                space.region_3d.view_perspective = 'PERSP'
                                space.region_3d.view_location = target_vec
                                space.region_3d.view_distance = ideal_dist
                                space.region_3d.view_rotation = rot_quat
                                space.region_3d.view_matrix = framed_view_mat

        # Save Native Blender .blend file FIRST (while ROLE__* / SUB__* Vertex Groups & wt3d_comp_index are intact)
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

        # Clear Vertex Groups and remove studio lights before exporting .fbx & .glb so exported meshes stay lightweight
        try:
            for o in list(bpy.context.scene.objects):
                if o.type == 'LIGHT':
                    bpy.data.objects.remove(o, do_unlink=True)
                elif o.type == 'MESH' and o.vertex_groups:
                    o.vertex_groups.clear()
        except Exception:
            pass

        try:
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        except Exception:
            pass
        gc.collect()
        log.write("Exporting FBX (Y-Up Standard with Embedded Studio V2.8 PBR, Visible Mesh Only)...\n")
        bpy.ops.export_scene.fbx(
            filepath=output_fbx, 
            use_selection=False, 
            use_visible=True,
            object_types={'MESH'},
            global_scale=1.0, 
            apply_unit_scale=True, 
            apply_scale_options='FBX_SCALE_ALL',
            axis_forward='-Z',
            axis_up='Y',
            bake_space_transform=True,
            mesh_smooth_type='OFF',
            use_mesh_modifiers=True,
            use_mesh_edges=False,
            use_tspace=False,
            path_mode='COPY',
            embed_textures=True
        )
        log.write("FBX export SUCCESS.\n")

        # Export glTF 2.0 Binary (.glb) in pure Y-Up Meters (Zero node rotation, True Studio V2.8 PBR)
        output_glb = os.path.splitext(output_fbx)[0] + ".glb"
        try:
            bpy.ops.export_scene.gltf(
                filepath=output_glb,
                export_format='GLB',
                use_selection=False,
                use_visible=True,
                export_yup=True,
                export_apply=True,
                export_texcoords=True,
                export_normals=True,
                export_materials='EXPORT'
            )
            log.write(f"GLB export SUCCESS: {output_glb}\n")
        except Exception as ex_glb:
            log.write(f"GLB export warning: {ex_glb}\n")

        # ==========================================
        # 2A. EXPORT EUROPEAN CLEANROOM REALISTIC EDITION (DISABLED BY USER: ONLY FAB REQUIRED FILES)
        # ==========================================
        try:
          if False:
            pbr_decal.apply_european_cleanroom_pbr_materials()
            eu_fbx = os.path.splitext(output_fbx)[0] + "_EU_Realistic.fbx"
            eu_glb = os.path.splitext(output_fbx)[0] + "_EU_Realistic.glb"
            bpy.ops.export_scene.fbx(
                filepath=eu_fbx,
                use_selection=False,
                use_visible=True,
                object_types={'MESH'},
                global_scale=1.0,
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_ALL',
                axis_forward='-Z',
                axis_up='Y',
                bake_space_transform=True,
                mesh_smooth_type='OFF',
                use_mesh_modifiers=True,
                use_mesh_edges=False,
                use_tspace=False,
                path_mode='COPY',
                embed_textures=True
            )
            bpy.ops.export_scene.gltf(
                filepath=eu_glb,
                export_format='GLB',
                use_selection=False,
                use_visible=True,
                export_yup=True,
                export_apply=True,
                export_texcoords=True,
                export_normals=True,
                export_materials='EXPORT'
            )
            # Restore A2 PBR materials for Web Shell GLB export below
            pbr_decal.apply_inventor_pbr_materials()
            log.write(f"European Cleanroom Realistic Edition exported: {eu_fbx} & {eu_glb}\n")
        except Exception as ex_eu:
            log.write(f"EU Realistic export warning: {ex_eu}\n")

        # Clean up any legacy _EU_Realistic or .blend1 files in export_dir
        for stale_pat in ("*_EU_Realistic.fbx", "*_EU_Realistic.glb", "*.blend1", "*_3D_MultiFormat_All_In_One.zip"):
            for stale_f in glob.glob(os.path.join(export_dir, stale_pat)):
                try:
                    os.remove(stale_f)
                except Exception:
                    pass

        # ==========================================
        # 2B. AUTO-EXPORT DRACO WEB SHELL GLB (06_Web_Viewer_GLB/<ModelName>_Web_Shell.glb)
        # ==========================================
        try:
            proj_root_for_web = os.path.dirname(export_dir)
            if os.path.basename(proj_root_for_web) == "06_Renders_and_Media":
                web_glb_dir = os.path.join(proj_root_for_web, "06_Web_Viewer_GLB")
            else:
                web_glb_dir = os.path.join(proj_root_for_web, "06_Renders_and_Media", "06_Web_Viewer_GLB")
            os.makedirs(web_glb_dir, exist_ok=True)
            web_shell_glb = os.path.join(web_glb_dir, f"{true_model_name}_Web_Shell.glb")

            mesh_objs_w = [o for o in bpy.context.scene.objects if o.type == 'MESH']
            if mesh_objs_w:
                shell_obj = mesh_objs_w[0]
                shell_obj.name = "WT3D_Web_Preview_Shell"
                if shell_obj.data:
                    shell_obj.data.name = "WT3D_Web_Preview_Shell_Mesh"
                bpy.ops.object.select_all(action='DESELECT')
                shell_obj.select_set(True)
                bpy.context.view_layer.objects.active = shell_obj

                bbox_w = [shell_obj.matrix_world @ mathutils.Vector(c) for c in shell_obj.bound_box]
                wx0 = min(v.x for v in bbox_w); wx1 = max(v.x for v in bbox_w)
                wy0 = min(v.y for v in bbox_w); wy1 = max(v.y for v in bbox_w)
                wz0 = min(v.z for v in bbox_w); wz1 = max(v.z for v in bbox_w)
                w_max = max(wx1 - wx0, wy1 - wy0, wz1 - wz0, 1e-5)

                w_sf = 2.0 / w_max
                shell_obj.scale = (w_sf, w_sf, w_sf)
                shell_obj.location = (-(wx0 + wx1) * 0.5 * w_sf, -(wy0 + wy1) * 0.5 * w_sf, -wz0 * w_sf)

                bpy.ops.export_scene.gltf(
                    filepath=web_shell_glb,
                    export_format='GLB',
                    use_selection=False,
                    use_visible=True,
                    export_yup=True,
                    export_apply=False,
                    export_texcoords=True,
                    export_normals=True,
                    export_materials='EXPORT',
                    export_attributes=False,
                    export_draco_mesh_compression_enable=False
                )
                log.write(f"Web Shell Draco GLB export SUCCESS: {web_shell_glb}\n")
        except Exception as ex_web_glb:
            log.write(f"Web Shell GLB warning: {ex_web_glb}\n")
        
        # ==========================================
        # 3. AUTO INJECT DIRECTLY INTO HTML STUDIO & JSON
        # ==========================================
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
                    p_data["specs"]["edges"] = total_edges
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
