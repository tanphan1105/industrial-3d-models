#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
WT3D PBR MATERIAL RESTORER & 3D DECAL INJECTOR MASTER V1.0
==========================================================
1. Khôi phục 100% tính chất vật liệu PBR chuẩn Autodesk Inventor cho .blend / .glb / .fbx:
   - Sửa lỗi chí mạng của Blender `obj_import` khi đọc file `.mtl` của Inventor:
     + Inventor xuất `Ns 1000` khiến Blender đặt `Roughness = 0.0` và `Metallic = 0.0` cho mọi vật liệu.
     + Blender đặt `blend_method = 'HASHED'` (`DITHERED`) khiến glTF (.glb) xuất `alphaMode: "MASK"` (alphaCutoff=0.5),
       làm các bồn lọc/vỏ tủ trong suốt (`d = 0.52`, `d = 0.66`) bị đặc kịt 100% và ống đo lưu lượng (`d = 0.40`) bị tàng hình!
   - Tự động nhận diện bảng mã RGB chuẩn Inventor của WT3D:
     + Inox 304 / Chrome / Thép gia công (`190,188,186`, `224,223,219`, `178,178,178`, `129,130,133`): `Metallic = 0.88`, `Roughness = 0.24`.
     + Đồng thau / Brass (`203,154,59`, `191,153,15`): `Metallic = 0.90`, `Roughness = 0.22`.
     + Bồn Composite / Cửa tủ / Bầu lọc trong suốt (`d < 0.99` hoặc `1,62,241`, `16,171,74`, `77,77,250`, `229,229,229`, `236,241,239`, `47,159,195`):
       Bật `blend_method = 'BLEND'` (`surface_render_method = 'BLENDED'`), `Roughness = 0.10`, giữ nguyên độ trong suốt nhìn xuyên thấu lõi lọc bên trong!
     + Nhựa uPVC Sch80 (`123,124,127`, `128,128,128`, `97,103,121`, `89,96,114`): `Metallic = 0.0`, `Roughness = 0.26`.
     + Vỏ bồn FRP Gelcoat & Sơn tĩnh điện tủ điện (`155,173,136`, `235,235,235`, `255,255,255`, `31,31,180`...): `Roughness = 0.20 - 0.24`.
     + Cao su EPDM / Đế bồn / Đầu van Runxin (`0,0,0`, `5,5,5`, `64,64,64`): `Roughness = 0.45`.
2. Nhúng trực tiếp 3D Decal Mesh + Packed PNG Texture (`UVMap`) vào mô hình 3D:
   - Giúp khách hàng mở `.glb`, `.fbx`, `.blend` trên Web hoặc phần mềm 3D đều thấy rõ 100% tem nhãn kỹ thuật sắc nét!
"""

import bpy
import bmesh
import math
import mathutils
import os

DECAL_LIB_DIR = r"D:\WT3D_Project\Z_Tools\Decals_Library"

# Bảng phân loại mã màu RGB chuẩn Autodesk Inventor của hệ sinh thái WT3D
METALLIC_STAINLESS_RGB = {
    (190, 188, 186),
    (215, 220, 225),
    (225, 230, 235),
    (224, 223, 219),
    (180, 178, 167),
    (162, 163, 167),
    (178, 178, 178),
    (129, 130, 133),
}

METALLIC_BRASS_RGB = {
    (203, 154, 59),
    (191, 153, 15),
}

TRANSLUCENT_FORCE_RGB = {
    (1, 62, 241): 0.48,
    (16, 171, 74): 0.48,
    (77, 77, 250): 0.48,
    (102, 255, 128): 0.55,
    (178, 66, 209): 0.48,
    (215, 104, 221): 0.48,
    (229, 229, 229): 0.38,
    (236, 241, 239): 0.52,
    (250, 250, 250): 0.48,
    (212, 207, 0): 0.52,
    (47, 159, 195): 0.38,
    (77, 202, 255): 0.38,
    (114, 233, 245): 0.32,
}

CLEAR_TRANSMISSION_RGB = {
    (229, 229, 229),
    (236, 241, 239),
    (250, 250, 250),
    (47, 159, 195),
    (77, 202, 255),
    (114, 233, 245),
}

UPVC_PIPE_RGB = {
    (123, 124, 127),
    (128, 128, 128),
    (97, 103, 121),
    (89, 96, 114),
    (46, 138, 87),
}

RUBBER_MATTE_RGB = {
    (0, 0, 0),
    (5, 5, 5),
    (47, 47, 47),
    (64, 64, 64),
    (80, 80, 80),
}

GLOSS_FRP_AND_CABINET_RGB = {
    (155, 173, 136),
    (191, 187, 166),
    (197, 194, 148),
    (199, 191, 174),
    (255, 227, 181),
    (229, 226, 188),
    (212, 175, 55),
    (240, 215, 140),
    (31, 31, 180),
    (0, 102, 204),
    (25, 84, 166),
    (235, 235, 235),
    (240, 240, 238),
    (242, 242, 255),
    (244, 244, 244),
    (245, 245, 245),
    (245, 246, 246),
    (255, 251, 240),
    (255, 254, 246),
    (255, 255, 255),
    (191, 191, 191),
    (230, 233, 236),
}


def _srgb_to_linear(c):
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _hex_to_rgba(hex_str, alpha=1.0):
    h = hex_str.lstrip("#")
    r = _srgb_to_linear(int(h[0:2], 16) / 255.0)
    g = _srgb_to_linear(int(h[2:4], 16) / 255.0)
    b = _srgb_to_linear(int(h[4:6], 16) / 255.0)
    return (r, g, b, alpha)


def _rgb_tuple_to_linear(rgb, alpha=1.0):
    return (
        _srgb_to_linear(rgb[0] / 255.0),
        _srgb_to_linear(rgb[1] / 255.0),
        _srgb_to_linear(rgb[2] / 255.0),
        alpha,
    )


def _parse_rgb_from_mat_name(mat_name):
    """Trích xuất bộ (R, G, B) từ tên vật liệu kiểu '190,188,186_1' của Inventor."""
    base = mat_name.split("_")[0].split(".")[0].strip()
    parts = base.split(",")
    if len(parts) == 3:
        try:
            return (int(parts[0]), int(parts[1]), int(parts[2]))
        except ValueError:
            pass
    return None


def restore_crisp_cad_sharp_edges(angle_deg=28.0):
    """
    V3.0 Ultra-Photoreal Mesh & Normal Calibration (Zero-Decal):
    1. Xóa mọi đối tượng `WT3D_Decal_*` nếu có (100% không dùng Decal rời).
    2. Trên `Industrial_RO_System_2m3h_2Stage_8040_UF_IoT`: tự động gán 30 mặt cửa sổ cánh tủ điện
       đang mang mã `128,128,128` sang `229,229,229` (Kính cường lực trong suốt) để thấy rõ màn hình HMI bên trong.
    3. Xóa toàn bộ các mặt đa giác trùng khít tọa độ (`coplanar duplicate faces`) gây lỗi sọc đen Z-fighting
       trên vỏ màng RO 8040, cùm kẹp và mặt bích.
    4. Áp dụng `shade_smooth_by_angle(28°)` và khóa pháp tuyến bậc gờ trụ tròn để thân bồn/ống láng mịn
       nhưng các cạnh cơ khí 90° vẫn sắc nét.
    """
    # 1. Remove any stray Decal objects
    for o in list(bpy.data.objects):
        if o.name.startswith("WT3D_Decal_"):
            bpy.data.objects.remove(o, do_unlink=True)

    for obj in list(bpy.context.scene.objects):
        if obj.type != "MESH" or not obj.data:
            continue
        try:
            m = obj.data
            slot_names = [s.name for s in obj.material_slots]
            ro_idx = slot_names.index("230,233,236") if "230,233,236" in slot_names else -1
            glass_idx = slot_names.index("229,229,229") if "229,229,229" in slot_names else -1
            grey_idx = slot_names.index("128,128,128") if "128,128,128" in slot_names else -1

            bm = bmesh.new()
            bm.from_mesh(m)

            # Reassign the 30 front-window faces on the Electrical Cabinet door of RO 2m3/h to Clear Glass (229,229,229)
            if "RO_System_2m3h" in obj.name and glass_idx >= 0 and grey_idx >= 0:
                for f in bm.faces:
                    if f.material_index == grey_idx:
                        c = f.calc_center_median()
                        if -0.500 < c.x < -0.480 and 0.410 < c.y < 0.870 and 1.070 < c.z < 1.750:
                            f.material_index = glass_idx

            # Dynamically compute 8040 RO vessel axes if present (`230,233,236`)
            ro_x0 = 0.0447
            ro_z_top = 0.9665
            ro_z_bot = 0.5865
            ro_z_split = 0.7765
            if "RO_System_2m3h" in obj.name and ro_idx >= 0:
                ro_centers = [f.calc_center_median() for f in bm.faces if f.material_index == ro_idx]
                if ro_centers:
                    ro_x0 = (min(c.x for c in ro_centers) + max(c.x for c in ro_centers)) * 0.5
                    ro_z_mid_all = (min(c.z for c in ro_centers) + max(c.z for c in ro_centers)) * 0.5
                    ro_z_split = ro_z_mid_all
                    z_tops = [c.z for c in ro_centers if c.z > ro_z_split]
                    z_bots = [c.z for c in ro_centers if c.z <= ro_z_split]
                    if z_tops:
                        ro_z_top = (min(z_tops) + max(z_tops)) * 0.5
                    if z_bots:
                        ro_z_bot = (min(z_bots) + max(z_bots)) * 0.5

            # Delete exact coplanar duplicate faces (and hidden inner wall of 8040 RO vessels on RO 2m3/h)
            seen = set()
            del_faces = []
            for f in bm.faces:
                vs = tuple(sorted((round(v.co.x, 5), round(v.co.y, 5), round(v.co.z, 5)) for v in f.verts))
                if vs in seen:
                    del_faces.append(f)
                    continue
                seen.add(vs)
                if "RO_System_2m3h" in obj.name and f.material_index == ro_idx:
                    c = f.calc_center_median()
                    z0 = ro_z_top if c.z > ro_z_split else ro_z_bot
                    if abs(c.y) < 0.72 and ((c.x - ro_x0) * f.normal.x + (c.z - z0) * f.normal.z) < -0.02:
                        del_faces.append(f)

            if del_faces:
                bmesh.ops.delete(bm, geom=del_faces, context="FACES")
            # Use 15-micron (0.015mm) weld tolerance so 0.04mm thin-wall decal sleeves (`BLUE42/34/27`) never weld inner & outer walls!
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.000015)

            # Tách riêng Vòng tròn định danh trên ống (WT3D_Pipe_Arrow_Ring) & Mũi tên chỉ hướng phẳng liền mạch như Inventor (WT3D_Pipe_Arrow_Mark)
            slot_names_now = [s.name for s in obj.material_slots]
            if "WT3D_Pipe_Arrow_Mark" not in slot_names_now:
                ring_src_indices = {i for i, s in enumerate(obj.material_slots) if s.name in ("24,37,248", "34,46,248")}
                arrow_src_indices = {i for i, s in enumerate(obj.material_slots) if s.name in ("235,235,235", "255,255,255")}
                if ring_src_indices and arrow_src_indices:
                    def _get_mat_islands(target_indices):
                        seen_f = set()
                        islands_list = []
                        for f in bm.faces:
                            if f.material_index in target_indices and f not in seen_f:
                                comp = set()
                                q = [f]
                                while q:
                                    cur = q.pop()
                                    if cur in comp:
                                        continue
                                    comp.add(cur)
                                    for e in cur.edges:
                                        for nf in e.link_faces:
                                            if nf.material_index in target_indices and nf not in comp:
                                                q.append(nf)
                                seen_f |= comp
                                islands_list.append(comp)
                        return islands_list

                    isl_ring_cand = _get_mat_islands(ring_src_indices)
                    isl_arrow_cand = _get_mat_islands(arrow_src_indices)

                    def _island_bbox(comp):
                        xs = [v.co.x for f in comp for v in f.verts]
                        ys = [v.co.y for f in comp for v in f.verts]
                        zs = [v.co.z for f in comp for v in f.verts]
                        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

                    def _island_center(comp):
                        bb = _island_bbox(comp)
                        return ((bb[0] + bb[1]) * 0.5, (bb[2] + bb[3]) * 0.5, (bb[4] + bb[5]) * 0.5)

                    # Lọc các cụm Mũi tên (<= 180 mặt, kích thước < 65mm) và các Vòng tròn ôm ống (50..1200 mặt, kích thước < 160mm)
                    arrow_cands = []
                    for c in isl_arrow_cand + isl_ring_cand:
                        if len(c) <= 180:
                            bb = _island_bbox(c)
                            if max(bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]) < 0.068:
                                arrow_cands.append((c, _island_center(c)))

                    valid_rings = []
                    valid_arrows = []
                    pad = 0.004  # 4mm spatial tolerance (bắt trọn cả các mũi tên khác shell không hàn đỉnh với vòng tròn!)
                    for c_ring in isl_ring_cand + isl_arrow_cand:
                        if 50 <= len(c_ring) <= 1200:
                            bb = _island_bbox(c_ring)
                            if max(bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]) < 0.165:
                                r_mat = next(iter(c_ring)).material_index
                                matched_arrows = [
                                    c_arr for (c_arr, pt) in arrow_cands
                                    if next(iter(c_arr)).material_index != r_mat
                                    and (bb[0] - pad <= pt[0] <= bb[1] + pad)
                                    and (bb[2] - pad <= pt[1] <= bb[3] + pad)
                                    and (bb[4] - pad <= pt[2] <= bb[5] + pad)
                                ]
                                if matched_arrows:
                                    valid_rings.append(c_ring)
                                    valid_arrows.extend(matched_arrows)

                    valid_ring_faces = {f for c in valid_rings for f in c}
                    valid_arrow_faces = [f for c in valid_arrows for f in c]
                    # Loại trùng lặp mặt mũi tên nếu có
                    valid_arrow_faces = list({f: None for f in valid_arrow_faces}.keys())

                    if valid_ring_faces and valid_arrow_faces:
                        mat_ring = bpy.data.materials.get("WT3D_Pipe_Arrow_Ring")
                        if not mat_ring:
                            mat_ring = bpy.data.materials.new("WT3D_Pipe_Arrow_Ring")
                            mat_ring.use_nodes = True
                        mat_arrow = bpy.data.materials.get("WT3D_Pipe_Arrow_Mark")
                        if not mat_arrow:
                            mat_arrow = bpy.data.materials.new("WT3D_Pipe_Arrow_Mark")
                            mat_arrow.use_nodes = True

                        if "WT3D_Pipe_Arrow_Ring" not in [m_slot.name for m_slot in m.materials if m_slot]:
                            m.materials.append(mat_ring)
                        if "WT3D_Pipe_Arrow_Mark" not in [m_slot.name for m_slot in m.materials if m_slot]:
                            m.materials.append(mat_arrow)

                        ring_mat_idx = [i for i, ms in enumerate(m.materials) if ms and ms.name == "WT3D_Pipe_Arrow_Ring"][0]
                        arrow_mat_idx = [i for i, ms in enumerate(m.materials) if ms and ms.name == "WT3D_Pipe_Arrow_Mark"][0]

                        for c_ring in valid_rings:
                            for f in c_ring:
                                if f.is_valid:
                                    f.material_index = ring_mat_idx
                                    f.smooth = True

                        for f in valid_arrow_faces:
                            if f.is_valid:
                                f.material_index = arrow_mat_idx
                                f.smooth = True

                    # Tách riêng `van 10` (`van 10.ipt` / `van 10 - 01.ipt`) giữ đúng màu gốc:
                    # Thân van Smooth-White (#BFBFBF) + Tay vặn Xanh Gốc (#005AE6)
                    van10_handle_islands = []
                    for c_h in isl_ring_cand:
                        c_h_valid = [f for f in c_h if f.is_valid]
                        if 240 <= len(c_h_valid) <= 275:
                            bb_h = _island_bbox(c_h_valid)
                            if max(bb_h[1] - bb_h[0], bb_h[3] - bb_h[2], bb_h[5] - bb_h[4]) < 0.040:
                                van10_handle_islands.append((c_h_valid, _island_center(c_h_valid)))
                    if van10_handle_islands:
                        van10_blue_faces = {f for (c_h, _) in van10_handle_islands for f in c_h}
                        van10_white_faces = set()
                        for c_r in isl_ring_cand:
                            c_r_valid = [f for f in c_r if f.is_valid]
                            if 45 <= len(c_r_valid) <= 65:
                                pt_r = _island_center(c_r_valid)
                                if any(math.hypot(pt_r[0] - hc[0], math.hypot(pt_r[1] - hc[1], pt_r[2] - hc[2])) < 0.038 for (_, hc) in van10_handle_islands):
                                    van10_blue_faces.update(c_r_valid)
                        for c_w in isl_arrow_cand:
                            c_w_valid = [f for f in c_w if f.is_valid]
                            if not c_w_valid:
                                continue
                            bb_w = _island_bbox(c_w_valid)
                            if max(bb_w[1] - bb_w[0], bb_w[3] - bb_w[2], bb_w[5] - bb_w[4]) <= 0.056:
                                pt_w = _island_center(c_w_valid)
                                if any(math.hypot(pt_w[0] - hc[0], math.hypot(pt_w[1] - hc[1], pt_w[2] - hc[2])) < 0.038 for (_, hc) in van10_handle_islands):
                                    van10_white_faces.update(c_w_valid)
                        if van10_white_faces or van10_blue_faces:
                            mat_v10_w = bpy.data.materials.get("WT3D_Van10_Orig_White_Mat") or bpy.data.materials.new("WT3D_Van10_Orig_White_Mat")
                            mat_v10_w.use_nodes = True
                            mat_v10_b = bpy.data.materials.get("WT3D_Van10_Orig_Blue_Mat") or bpy.data.materials.new("WT3D_Van10_Orig_Blue_Mat")
                            mat_v10_b.use_nodes = True
                            if "WT3D_Van10_Orig_White_Mat" not in [ms.name for ms in m.materials if ms]:
                                m.materials.append(mat_v10_w)
                            if "WT3D_Van10_Orig_Blue_Mat" not in [ms.name for ms in m.materials if ms]:
                                m.materials.append(mat_v10_b)
                            v10_w_idx = [i for i, ms in enumerate(m.materials) if ms and ms.name == "WT3D_Van10_Orig_White_Mat"][0]
                            v10_b_idx = [i for i, ms in enumerate(m.materials) if ms and ms.name == "WT3D_Van10_Orig_Blue_Mat"][0]
                            for f in van10_white_faces:
                                if f.is_valid:
                                    f.material_index = v10_w_idx
                            for f in van10_blue_faces:
                                if f.is_valid:
                                    f.material_index = v10_b_idx

            bm.to_mesh(m)
            bm.free()
            m.update()

            # Apply crisp 28-deg Auto-Smooth and isolate cylinder step-rings
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle_deg), keep_sharp_edges=False)
            obj.select_set(False)

            slot_names_smooth = [ms.name if ms else "" for ms in m.materials]
            arrow_smooth_indices = {
                i for i, sn in enumerate(slot_names_smooth)
                if sn in ("24,37,248", "34,46,248", "WT3D_Pipe_Arrow_Ring", "WT3D_Pipe_Arrow_Mark", "WT3D_Flow_Arrow_White_Mat")
            }
            bm = bmesh.new()
            bm.from_mesh(m)
            for f in bm.faces:
                if f.material_index in arrow_smooth_indices:
                    f.smooth = True
                    for e in f.edges:
                        e.smooth = True
                    continue
                if abs(f.normal.y) < 0.005 and math.hypot(f.normal.x, f.normal.z) > 0.98:
                    for e in f.edges:
                        if any(abs(nf.normal.y) > 0.012 for nf in e.link_faces):
                            e.smooth = False
                if abs(f.normal.z) < 0.005 and math.hypot(f.normal.x, f.normal.y) > 0.98:
                    for e in f.edges:
                        if any(abs(nf.normal.z) > 0.012 for nf in e.link_faces):
                            e.smooth = False
            bm.to_mesh(m)
            bm.free()
            m.update()

            if hasattr(obj, "cycles"):
                obj.cycles.shadow_terminator_offset = 0.0
                obj.cycles.shadow_terminator_geometry_offset = 0.0
        except Exception as e:
            print(f"[WT3D V3.0] Warning in restore_crisp_cad_sharp_edges ({obj.name}): {e}")


def inject_keyshot_material_graph(mat, profile=None):
    """
    KeyShot 11 Pro Multi-Layer Material Graph Engine for Blender Cycles/EEVEE:
    Phối trộn đa tầng bất hoàn hảo bề mặt (Surface Imperfections & Dual-Layer Bump Add):
    1. Rounded Edges (`ShaderNodeBevel`, r = 0.45mm): Bo mép ảo bắt sáng viền cạnh cơ khí CAD.
    2. Kênh Độ Nhám (`Roughness` Imperfection Mixer):
       - `TexCoord (Object)` -> `Noise Grunge/Smudge` -> `Map Range (Color To Number)` -> `Principled BSDF.Roughness`.
       - Ép dải hẹp quanh `base_roughness` (±0.045) tạo độ sâu phản chiếu tự nhiên khi đèn Studio quét qua.
    3. Kênh Độ Nổi 2 Tầng (`Bump Add`: Vi mô Micro + Vĩ mô Macro Waviness):
       - `Bump Macro`: Noise tần số thấp (`Scale = 4.5` ~ 220mm, `Strength = 0.022`) tạo độ lượn sóng nhẹ của kim loại chấn hàn / nhựa đùn.
       - `Bump Micro` (theo `profile`):
         + `"SUS304_BRUSHED"`: Vân xước phay kim loại kéo giãn 42x (`Scale Z = 42`, `Noise Scale = 75`, `Strength = 0.055`).
         + `"FRP_GELCOAT_WEAVE"`: Lớp nền sợi thủy tinh đan chéo (`Wave Bands Scale = 38`, `Strength = 0.032` vào `Normal`) + Lớp phủ bóng Gelcoat sần vỏ cam (`Orange Peel Noise Scale = 135`, `Strength = 0.018` vào `Coat Normal`).
         + `"UPVC_EXTRUDED"`: Vân kéo đùn khuôn ống nhựa (`Mapping Scale = (10,10,1.5)`, `Noise Scale = 35`, `Strength = 0.028`).
         + `"POWDER_COAT_RAL"`: Hạt sần vỏ cam sơn tĩnh điện (`Voronoi Scale = 380` ~ 1.5mm, `Strength = 0.085`).
         + `"CLEAR_ACRYLIC_PMMA"`: Kính Acrylic/PC trong suốt siêu láng kèm vi biến thiên phản xạ (`0.015 -> 0.045`).
    """
    if not mat or not mat.use_nodes or not mat.node_tree:
        return False
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bsdf:
        return False

    # Remove previous KeyShot procedural nodes to keep node tree clean and idempotent
    for n in list(nodes):
        if n.name.startswith("_KS_"):
            nodes.remove(n)

    rgb = _parse_rgb_from_mat_name(mat.name)
    base_rough = float(bsdf.inputs['Roughness'].default_value) if 'Roughness' in bsdf.inputs else 0.20
    metal_val = float(bsdf.inputs['Metallic'].default_value) if 'Metallic' in bsdf.inputs else 0.0
    cur_alpha = float(bsdf.inputs['Alpha'].default_value) if 'Alpha' in bsdf.inputs else 1.0

    if profile is None:
        if cur_alpha < 0.98 or mat.blend_method == 'BLEND':
            profile = "CLEAR_ACRYLIC_PMMA"
        elif metal_val >= 0.55 or rgb in METALLIC_STAINLESS_RGB or rgb in METALLIC_BRASS_RGB:
            profile = "SUS304_BRUSHED"
        elif rgb in ((155, 173, 136), (16, 171, 74), (77, 77, 250), (102, 255, 128), (230, 233, 236)) or "frp" in mat.name.lower() or "ro_housing" in mat.name.lower():
            profile = "FRP_GELCOAT_WEAVE"
        elif rgb in ((242, 242, 255), (5, 5, 5), (28, 30, 33), (64, 64, 64), (0, 0, 0), (32, 35, 38)):
            profile = "POWDER_COAT_RAL"
        else:
            profile = "UPVC_EXTRUDED"

    # 1. Object Coordinates (UV-Free 3D Solid Mapping)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.name = "_KS_TexCoord"
    tex_coord.location = (-1100, -100)

    # 2. KeyShot Rounded Edges (Virtual CAD Edge Bevel Shader)
    bevel_node = nodes.new('ShaderNodeBevel')
    bevel_node.name = "_KS_Bevel"
    bevel_node.samples = 4
    bevel_node.inputs['Radius'].default_value = 0.0005  # 0.5mm edge highlight
    bevel_node.location = (-880, -420)

    # 3. Macro Waviness Layer (Bump Layer 2 - Low Frequency Manufacturing Waviness)
    noise_macro = nodes.new('ShaderNodeTexNoise')
    noise_macro.name = "_KS_Noise_Macro"
    noise_macro.location = (-880, -180)
    noise_macro.inputs['Scale'].default_value = 4.5
    noise_macro.inputs['Detail'].default_value = 2.0
    if 'Roughness' in noise_macro.inputs:
        noise_macro.inputs['Roughness'].default_value = 0.50
    links.new(tex_coord.outputs['Object'], noise_macro.inputs['Vector'])

    bump_macro = nodes.new('ShaderNodeBump')
    bump_macro.name = "_KS_Bump_Macro"
    bump_macro.location = (-640, -320)
    bump_macro.inputs['Strength'].default_value = 0.018 if profile != "CLEAR_ACRYLIC_PMMA" else 0.005
    bump_macro.inputs['Distance'].default_value = 0.0008
    links.new(noise_macro.outputs['Fac'], bump_macro.inputs['Height'])
    links.new(bevel_node.outputs['Normal'], bump_macro.inputs['Normal'])

    # 4. Micro Texture + Roughness Color-To-Number Layer (Bump Layer 1 + Roughness Map Range)
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.name = "_KS_ColorToNumber"
    map_range.location = (-360, 80)
    map_range.inputs['From Min'].default_value = 0.25
    map_range.inputs['From Max'].default_value = 0.75

    bump_micro = nodes.new('ShaderNodeBump')
    bump_micro.name = "_KS_Bump_Micro"
    bump_micro.location = (-360, -260)
    links.new(bump_macro.outputs['Normal'], bump_micro.inputs['Normal'])

    if profile == "SUS304_BRUSHED":
        mapping = nodes.new('ShaderNodeMapping')
        mapping.name = "_KS_Mapping_Brushed"
        mapping.location = (-880, 120)
        mapping.inputs['Scale'].default_value = (1.0, 1.0, 42.0)
        links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

        noise_micro = nodes.new('ShaderNodeTexNoise')
        noise_micro.name = "_KS_Noise_Brushed"
        noise_micro.location = (-640, 120)
        noise_micro.inputs['Scale'].default_value = 78.0
        noise_micro.inputs['Detail'].default_value = 12.0
        if 'Roughness' in noise_micro.inputs:
            noise_micro.inputs['Roughness'].default_value = 0.72
        links.new(mapping.outputs['Vector'], noise_micro.inputs['Vector'])

        map_range.inputs['To Min'].default_value = max(0.06, base_rough - 0.045)
        map_range.inputs['To Max'].default_value = min(0.36, base_rough + 0.055)
        links.new(noise_micro.outputs['Fac'], map_range.inputs['Value'])

        bump_micro.inputs['Strength'].default_value = 0.052
        bump_micro.inputs['Distance'].default_value = 0.0003
        links.new(noise_micro.outputs['Fac'], bump_micro.inputs['Height'])

    elif profile == "FRP_GELCOAT_WEAVE":
        wave_weave = nodes.new('ShaderNodeTexWave')
        wave_weave.name = "_KS_Wave_Weave"
        wave_weave.location = (-640, 120)
        wave_weave.wave_type = 'BANDS'
        wave_weave.inputs['Scale'].default_value = 38.0
        wave_weave.inputs['Distortion'].default_value = 1.6
        wave_weave.inputs['Detail'].default_value = 4.0
        links.new(tex_coord.outputs['Object'], wave_weave.inputs['Vector'])

        map_range.inputs['To Min'].default_value = max(0.05, base_rough - 0.035)
        map_range.inputs['To Max'].default_value = min(0.28, base_rough + 0.040)
        links.new(wave_weave.outputs['Fac'], map_range.inputs['Value'])

        bump_micro.inputs['Strength'].default_value = 0.030
        bump_micro.inputs['Distance'].default_value = 0.0004
        links.new(wave_weave.outputs['Fac'], bump_micro.inputs['Height'])

        # Separate Clearcoat Orange Peel Bump on Coat Normal!
        if 'Coat Normal' in bsdf.inputs:
            noise_coat = nodes.new('ShaderNodeTexNoise')
            noise_coat.name = "_KS_Noise_OrangePeel"
            noise_coat.location = (-640, -520)
            noise_coat.inputs['Scale'].default_value = 135.0
            noise_coat.inputs['Detail'].default_value = 3.0
            links.new(tex_coord.outputs['Object'], noise_coat.inputs['Vector'])

            bump_coat = nodes.new('ShaderNodeBump')
            bump_coat.name = "_KS_Bump_Coat"
            bump_coat.location = (-360, -520)
            bump_coat.inputs['Strength'].default_value = 0.016
            bump_coat.inputs['Distance'].default_value = 0.0002
            links.new(noise_coat.outputs['Fac'], bump_coat.inputs['Height'])
            links.new(bevel_node.outputs['Normal'], bump_coat.inputs['Normal'])
            links.new(bump_coat.outputs['Normal'], bsdf.inputs['Coat Normal'])

    elif profile == "POWDER_COAT_RAL":
        voronoi = nodes.new('ShaderNodeTexVoronoi')
        voronoi.name = "_KS_Voronoi_Powder"
        voronoi.location = (-640, 120)
        voronoi.inputs['Scale'].default_value = 380.0
        if 'Randomness' in voronoi.inputs:
            voronoi.inputs['Randomness'].default_value = 0.85
        links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])

        map_range.inputs['To Min'].default_value = max(0.12, base_rough - 0.045)
        map_range.inputs['To Max'].default_value = min(0.52, base_rough + 0.065)
        links.new(voronoi.outputs['Distance'], map_range.inputs['Value'])

        bump_micro.inputs['Strength'].default_value = 0.075
        bump_micro.inputs['Distance'].default_value = 0.0005
        links.new(voronoi.outputs['Distance'], bump_micro.inputs['Height'])

    elif profile == "CLEAR_ACRYLIC_PMMA":
        noise_clear = nodes.new('ShaderNodeTexNoise')
        noise_clear.name = "_KS_Noise_Clear"
        noise_clear.location = (-640, 120)
        noise_clear.inputs['Scale'].default_value = 22.0
        noise_clear.inputs['Detail'].default_value = 4.0
        links.new(tex_coord.outputs['Object'], noise_clear.inputs['Vector'])

        map_range.inputs['To Min'].default_value = 0.015
        map_range.inputs['To Max'].default_value = 0.045
        links.new(noise_clear.outputs['Fac'], map_range.inputs['Value'])

        bump_micro.inputs['Strength'].default_value = 0.006
        bump_micro.inputs['Distance'].default_value = 0.0001
        links.new(noise_clear.outputs['Fac'], bump_micro.inputs['Height'])

    else:  # UPVC_EXTRUDED
        mapping = nodes.new('ShaderNodeMapping')
        mapping.name = "_KS_Mapping_uPVC"
        mapping.location = (-880, 120)
        mapping.inputs['Scale'].default_value = (10.0, 10.0, 1.8)
        links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

        noise_upvc = nodes.new('ShaderNodeTexNoise')
        noise_upvc.name = "_KS_Noise_uPVC"
        noise_upvc.location = (-640, 120)
        noise_upvc.inputs['Scale'].default_value = 34.0
        noise_upvc.inputs['Detail'].default_value = 6.0
        if 'Roughness' in noise_upvc.inputs:
            noise_upvc.inputs['Roughness'].default_value = 0.62
        links.new(mapping.outputs['Vector'], noise_upvc.inputs['Vector'])

        map_range.inputs['To Min'].default_value = max(0.08, base_rough - 0.040)
        map_range.inputs['To Max'].default_value = min(0.36, base_rough + 0.045)
        links.new(noise_upvc.outputs['Fac'], map_range.inputs['Value'])

        bump_micro.inputs['Strength'].default_value = 0.026
        bump_micro.inputs['Distance'].default_value = 0.0003
        links.new(noise_upvc.outputs['Fac'], bump_micro.inputs['Height'])

    if 'Roughness' in bsdf.inputs:
        links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])
    if 'Normal' in bsdf.inputs:
        links.new(bump_micro.outputs['Normal'], bsdf.inputs['Normal'])
    return True


def apply_inventor_pbr_materials():
    """
    V3.0 Ultra-Photoreal PBR Material Calibration Engine (Zero-Decal, Fab/GLB/FBX Ready):
    - Chuyển đổi chính xác không gian màu `sRGB -> Scene Linear` (`_srgb_to_linear`) giúp màu sắc đậm, sâu, không bị bạc phấn.
    - Đặt `Emission Color = (0,0,0,1)` và `Emission Strength = 0.0` cho mọi vật liệu không phát sáng để FBX không bị lỗi `EmissiveColor = (1,1,1)` trên Fab.
    - Hiệu chuẩn vật lý chuẩn công nghiệp cho Inox SUS304 Satin, Đồng thau, Vỏ màng RO Gelcoat,
      Nhựa uPVC Sch80 Xám Xanh Đá (tách khỏi cao su đen), Gang Motor Bơm `#24303C`, Tay van đỏ `#EB2026`,
      Chữ nổi 3D Sapphire `#007CFF`, Đèn tháp 3 tầng LED, và Vật liệu Clear PMMA / Bầu lọc trong suốt.
    """
    restore_crisp_cad_sharp_edges(28.0)

    updated_count = 0
    for mat in bpy.data.materials:
        if not mat:
            continue
        if mat.name.startswith("WT3D_Decal_"):
            mat.blend_method = 'OPAQUE'
            if hasattr(mat, "surface_render_method"):
                try:
                    mat.surface_render_method = 'DITHERED'
                except Exception:
                    pass
            continue

        if not mat.use_nodes or not mat.node_tree:
            continue

        bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf:
            continue

        rgb = _parse_rgb_from_mat_name(mat.name)
        # Check if 255,255,255 was originally an Inventor metal-textured material (Steelplt.png / Stainless.Bright.jpg -> Kd 0.784 0.804 0.816 in MTL)
        if rgb == (255, 255, 255):
            imp_bc = list(bsdf.inputs['Base Color'].default_value)
            has_metal_tex = any(
                n.type == 'TEX_IMAGE' and getattr(n, 'image', None) and any(k in n.image.name.lower() for k in ('steelplt', 'stainless', 'metal', 'ornamental'))
                for n in mat.node_tree.nodes
            )
            if has_metal_tex or (0.45 < imp_bc[0] < 0.86 and 0.45 < imp_bc[1] < 0.88):
                rgb = (190, 188, 186)
        # Disconnect any missing/temporary TEX_IMAGE nodes from Base Color so procedural PBR color is pure
        for n in list(mat.node_tree.nodes):
            if n.type == 'TEX_IMAGE':
                mat.node_tree.nodes.remove(n)
        if rgb is not None:
            bsdf.inputs['Base Color'].default_value = _rgb_tuple_to_linear(rgb, 1.0)

        # Reset Emission to pure black (0,0,0) by default so FBX never exports white EmissiveColor!
        if 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = (0.0, 0.0, 0.0, 1.0)
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = 0.0
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = 0.58
        if 'Coat Weight' in bsdf.inputs:
            bsdf.inputs['Coat Weight'].default_value = 0.0
        if 'Coat Roughness' in bsdf.inputs:
            bsdf.inputs['Coat Roughness'].default_value = 0.08
        if 'Anisotropic' in bsdf.inputs:
            bsdf.inputs['Anisotropic'].default_value = 0.0
        if 'Transmission Weight' in bsdf.inputs:
            bsdf.inputs['Transmission Weight'].default_value = 0.0

        cur_alpha = float(bsdf.inputs['Alpha'].default_value) if 'Alpha' in bsdf.inputs else 1.0
        name_lower = mat.name.lower()
        is_clear_keyword = any(
            k in name_lower
            for k in ("clear", "glass", "transpar", "acrylic", "polycarbonate", "rotameter", "sight")
        )
        is_trans_suffix = name_lower.endswith("_trans")

        # 1. Vật liệu trong suốt (Clear Glass / Acrylic PMMA / Clear Filter Housing / Translucent Composite)
        is_translucent = (cur_alpha < 0.98) or (rgb in TRANSLUCENT_FORCE_RGB) or is_clear_keyword or is_trans_suffix

        if is_translucent:
            is_clear_glass = is_clear_keyword or (rgb in CLEAR_TRANSMISSION_RGB)
            if is_clear_glass and not is_trans_suffix:
                # Kính kỹ thuật Acrylic (#E8F4FA, IOR = 1.49, Transmission = 0.95, Roughness = 0.03)
                target_alpha = min(cur_alpha, 0.24) if cur_alpha < 0.98 else 0.24
                if mat.name == "WT3D_Clear_Housing" or rgb in ((229, 229, 229), (250, 250, 250), (236, 241, 239), (232, 244, 250)):
                    base_lin = _hex_to_rgba("#E8F4FA", target_alpha)
                else:
                    bc0 = list(bsdf.inputs['Base Color'].default_value)
                    base_lin = (bc0[0], bc0[1], bc0[2], target_alpha)
            else:
                # Bầu lọc xanh trong suốt (1,62,241), Bồn Composite bán trong suốt (16,171,74 / 102,255,128 / *_trans)
                target_alpha = (
                    cur_alpha
                    if cur_alpha < 0.98
                    else TRANSLUCENT_FORCE_RGB.get(rgb, 0.42)
                )
                if rgb == (1, 62, 241):
                    # Bầu lọc xanh dương trong suốt: dùng xanh Sapphire trong trẻo thay vì xanh tối sẫm để FBX nhìn xuyên lõi lọc!
                    target_alpha = min(target_alpha, 0.36)
                    base_lin = _hex_to_rgba("#1E78FF", target_alpha)
                else:
                    bc0 = list(bsdf.inputs['Base Color'].default_value)
                    base_lin = (bc0[0], bc0[1], bc0[2], target_alpha)

            bsdf.inputs['Base Color'].default_value = base_lin
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.03 if is_clear_glass else 0.07
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.49
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.85 if is_clear_glass else 0.75
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.85 if is_clear_glass else 0.40
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.02
            if 'Alpha' in bsdf.inputs:
                bsdf.inputs['Alpha'].default_value = target_alpha
            if 'Transmission Weight' in bsdf.inputs:
                bsdf.inputs['Transmission Weight'].default_value = 0.0

            try:
                mat.diffuse_color = base_lin
                mat.metallic = 0.0
                mat.roughness = float(bsdf.inputs['Roughness'].default_value)
            except Exception:
                pass

            mat.blend_method = 'BLEND'
            if hasattr(mat, "surface_render_method"):
                try:
                    mat.surface_render_method = 'BLENDED'
                except Exception:
                    pass
            mat.use_backface_culling = False
            inject_keyshot_material_graph(mat, profile="CLEAR_ACRYLIC_PMMA")
            updated_count += 1
            continue

        # 2. Vật liệu đặc (Opaque): khóa chặt OPAQUE để không bị lỗi Z-sorting
        mat.blend_method = 'OPAQUE'
        if hasattr(mat, "surface_render_method"):
            try:
                mat.surface_render_method = 'DITHERED'
            except Exception:
                pass
        if 'Alpha' in bsdf.inputs:
            bsdf.inputs['Alpha'].default_value = 1.0

        # 2A. Chữ nổi 3D "WaterTreatment3D" trên cánh tủ điện (`31,31,180_1` -> Xanh Bóng Sapphire!)
        if mat.name == "31,31,180_1":
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#007CFF", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.35
            bsdf.inputs['Roughness'].default_value = 0.06
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.54
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 1.0
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.015
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#0066E8", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.45

        # 2A-2. Vòng tròn chứa mũi tên trên ống (WT3D_Pipe_Arrow_Ring) & Mũi tên 3D nổi trên vòng tròn (WT3D_Pipe_Arrow_Mark)
        elif mat.name == "WT3D_Pipe_Arrow_Ring":
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#1268F0", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.05
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.54
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.85
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.04
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#1268F0", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.08
        elif mat.name == "WT3D_Pipe_Arrow_Mark":
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#FFFFFF", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.08
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.54
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 1.0
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.02
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#FFFFFF", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.28
        elif mat.name == "WT3D_Van10_Orig_White_Mat":
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#D8DDE2", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.20
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.49
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.35
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
        elif mat.name == "WT3D_Van10_Orig_Blue_Mat":
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#0A66E6", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.20
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.49
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.35
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
        elif mat.name == "WT3D_UV_Purple_LED" or rgb == (170, 45, 255):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#AA2DFF", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.06
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.46
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.90
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.02
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#C85FFF", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 3.5

        # 2A-3. Studio V2.8: Inox 304 Bóng Sáng Chuẩn Inventor (`215,220,225` -> #E4E9EE, Metallic=0.65, Roughness=0.16)
        elif rgb == (215, 220, 225):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#E4E9EE", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.65
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.25
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.05
            if 'Anisotropic' in bsdf.inputs:
                bsdf.inputs['Anisotropic'].default_value = 0.15
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.85

        # 2A-4. Studio V2.8: Đường Ống & Phụ Kiện Nhựa uPVC Sch80 Xám Đá Sáng Chuẩn Inventor (`78,86,94` -> #788694; giữ nguyên màu xanh `48,135,227` nếu View Inventor đang để ống xanh!)
        elif rgb == (78, 86, 94):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#788694", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.22
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.52
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.35
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.58

        # 2A-5. Studio V2.8: Thân Van Bi uPVC Xám Đậm Chuẩn Inventor (`42,48,54` -> #48525C)
        elif rgb in ((42, 48, 54), (66, 74, 82)):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#667482", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.20
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.52
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.30
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.55

        # 2A-6. Studio V3.0: Tay Gạt Van Cam (`244,119,33` -> #F47721), Đỏ (`214,40,40` -> #E02424) & Xanh Dương (`29,91,158` / `0,125,168` -> #1A66CC)
        elif rgb == (244, 119, 33):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#F47721", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.50
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.50
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.06
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.68
        elif rgb == (214, 40, 40):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#E02424", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.50
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.50
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.06
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.68
        elif rgb in ((29, 91, 158), (0, 125, 168)):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#1A66CC", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.50
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.50
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.06
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.68

        # 2A-7. Studio V2.8: Cao Su Đệm EPDM & Bánh Xe PU Đen (`32,35,38` -> #2B3036)
        elif rgb == (32, 35, 38):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#2B3036", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.05
            bsdf.inputs['Roughness'].default_value = 0.28
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.52
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.20
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.10

        # 2B. Đèn tháp báo hiệu 3 tầng & Đèn báo tủ điện (`255,0,0` Đỏ, `255,140,0` Vàng Cam, `0,255,0` Xanh Lá Sáng, `34,197,94` Xanh Lá Chờ)
        elif rgb == (255, 0, 0):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#E62222", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.12
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.85
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#D61C1C", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.25
        elif rgb == (255, 140, 0):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#F8A800", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.12
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.85
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#E89800", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.25
        elif rgb == (0, 255, 0):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#00FF44", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.08
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.95
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#00FF38", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 1.8
        elif rgb == (34, 197, 94):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#28B858", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.70

        # 2C-0. Van 10 & Nhựa Trắng Mịn Smooth-White (191,191,191) -> Trắng Sáng Chuẩn Inventor Default View
        elif rgb == (191, 191, 191):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#D8DDE2", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.18
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.45
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.60

        # 2C. Inox SUS304/316 Sáng Bóng Chuẩn Inventor (#E2E7EC, Metallic = 0.65, Roughness = 0.16)
        elif rgb in METALLIC_STAINLESS_RGB or rgb in ((128, 0, 128), (255, 251, 240)):
            if rgb == (128, 0, 128):
                # Máng cáp lưới (`mang luoi 133x50`): Inox SUS304 sáng (#E2E7EC)
                bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#E2E7EC", 1.0)
                bsdf.inputs['Metallic'].default_value = 0.65
                bsdf.inputs['Roughness'].default_value = 0.16
            elif rgb == (129, 130, 133):
                bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#D6DEE6", 1.0)
                bsdf.inputs['Metallic'].default_value = 0.62
                bsdf.inputs['Roughness'].default_value = 0.18
            else:
                bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#E2E7EC", 1.0)
                bsdf.inputs['Metallic'].default_value = 0.65
                bsdf.inputs['Roughness'].default_value = 0.16
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.25
            if 'Anisotropic' in bsdf.inputs:
                bsdf.inputs['Anisotropic'].default_value = 0.15
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.85

        # 2D. Đồng thau / Van điện từ Brass (`203,154,59`, `191,153,15`, `255,227,181`)
        elif rgb in METALLIC_BRASS_RGB or rgb == (255, 227, 181):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#D6A844", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.78
            bsdf.inputs['Roughness'].default_value = 0.20
            if 'Anisotropic' in bsdf.inputs:
                bsdf.inputs['Anisotropic'].default_value = 0.20

        # 2E-1. Mũi tên chỉ hướng dòng chảy & Nhãn trắng tinh khiết (`235,235,235`, `WT3D_Pipe_Arrow_Mark`)
        elif mat.name in ("WT3D_Pipe_Arrow_Mark", "WT3D_Flow_Arrow_White_Mat") or "arrow_mark" in mat.name.lower():
            bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.10
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.50
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.35

        # 2E-2. Lõi lọc bông nén 7 lõi PP (`WT3D_7Core_PP_DirtTrap_Mat`): Trắng tinh khiết tự phát sáng nhẹ để nhìn xuyên qua bầu lọc trong suốt
        elif mat.name == "WT3D_7Core_PP_DirtTrap_Mat" or "dirttrap" in mat.name.lower():
            bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.25
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.40

        # 2E-3. Vỏ màng RO 8040, Nắp bồn màng RO & Tủ điện điều khiển trắng bóng (`244,246,248`, `242,242,255`, `255,255,255`, `28,30,33` nắp đầu màng)
        elif rgb in ((244, 246, 248), (242, 242, 255), (255, 255, 255), (240, 240, 238)) or any(k in mat.name.lower() for k in ("244,246,248", "242,242,255", "ro_housing")):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#F2F5F8", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.14
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.65
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.04
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.60

                # 2E-0. Cong tac ap Danfoss KP35 dial scale plate (White Gloss with crisp scale)
        elif mat.name == "WT3D_Danfoss_KP35_Scale_Mat" or ("kp35" in mat.name.lower() and rgb == (64, 64, 64)) or "cong_tac_ap_scale" in mat.name.lower():
            bsdf.inputs['Base Color'].default_value = (0.96, 0.96, 0.96, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.15
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.60
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.40
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.20

                # 2E-FRP. Cột lọc composite FRP Gelcoat bóng cao cấp (155,173,136 / FRP-VN)
        elif rgb == (155, 173, 136) or "frp" in mat.name.lower() or mat.name.startswith("155,173,136"):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#5B7B54", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.10
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.85
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.03
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.65
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.0

                # 2E-HDPE. Nhựa HDPE trắng mờ công nghiệp (235,235,235 - Thùng muối, Nắp van - ZERO EMISSION)
        elif rgb == (235, 235, 235) or mat.name.startswith("235,235,235"):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#EDF1F4", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.24
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.25
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.0

        # 2E & 2F. Toàn bộ Phụ kiện ống uPVC Sch80 (Tê, Co 90°, Rắc co đôi, Nối ren, Thân van, Cổ nối lưu lượng kế)
        # Chuẩn thực tế uPVC công nghiệp: Xám Đá uPVC Sch80 Sáng Chuẩn Inventor (#788694, Roughness = 0.22, Clearcoat = 0.35)
        elif rgb in (
            (47, 47, 47),
            (80, 80, 80),
            (89, 96, 114),
            (97, 103, 121),
            (110, 125, 161),
            (123, 124, 127),
            (148, 166, 184),
            (78, 86, 94),
        ) or mat.name in ("78,86,94"):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#788694", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.22
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.54
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.35
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.58

        # 2F-Color. Đường ống / Phụ kiện uPVC có màu riêng trên View Inventor (`48,135,227` Xanh dương, `33,138,33` / `46,138,87` Xanh lá, `43,54,119` / `45,54,107` Xanh đậm):
        # Giữ nguyên 100% màu RGB đang hiển thị trên Inventor, chỉ áp độ bóng nhựa uPVC (Roughness=0.22, Coat=0.35)
        elif rgb in (
            (48, 135, 227),
            (43, 54, 119),
            (45, 54, 107),
            (46, 138, 87),
            (33, 138, 33),
        ):
            bsdf.inputs['Base Color'].default_value = _rgb_tuple_to_linear(rgb, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.22
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.54
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.35
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.58

        # 2G. Thân Motor Bơm Gang Sơn Tĩnh Điện (`5,5,5` -> #2A2F35) & Đế Cao Su EPDM (`0,0,0` -> #262B30)
        elif rgb in ((5, 5, 5), (28, 30, 33), (64, 64, 64)):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#2A2F35", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.18
            bsdf.inputs['Roughness'].default_value = 0.28
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.25
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.65
        elif rgb == (0, 0, 0):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#262B30", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.05
            bsdf.inputs['Roughness'].default_value = 0.32

        # 2H. Tay van bi đỏ tín hiệu (`204,0,0`, `178,0,0`, `182,18,12`, `220,38,38`, `229,31,31`)
        elif rgb in ((204, 0, 0), (178, 0, 0), (182, 18, 12), (220, 38, 38), (229, 31, 31)):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#EB2026", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.20
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.50
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.45
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.06
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.68

        # 2I. Vỏ màng RO 8040 Trắng Sứ Gelcoat (#F8FAFC - RAL 9003 Signal White, Metallic = 0.0, Roughness = 0.12, Clearcoat = 1.0)
        elif rgb in ((230, 233, 236), (244, 246, 248), (255, 255, 255), (240, 240, 238), (244, 244, 244), (245, 245, 245), (245, 246, 246)):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#F8FAFC", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.12
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.52
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 1.0
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.04
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.72
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = _hex_to_rgba("#FFFFFF", 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.04

        # 2J. Vỏ Tủ Điện / Tấm Panel gắn thiết bị đo (`242,242,255` -> #EEF2F6 Trắng Sáng Chuẩn Inventor!)
        elif rgb == (242, 242, 255):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#EEF2F6", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.02
            bsdf.inputs['Roughness'].default_value = 0.24
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.50
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.25

        # 2K. Bồn FRP Gelcoat & Khung Sơn Epoxy (`155,173,136`, `31,31,180`, v.v.)
        elif rgb in GLOSS_FRP_AND_CABINET_RGB:
            bsdf.inputs['Metallic'].default_value = 0.05 if rgb == (31, 31, 180) else 0.0
            bsdf.inputs['Roughness'].default_value = 0.22
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.52
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.45
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.65

        # 2L. Đường ống phân tuyến màu kỹ thuật CAD (giữ nguyên màu ống phân tuyến, bề mặt nhựa/sơn kỹ thuật Roughness = 0.24)
        else:
            bsdf.inputs['Metallic'].default_value = 0.02
            bsdf.inputs['Roughness'].default_value = 0.24
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.52
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.35
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.65

        bc_final = list(bsdf.inputs['Base Color'].default_value)
        try:
            mat.diffuse_color = (bc_final[0], bc_final[1], bc_final[2], 1.0)
            mat.metallic = float(bsdf.inputs['Metallic'].default_value)
            mat.roughness = float(bsdf.inputs['Roughness'].default_value)
        except Exception:
            pass

        inject_keyshot_material_graph(mat)
        updated_count += 1

    # Xóa các image mồ côi khỏi bpy.data.images để FBX/GLB không báo lỗi thiếu file
    for img in list(bpy.data.images):
        if img.users == 0:
            bpy.data.images.remove(img)

    return updated_count


def apply_european_cleanroom_pbr_materials():
    """
    Phiên bản Thực Tế Phong Cách Châu Âu (European High-Tech Industrial Cleanroom 60-30-10 Realism):
    - 60% Khối Nền Sáng:
      + Khung Skid chịu lực (`31,31,180`) + Thân Bơm/Vỏ lọc Inox -> Bạc Inox SUS304/316 xước mờ `#C8CDD0` (`Metallic = 0.90, Roughness = 0.28, Anisotropic = 0.50`).
      + Vỏ màng RO FRP (`230,233,236`) -> Trắng Sứ `#F4F6F8` (*RAL 9003 Signal White*, `Roughness = 0.12, Coat Weight = 1.0`).
      + Tủ điện / Panel (`242,242,255`) -> Xám sáng mờ `#D0D4D7` (*RAL 7035 Light Grey*, `Roughness = 0.55`).
      + Cột lọc Composite / Bồn FRP áp lực (`155,173,136`, `16,171,74`, `77,77,250`, `1,62,241_trans`...) -> Xanh Nước Công Nghiệp Châu Âu `#0052CC` (*RAL 5005 Signal Blue*) hoặc Trắng Sứ `#F4F6F8`.
    - 30% Khối Kỹ Thuật & Tương Phản:
      + Toàn bộ Đường ống + Phụ kiện uPVC Sch80 (Georg Fischer / +GF+ Standard) -> Xám Đậm `#4A525A` (*RAL 7011 Iron Grey*, `Metallic = 0.0, Roughness = 0.35`).
      + Động cơ Bơm & Đế gang (`5,5,5`, `0,0,0`) -> Đen Công Nghiệp `#1C1E21` (*RAL 9005 Jet Black*, `Metallic = 0.20, Roughness = 0.45`).
      + Bầu lọc & Lưu lượng kế Acrylic (`229,229,229`) -> Kính kỹ thuật `#E8F1F5` (`IOR = 1.49, Transmission = 0.95, Roughness = 0.03`).
    - 10% Điểm Nhấn Thị Giác & Điều Khiển (Visual Management 5S):
      + Tay van bi / Phao lưu lượng: Đỏ `#EB2026` / Cam `#FF6B00` / Xanh `#0052CC` / Vàng `#FFC400`.
    """
    apply_inventor_pbr_materials()

    # Các mã RGB của các đoạn ống phân tuyến CAD trên toàn bộ 11 dự án sẽ được đồng bộ về Xám Đậm uPVC Sch80 Châu Âu (#4A525A - RAL 7011)
    eu_upvc_sch80_pipe_rgbs = {
        (207, 79, 0),     # Ống nước cấp thô (Cam CAD) -> uPVC Sch80 #4A525A
        (255, 76, 0),     # Ống cam đậm -> uPVC Sch80 #4A525A
        (232, 93, 4),     # Ống cam -> uPVC Sch80 #4A525A
        (250, 128, 10),   # Ống cam -> uPVC Sch80 #4A525A
        (142, 76, 38),    # Ống nâu/cam -> uPVC Sch80 #4A525A
        (69, 140, 152),   # Ống nước thành phẩm Xanh lơ -> uPVC Sch80 #4A525A
        (18, 82, 122),    # Ống xanh đậm -> uPVC Sch80 #4A525A
        (24, 76, 120),    # Ống xanh đậm -> uPVC Sch80 #4A525A
        (42, 60, 161),    # Ống xanh -> uPVC Sch80 #4A525A
        (48, 135, 227),   # Ống nhánh xanh dương -> uPVC Sch80 #4A525A
        (56, 189, 248),   # Ống xanh da trời -> uPVC Sch80 #4A525A
        (168, 196, 219),  # Ống xanh nhạt -> uPVC Sch80 #4A525A
        (2, 132, 199),    # Ống nước tinh khiết RO -> uPVC Sch80 #4A525A
        (0, 102, 204),    # Ống nhánh -> uPVC Sch80 #4A525A
        (25, 84, 166),    # Ống nhánh -> uPVC Sch80 #4A525A
        (13, 148, 136),   # Ống xanh cổ vịt -> uPVC Sch80 #4A525A
        (13, 157, 13),    # Ống xanh lá -> uPVC Sch80 #4A525A
        (132, 204, 22),   # Ống tuần hoàn CIP -> uPVC Sch80 #4A525A
        (114, 187, 83),   # Ống xanh lá -> uPVC Sch80 #4A525A
        (131, 88, 197),   # Ống nước thải Tím -> uPVC Sch80 #4A525A
        (147, 51, 234),   # Ống nước thải Concentrate -> uPVC Sch80 #4A525A
        (107, 63, 160),   # Ống tím -> uPVC Sch80 #4A525A
        (255, 254, 246),  # Ống kem/vàng nhạt mặt trước -> uPVC Sch80 #4A525A
        (255, 227, 181),  # Ống đứng mặt trước vàng kem -> uPVC Sch80 #4A525A
        (203, 154, 59),   # Ống đứng liên kết 2 vỏ màng RO vàng đồng -> uPVC Sch80 #4A525A
        (191, 153, 15),   # Phụ kiện / ống vàng đồng -> uPVC Sch80 #4A525A
        (229, 226, 188),  # Ống đứng liên kết 2 vỏ màng RO -> uPVC Sch80 #4A525A
        (212, 175, 55),   # Ống đứng liên kết 2 vỏ màng RO mặt trước -> uPVC Sch80 Đen Xanh
        (221, 221, 13),   # Ống liên kết liên cấp Stage 1-2 vàng CAD -> uPVC Sch80 Đen Xanh
        (255, 255, 0),    # Ống đứng liên kết 2 vỏ màng RO bên phải -> uPVC Sch80 Đen Xanh
        (0, 180, 216),    # Ống xanh lơ -> uPVC Sch80 Đen Xanh
        (37, 179, 213),   # Ống xanh lơ -> uPVC Sch80 Đen Xanh
        (20, 184, 166),   # Ống xanh ngọc -> uPVC Sch80 Đen Xanh
        (128, 128, 128),  # Khớp nối / Ống xám -> uPVC Sch80 Đen Xanh
    }

    has_green_frp = any(_parse_rgb_from_mat_name(m.name) == (16, 171, 74) for m in bpy.data.materials if m)
    eu_stainless_rgbs = {(31, 31, 180), (24, 37, 248), (34, 46, 248)}
    if has_green_frp:
        # Trong dự án RO 2m3/h có cột FRP (16,171,74), mã (1,62,241) là buồng đèn UV / vỏ lọc ngang -> đồng bộ Inox SUS304 xước mờ #C8CDD0
        eu_stainless_rgbs.add((1, 62, 241))

    eu_count = 0
    for mat in bpy.data.materials:
        if not mat or not mat.use_nodes or not mat.node_tree:
            continue
        bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf:
            continue

        rgb = _parse_rgb_from_mat_name(mat.name)
        cur_alpha = float(bsdf.inputs['Alpha'].default_value) if 'Alpha' in bsdf.inputs else 1.0

        # 0. Bồn Composite FRP (`1,62,241`, `16,171,74`, `77,77,250`, `102,255,128`, `155,173,136`, `191,187,166`, `197,194,148`, `199,191,174`)
        # Trong phong cách thực tế Châu Âu (như Ảnh 2 mẫu): Cột lọc Composite / Bồn FRP áp lực là vỏ đặc màu Xanh Nước Công Nghiệp (#0052CC - RAL 5005 Signal Blue, Clearcoat Gelcoat)!
        frp_vessel_rgbs = {(16, 171, 74), (77, 77, 250), (102, 255, 128), (155, 173, 136), (191, 187, 166), (197, 194, 148), (199, 191, 174)}
        if not has_green_frp:
            frp_vessel_rgbs.add((1, 62, 241))
        if rgb in frp_vessel_rgbs:
            mat.blend_method = 'OPAQUE'
            if hasattr(mat, "surface_render_method"):
                try:
                    mat.surface_render_method = 'DITHERED'
                except Exception:
                    pass
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#0052CC", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'Alpha' in bsdf.inputs:
                bsdf.inputs['Alpha'].default_value = 1.0
            if 'Transmission Weight' in bsdf.inputs:
                bsdf.inputs['Transmission Weight'].default_value = 0.0
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.52
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.90
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.04
            bc_final = list(bsdf.inputs['Base Color'].default_value)
            try:
                mat.diffuse_color = (bc_final[0], bc_final[1], bc_final[2], 1.0)
                mat.metallic = 0.0
                mat.roughness = 0.16
            except Exception:
                pass
            eu_count += 1
            continue

        # 1. Khung Skid chịu lực & Buồng UV Inox (`31,31,180`, `24,37,248`, `34,46,248` — trừ chữ nổi `31,31,180_1`) -> Bạc Inox SUS304/316 Sáng Ánh Kim (#D6DEE4)
        if rgb in eu_stainless_rgbs and mat.name != "31,31,180_1":
            mat.blend_method = 'OPAQUE'
            if hasattr(mat, "surface_render_method"):
                try:
                    mat.surface_render_method = 'DITHERED'
                except Exception:
                    pass
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#D6DEE4", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.94
            bsdf.inputs['Roughness'].default_value = 0.20
            if 'Alpha' in bsdf.inputs:
                bsdf.inputs['Alpha'].default_value = 1.0
            if 'Transmission Weight' in bsdf.inputs:
                bsdf.inputs['Transmission Weight'].default_value = 0.0
            if 'Anisotropic' in bsdf.inputs:
                bsdf.inputs['Anisotropic'].default_value = 0.55
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.25
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.08
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.85

        # 1B-1. Mũi tên và lõi lọc trắng
        elif mat.name in ("WT3D_Pipe_Arrow_Mark", "WT3D_Flow_Arrow_White_Mat", "WT3D_7Core_PP_DirtTrap_Mat") or "dirttrap" in mat.name.lower() or "arrow_mark" in mat.name.lower():
            bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.15
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.35

        # 1B-2. Vỏ màng RO trắng và Tủ điện trắng
        elif rgb in ((244, 246, 248), (242, 242, 255), (255, 255, 255)) or any(k in mat.name.lower() for k in ("244,246,248", "242,242,255", "ro_housing")):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#F2F5F8", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.14
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.65

                # 1B-0. Cong tac ap Danfoss KP35 dial scale plate (White Gloss with crisp scale)
        elif mat.name == "WT3D_Danfoss_KP35_Scale_Mat" or ("kp35" in mat.name.lower() and rgb == (64, 64, 64)) or "cong_tac_ap_scale" in mat.name.lower():
            bsdf.inputs['Base Color'].default_value = (0.96, 0.96, 0.96, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.15
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.60
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.40
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = 0.20

        # 1B. Phụ kiện Co, Tê, Rắc co đôi, Mặt bích, Thân van uPVC -> Xám Đá uPVC Sch80 Sáng Chuẩn Inventor (#788694) đồng bộ chuẩn màu và độ bóng Inventor!
        elif rgb in (
            (47, 47, 47),
            (80, 80, 80),
            (89, 96, 114),
            (97, 103, 121),
            (110, 125, 161),
            (123, 124, 127),
            (148, 166, 184),
            (43, 54, 119),
            (45, 54, 107),
            (46, 138, 87),
            (33, 138, 33),
            (78, 86, 94),
        ) or mat.name in ("78,86,94"):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#788694", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.20
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.54
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.45
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.07
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.65

        # 2. Tuyến ống thẳng uPVC Sch80 -> Xám Đá uPVC Sch80 Sáng Chuẩn Inventor (#788694) đồng bộ màu xám đá với phụ kiện uPVC như Inventor!
        elif rgb in eu_upvc_sch80_pipe_rgbs:
            mat.blend_method = 'OPAQUE'
            if hasattr(mat, "surface_render_method"):
                try:
                    mat.surface_render_method = 'DITHERED'
                except Exception:
                    pass
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#788694", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.18
            if 'Alpha' in bsdf.inputs:
                bsdf.inputs['Alpha'].default_value = 1.0
            if 'Transmission Weight' in bsdf.inputs:
                bsdf.inputs['Transmission Weight'].default_value = 0.0
            if 'Anisotropic' in bsdf.inputs:
                bsdf.inputs['Anisotropic'].default_value = 0.0
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = 1.54
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.65
            if 'Coat Roughness' in bsdf.inputs:
                bsdf.inputs['Coat Roughness'].default_value = 0.06
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.72

        elif cur_alpha < 0.98:
            continue

        # 3. Chi tiết nhấn Vàng / Cam chuẩn 5S (`240,215,140`, `254,213,0` -> #FFB800 RAL 1003 Signal Yellow)
        elif rgb in ((240, 215, 140), (254, 213, 0)):
            bsdf.inputs['Base Color'].default_value = _hex_to_rgba("#FFB800", 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.16
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = 0.75

        bc_final = list(bsdf.inputs['Base Color'].default_value)
        try:
            mat.diffuse_color = (bc_final[0], bc_final[1], bc_final[2], 1.0)
            mat.metallic = float(bsdf.inputs['Metallic'].default_value)
            mat.roughness = float(bsdf.inputs['Roughness'].default_value)
        except Exception:
            pass
        inject_keyshot_material_graph(mat)
        eu_count += 1

    return eu_count


def _Ensure_Base_UV_Layer_On_CAD_Meshes():
    """
    Đảm bảo mọi mesh CAD gốc đều có kênh UV tên `UVMap` trước khi Join với các tấm Decal,
    tránh việc UV của Decal bị mất hoặc lệch khi `bpy.ops.object.join()`.
    """
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and not obj.name.startswith("WT3D_Decal_"):
            mesh = obj.data
            if not mesh.uv_layers:
                mesh.uv_layers.new(name="UVMap")
            else:
                mesh.uv_layers.active.name = "UVMap"


def _get_or_create_decal_material(png_filename):
    img_path = os.path.join(DECAL_LIB_DIR, png_filename)
    if not os.path.exists(img_path):
        return None

    mat_name = "WT3D_Decal_" + os.path.splitext(png_filename)[0]
    if mat_name in bpy.data.materials:
        return bpy.data.materials[mat_name]

    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    mat.blend_method = 'OPAQUE'
    if hasattr(mat, "surface_render_method"):
        try:
            mat.surface_render_method = 'DITHERED'
        except Exception:
            pass

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Roughness'].default_value = 0.22
    bsdf.inputs['Metallic'].default_value = 0.0
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = 0.5

    tex = nodes.new('ShaderNodeTexImage')
    img = bpy.data.images.load(img_path, check_existing=True)
    try:
        img.pack()
    except Exception:
        pass
    tex.image = img
    tex.extension = 'CLIP'

    links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    return mat


def add_flat_decal(name, png_filename, center, width, height, facing='-Y'):
    mat = _get_or_create_decal_material(png_filename)
    if not mat:
        return None

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    hw, hh = width * 0.5, height * 0.5
    cx, cy, cz = center

    if facing == '-Y':
        # Nhìn từ -Y: Trái là -X, Phải là +X
        v0 = bm.verts.new((cx - hw, cy, cz - hh))
        v1 = bm.verts.new((cx + hw, cy, cz - hh))
        v2 = bm.verts.new((cx + hw, cy, cz + hh))
        v3 = bm.verts.new((cx - hw, cy, cz + hh))
    elif facing == '+Y':
        # Nhìn từ +Y: Trái là +X, Phải là -X
        v0 = bm.verts.new((cx + hw, cy, cz - hh))
        v1 = bm.verts.new((cx - hw, cy, cz - hh))
        v2 = bm.verts.new((cx - hw, cy, cz + hh))
        v3 = bm.verts.new((cx + hw, cy, cz + hh))
    elif facing == '+X':
        # Nhìn từ +X: Trái là -Y, Phải là +Y
        v0 = bm.verts.new((cx, cy - hw, cz - hh))
        v1 = bm.verts.new((cx, cy + hw, cz - hh))
        v2 = bm.verts.new((cx, cy + hw, cz + hh))
        v3 = bm.verts.new((cx, cy - hw, cz + hh))
    elif facing == '-X':
        # Nhìn từ -X: Trái là +Y, Phải là -Y
        v0 = bm.verts.new((cx, cy + hw, cz - hh))
        v1 = bm.verts.new((cx, cy - hw, cz - hh))
        v2 = bm.verts.new((cx, cy - hw, cz + hh))
        v3 = bm.verts.new((cx, cy + hw, cz + hh))
    else:
        bm.free()
        return None

    face = bm.faces.new((v0, v1, v2, v3))
    uv_layer = bm.loops.layers.uv.new("UVMap")
    uvs = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    for loop, uv in zip(face.loops, uvs):
        loop[uv_layer].uv = uv

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat)
    return obj


def add_cyl_decal(name, png_filename, cx, cy, radius, z_min, z_max, angle_deg, arc_width, segs=28):
    mat = _get_or_create_decal_material(png_filename)
    if not mat:
        return None

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    half_span = (arc_width / max(radius, 0.01)) * 0.5
    center_rad = math.radians(angle_deg)
    # Khi nhìn từ ngoài vào mặt trụ tại góc center_rad:
    # Bên trái của người nhìn là (center_rad - half_span), bên phải là (center_rad + half_span)
    a_start = center_rad - half_span
    a_end = center_rad + half_span

    cols = []
    for i in range(segs + 1):
        u = i / float(segs)
        a = a_start + u * (a_end - a_start)
        x = cx + radius * math.cos(a)
        y = cy + radius * math.sin(a)
        vb = bm.verts.new((x, y, z_min))
        vt = bm.verts.new((x, y, z_max))
        cols.append((vb, vt, u))

    for i in range(segs):
        vb0, vt0, u0 = cols[i]
        vb1, vt1, u1 = cols[i + 1]
        f = bm.faces.new((vb0, vb1, vt1, vt0))
        f.smooth = True
        for loop, uv in zip(f.loops, [(u0, 0.0), (u1, 0.0), (u1, 1.0), (u0, 1.0)]):
            loop[uv_layer].uv = uv

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat)
    return obj


def inject_project_decals(model_hint):
    """
    Tự động gắn các tấm Decal 3D chuẩn xác theo tên dự án/file (hệ tọa độ Mét chuẩn của Blender).
    Nếu mô hình đã có sẵn Decal (`WT3D_Decal_*`), tự động bỏ qua để không nhân đôi.
    """
    for mat in bpy.data.materials:
        if mat and mat.name.startswith("WT3D_Decal_"):
            return 0

    _Ensure_Base_UV_Layer_On_CAD_Meshes()

    hint = (model_hint or "").lower()
    created = []

    # 1. Commercial_Alkaline_Water_Feeder_Cabinet_RO_Booster_1um_0.2um
    if "alkaline" in hint:
        created.append(add_flat_decal("WT3D_Decal_Obj_Brand", "WT3D_Green_Horiz.png", (0.018, -0.539, 1.38), 0.42, 0.075, facing='-Y'))
        created.append(add_flat_decal("WT3D_Decal_Obj_Flow", "Alkaline_Flow_Diagram.png", (0.018, -0.539, 0.88), 0.48, 0.48, facing='-Y'))

    # 2. SKID_Pre_Cartridge_Filter_2x7x40In_SS304_20m3h
    elif "pre_cartridge" in hint or "2x7x40" in hint:
        # Bầu lọc Inox 304 (Y = -0.1575) & Bầu lọc Xanh (Y = +0.1925)
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF1", "CF_01_Vertical.png", -0.0525, -0.1575, 0.1225, 0.42, 1.32, -135.0, 0.13))
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF2", "CF_01_Vertical.png", -0.0525, 0.1925, 0.1225, 0.42, 1.32, -135.0, 0.13))
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF1b", "CF_01_Vertical.png", -0.0525, -0.1575, 0.1225, 0.42, 1.32, -45.0, 0.13))
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF2b", "CF_01_Vertical.png", -0.0525, 0.1925, 0.1225, 0.42, 1.32, 45.0, 0.13))

    # 3. SKID_Ultrafiltration_UF_Dual_10000L_Outside_In_20m3h
    elif "ultrafiltration_uf_dual" in hint or "uf_dual_10000l" in hint or "lap he sieu loc" in hint:
        # 2 màng UF 10000L (cx=0.6795, cy=-0.200 và cy=+0.200, R=0.0695)
        created.append(add_cyl_decal("WT3D_Decal_Obj_UF1", "UF_01_Vertical.png", 0.6795, -0.200, 0.0715, 0.60, 1.38, -35.0, 0.095))
        created.append(add_cyl_decal("WT3D_Decal_Obj_UF2", "UF_01_Vertical.png", 0.6795, 0.200, 0.0715, 0.60, 1.38, 35.0, 0.095))
        # Tủ điện Inox / Nhựa (X=0.855, mặt +X)
        created.append(add_flat_decal("WT3D_Decal_Obj_Cab", "WT3D_Green_Vert.png", (0.978, 0.0, 1.25), 0.045, 0.26, facing='+X'))

    # 4. Water_Softener_Dual_FRP2472_Runxin_N74A3_500L_Tank_20m3h
    elif "frp2472" in hint:
        # Cột FRP 1 (cx=0.0, cy=-0.005, R=0.270) & Cột FRP 2 (cx=-1.0505, cy=0.0, R=0.260)
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF1", "SF_01_4272_Stacked.png", 0.0, -0.005, 0.272, 1.08, 1.30, 90.0, 0.44))
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF2", "SF_01_4272_Stacked.png", -1.0505, 0.0, 0.262, 1.08, 1.30, 90.0, 0.44))
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF1b", "SF_01_4272_Stacked.png", 0.0, -0.005, 0.272, 1.08, 1.30, -90.0, 0.44))
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF2b", "SF_01_4272_Stacked.png", -1.0505, 0.0, 0.262, 1.08, 1.30, -90.0, 0.44))
        # Bồn muối 500L (cx=-0.525, cy=0.425, R=0.387)
        created.append(add_cyl_decal("WT3D_Decal_Obj_Brine", "WT3D_Green_Horiz.png", -0.525, 0.425, 0.415, 0.70, 0.82, 90.0, 0.46))

    # 5. Industrial_RO_Pretreatment_Skid_20m3h_Dual_Cartridge_Softener_UF
    elif "pretreatment_skid_20m3h" in hint:
        # 2 Bầu lọc Cartridge (cx=0.392, cy=-1.1205 & cy=-1.4705, R=0.1205)
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF1", "CF_01_Vertical.png", 0.392, -1.1205, 0.1225, 0.42, 1.32, 35.0, 0.13))
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF2", "CF_01_Vertical.png", 0.392, -1.4705, 0.1225, 0.42, 1.32, 35.0, 0.13))
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF1b", "CF_01_Vertical.png", 0.392, -1.1205, 0.1225, 0.42, 1.32, -45.0, 0.13))
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF2b", "CF_01_Vertical.png", 0.392, -1.4705, 0.1225, 0.42, 1.32, -45.0, 0.13))
        # 2 Màng UF (cx=0.7555, cy=-0.200 & cy=+0.200, R=0.0695)
        created.append(add_cyl_decal("WT3D_Decal_Obj_UF1", "UF_01_Vertical.png", 0.7555, -0.200, 0.0715, 0.70, 1.50, -35.0, 0.095))
        created.append(add_cyl_decal("WT3D_Decal_Obj_UF2", "UF_01_Vertical.png", 0.7555, 0.200, 0.0715, 0.70, 1.50, -35.0, 0.095))
        # 2 Cột làm mềm FRP (cx=-0.889, cy=-0.1225 & cx=-0.894, cy=-1.173, R=0.265)
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF1", "SF_01_4272_Stacked.png", -0.889, -0.1225, 0.267, 1.12, 1.34, 0.0, 0.44))
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF2", "SF_01_4272_Stacked.png", -0.894, -1.173, 0.262, 1.12, 1.34, 0.0, 0.44))
        # Tủ điện trước cụm UF (X=[0.893, 1.052], Y=[-0.108, 0.111], Z=[1.232, 1.532])
        created.append(add_flat_decal("WT3D_Decal_Obj_Flag", "Vietnam_Flag.png", (0.972, -0.110, 1.43), 0.13, 0.088, facing='-Y'))
        created.append(add_flat_decal("WT3D_Decal_Obj_Cab", "CAB_01_1Row.png", (1.054, 0.0, 1.38), 0.18, 0.04, facing='+X'))

    # 6. Industrial_RO_System_2m3h_2Stage_8040_UF_IoT
    elif "ro_system_2m3h" in hint or "8040" in hint:
        # Tủ điện điều khiển (cánh tủ phẳng tại X = -0.488, Y=[0.310, 0.965], Z=[1.000, 1.900])
        created.append(add_flat_decal("WT3D_Decal_Obj_CP", "CP_RO_1Row.png", (-0.490, 0.6375, 1.835), 0.36, 0.052, facing='-X'))
        created.append(add_flat_decal("WT3D_Decal_Obj_Brand", "WT3D_Green_Vert.png", (-0.490, 0.915, 1.45), 0.038, 0.42, facing='-X'))
        created.append(add_flat_decal("WT3D_Decal_Obj_Flag", "Vietnam_Flag.png", (-0.310, 0.308, 1.76), 0.18, 0.12, facing='-Y'))
        # Bầu lọc tinh màu xanh (cx=0.3695, cy=0.0755, R=0.1205)
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF", "CF_01_Vertical.png", 0.3695, 0.0755, 0.1225, 0.78, 1.52, 45.0, 0.13))
        created.append(add_cyl_decal("WT3D_Decal_Obj_CFb", "CF_01_Vertical.png", 0.3695, 0.0755, 0.1225, 0.78, 1.52, -135.0, 0.13))

    # 7. Industrial_Water_Pretreatment_Skid_4m3h_Multimedia_Carbon_Softener
    elif "4m3h-multimedia" in hint or "pretreatment_skid_4m3h" in hint or "multimedia_carbon_softener" in hint:
        # 3 cột lọc FRP dọc theo trục Y
        created.append(add_cyl_decal("WT3D_Decal_Obj_MF", "MF_01_Stacked.png", -0.367, 0.480, 0.160, 0.74, 0.90, 45.0, 0.26))
        created.append(add_cyl_decal("WT3D_Decal_Obj_ACF", "ACF_01_Stacked.png", -0.367, -0.070, 0.156, 0.74, 0.90, 45.0, 0.26))
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF", "SF_01_2162_Stacked.png", -0.2915, -0.5705, 0.231, 1.15, 1.33, 45.0, 0.36))
        # Bồn muối vuông màu trắng (mặt -Y tại Y=-1.272)
        created.append(add_flat_decal("WT3D_Decal_Obj_Brine", "WT3D_Green_Vert.png", (-0.48, -1.272, 0.45), 0.055, 0.46, facing='-Y'))

    # 8. Industrial Water Softener Skid – Dual 2162 FRP Vessels
    elif "2162" in hint or "softener_skid_4m3h" in hint:
        # Cột 1 (cx=0.0, cy=-0.066, R=0.269) & Cột 2 (cx=0.9505, cy=-0.0595, R=0.2625)
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF1", "SF_01_2162_Stacked.png", 0.0, -0.066, 0.272, 1.05, 1.25, -75.0, 0.42))
        created.append(add_cyl_decal("WT3D_Decal_Obj_SF2", "SF_01_2162_Stacked.png", 0.9505, -0.0595, 0.265, 1.05, 1.25, -75.0, 0.42))

    # 9. Johkasou_Chemical_Dosing_System_3Tank_300L
    elif "johkasou" in hint or "3tank" in hint:
        # 3 bảng tên bồn hóa chất ở mặt trước (+Y = 0.9165, Z = 0.600)
        created.append(add_flat_decal("WT3D_Decal_Obj_MethTank", "Tank_METH_1Row.png", (-2.220, 0.9165, 0.600), 0.295, 0.058, facing='+Y'))
        created.append(add_flat_decal("WT3D_Decal_Obj_PacTank", "Tank_PAC_1Row.png", (-1.420, 0.9165, 0.600), 0.295, 0.058, facing='+Y'))
        created.append(add_flat_decal("WT3D_Decal_Obj_NaohTank", "Tank_NAOH_1Row.png", (-0.620, 0.9165, 0.600), 0.295, 0.058, facing='+Y'))

    # 10. Residential_WholeHouse_Water_Purifier_Disc_UF_UV (WholeHouse_Water_Filtration_System_UF_UV)
    elif "wholehouse_water" in hint or "disc_uf_uv" in hint:
        # Bầu lọc xanh (cx=0.219, cy=-0.359, R=0.116, Z=[0.183, 0.783])
        created.append(add_cyl_decal("WT3D_Decal_Obj_CF", "CF_01_Vertical.png", 0.219, -0.359, 0.118, 0.25, 0.72, -45.0, 0.11))
        # Bầu UF Inox góc trước (cx=0.402, cy=-0.740, R=0.110, Z=[0.192, 0.812])
        created.append(add_cyl_decal("WT3D_Decal_Obj_UF", "WT3D_Green_Vert.png", 0.402, -0.740, 0.115, 0.26, 0.70, -65.0, 0.085))

    # 11. Whole_House_UF_Polishing_Skid_2m3h_Dual_Cartridge_UV
    elif "whole_house_uf_polishing" in hint or "dual_cartridge_uv" in hint:
        # Cánh tủ điện màu trắng bên trái (X=[-1.269, -0.219], Y=0.165, Z=[-0.920, 0.238])
        created.append(add_flat_decal("WT3D_Decal_Obj_Brand", "WT3D_Green_Vert.png", (-1.21, 0.163, -0.15), 0.048, 0.42, facing='-Y'))
        created.append(add_flat_decal("WT3D_Decal_Obj_Cab", "CAB_01_1Row.png", (-0.95, 0.163, 0.12), 0.24, 0.045, facing='-Y'))

    created = [o for o in created if o is not None]
    return len(created)
