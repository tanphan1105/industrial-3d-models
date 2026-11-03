"""
==============================================================================
WT3D Studio Control Panel (Blender 4.2+ Add-on & Viewport Sidebar)
Bang dieu khien Camera, Anh Sang, Vat Lieu PBR & 1-Click Render chuan B2
Tich hop He Thong KeyShot Studio Pro (Moi Truong, Anh Sang, 17 Vat Lieu PBR)
Kem Kien Truc Chong Treo May Toan Dien (Anti-Freeze & Zero-Lag Architecture)
Tac gia: Phan Trong Tan (@tanphan1105) - He sinh thai WaterTreatment3D (WT3D)
Vi tri tren phan mem: 3D Viewport > N-Panel (phim N) > Tab 'WT3D Studio'
==============================================================================
"""

bl_info = {
    "name": "WT3D Studio Control Panel (KeyShot Pro Edition)",
    "author": "Phan Trong Tan (@tanphan1105)",
    "version": (1, 3, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar (N) > Tab WT3D Studio",
    "description": "Môi Trường, Ánh Sáng, Vật Liệu Chuẩn KeyShot, Chống Treo Máy và 1-Click Render B2",
    "category": "3D View",
}

import bpy
import mathutils
import math
import os
import time
import subprocess
import tempfile
import gc

# ----------------------------------------------------------------------------
# 1. HELPER FUNCTIONS: BOUNDING BOX, SAFE PATHS & ANTI-FREEZE
# ----------------------------------------------------------------------------
def get_safe_output_dir(raw_dir):
    """Xu ly thu muc xuat an toan, tranh loi PermissionError khi file .blend chua save"""
    if raw_dir.startswith("//"):
        if bpy.data.filepath:
            return bpy.path.abspath(raw_dir)
        else:
            if os.path.exists("D:\\WT3D_Project"):
                fallback_base = "D:\\WT3D_Project\\1_Exports_Batch\\Blender_B2_Renders"
            else:
                fallback_base = os.path.join(os.path.expanduser("~"), "Documents", "WT3D_Renders_B2")
            sub = raw_dir.replace("//", "").strip("/\\")
            return os.path.join(fallback_base, sub) if sub else fallback_base
    return os.path.abspath(raw_dir)

def get_smart_model_name(context):
    """Tu dong nhan dien ten san pham tu file blend hoac mesh CAD dau tien"""
    if bpy.data.filepath:
        name = bpy.path.basename(bpy.data.filepath).replace(".blend", "")
        if name:
            return name
    act = context.active_object
    if act and act.type == 'MESH' and not act.is_shadow_catcher and not act.name.startswith("WT3D_"):
        return act.name.split(".")[0]
    mesh_objs = [obj for obj in context.scene.objects if obj.type == 'MESH' and not obj.is_shadow_catcher and not obj.name.startswith("WT3D_")]
    if mesh_objs:
        return mesh_objs[0].name.split(".")[0]
    return "WT3D_Model"

def get_model_bounds(context):
    """Lay tat ca mesh object hien thi trong scene (bo qua camera, den, san)"""
    mesh_objs = [
        obj for obj in context.scene.objects 
        if obj.type == 'MESH' and not obj.is_shadow_catcher and not obj.name.startswith("WT3D_")
    ]
    if not mesh_objs:
        mesh_objs = [obj for obj in context.scene.objects if obj.type == 'MESH']
    
    if not mesh_objs:
        return None

    all_corners = []
    for obj in mesh_objs:
        mat = obj.matrix_world
        for corner in obj.bound_box:
            all_corners.append(mat @ mathutils.Vector(corner))

    min_x = min(c.x for c in all_corners)
    max_x = max(c.x for c in all_corners)
    min_y = min(c.y for c in all_corners)
    max_y = max(c.y for c in all_corners)
    min_z = min(c.z for c in all_corners)
    max_z = max(c.z for c in all_corners)

    lx = max_x - min_x
    ly = max_y - min_y
    lz = max_z - min_z
    center = mathutils.Vector(((min_x + max_x) / 2.0, (min_y + max_y) / 2.0, (min_z + max_z) / 2.0))
    radius = math.sqrt(lx**2 + ly**2 + lz**2) / 2.0

    return {
        "min": mathutils.Vector((min_x, min_y, min_z)),
        "max": mathutils.Vector((max_x, max_y, max_z)),
        "center": center,
        "size": mathutils.Vector((lx, ly, lz)),
        "radius": radius,
        "ground_z": min_z
    }

def get_or_create_camera(scene):
    cam = scene.camera
    if not cam or cam.name != "WT3D_Master_Camera":
        cam_obj = bpy.data.objects.get("WT3D_Master_Camera")
        if not cam_obj:
            cam_data = bpy.data.cameras.new("WT3D_Master_Camera")
            cam_data.sensor_width = 36.0
            cam_data.sensor_fit = 'HORIZONTAL'
            cam_obj = bpy.data.objects.new("WT3D_Master_Camera", cam_data)
            scene.collection.objects.link(cam_obj)
        else:
            if cam_obj.name not in scene.objects:
                scene.collection.objects.link(cam_obj)
        scene.camera = cam_obj
        cam = cam_obj
    return cam

def aim_camera(cam_obj, eye_pos, target_pos):
    """Dinh huong camera an toan, tu dong cast Vector chong loi tru tuple"""
    eye_vec = mathutils.Vector(eye_pos)
    target_vec = mathutils.Vector(target_pos)
    cam_obj.location = eye_vec
    direction = target_vec - eye_vec
    if direction.length > 1e-6:
        cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

def apply_shot_transform(context, shot_id):
    """Can chinh goc nhin B2 voi thuat toan framing da ti le (16:9, 9:16, 1:1)"""
    scene = context.scene
    bounds = get_model_bounds(context)
    if not bounds:
        return

    try:
        bpy.ops.screen.animation_cancel(restore_frame=False)
    except:
        pass

    cam = get_or_create_camera(scene)
    
    if cam.parent:
        cam.parent = None
        cam.matrix_parent_inverse.identity()
    if cam.animation_data:
        cam.animation_data_clear()

    cam_data = cam.data
    center = bounds["center"]
    size = bounds["size"]
    radius = bounds["radius"]
    ground_z = bounds["ground_z"]
    max_z = bounds["max"].z
    lx, ly, lz = size.x, size.y, size.z

    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    aspect = res_x / res_y if res_y > 0 else (16.0 / 9.0)
    sensor_width = 36.0
    sensor_height = sensor_width / aspect

    def calc_persp_dist(r_span, lens_mm, margin=1.20):
        limiting_dim = min(sensor_width, sensor_height)
        tan_half = (limiting_dim / 2.0) / lens_mm
        return (r_span / tan_half) * margin

    def calc_ortho_scale(w_span, h_span, margin=1.15):
        return max(w_span, h_span * aspect) * margin

    if shot_id == "00_LOW_ANGLE":
        cam_data.type = 'PERSP'
        cam_data.lens = 40.0
        low_dir = mathutils.Vector((0.8, -1.2, 0.05)).normalized()
        dist = calc_persp_dist(radius * 0.95, 40.0, margin=1.28)
        eye = center + low_dir * dist
        target = mathutils.Vector((center.x, center.y, ground_z + lz * 0.60))
        aim_camera(cam, eye, target)

    elif shot_id == "01_OVERALL_HERO":
        cam_data.type = 'PERSP'
        cam_data.lens = 50.0
        iso_dir = mathutils.Vector((1.0, -1.0, 0.65)).normalized()
        dist = calc_persp_dist(radius, 50.0, margin=1.25)
        aim_camera(cam, center + iso_dir * dist, center)

    elif shot_id == "02_PIPING_ROUTING":
        cam_data.type = 'PERSP'
        cam_data.lens = 50.0
        iso_dir = mathutils.Vector((-1.0, -1.0, 0.60)).normalized()
        dist = calc_persp_dist(radius, 50.0, margin=1.25)
        aim_camera(cam, center + iso_dir * dist, center)

    elif shot_id == "03_TOP_PLAN":
        cam_data.type = 'ORTHO'
        is_rotated = ly > lx
        cam_data.ortho_scale = calc_ortho_scale(ly, lx, 1.18) if is_rotated else calc_ortho_scale(lx, ly, 1.18)
        cam.location = mathutils.Vector((center.x, center.y, max_z + radius * 2.5))
        cam.rotation_euler = mathutils.Euler((0, 0, math.radians(90) if is_rotated else 0), 'XYZ')

    elif shot_id == "04_FRONT_ELEVATION":
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = calc_ortho_scale(lx, lz, 1.15)
        cam.location = mathutils.Vector((center.x, center.y - radius * 3.0, center.z))
        cam.rotation_euler = mathutils.Euler((math.radians(90), 0, 0), 'XYZ')

    elif shot_id == "05_RIGHT_PROFILE":
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = calc_ortho_scale(ly, lz, 1.15)
        cam.location = mathutils.Vector((center.x + radius * 3.0, center.y, center.z))
        cam.rotation_euler = mathutils.Euler((math.radians(90), 0, math.radians(90)), 'XYZ')

    elif shot_id == "06_DETAIL_CLOSEUP":
        cam_data.type = 'PERSP'
        cam_data.lens = 75.0
        eye = mathutils.Vector((center.x + radius * 0.95, center.y - radius * 0.95, max_z + radius * 0.2))
        target = mathutils.Vector((center.x, center.y, max_z - lz * 0.18))
        aim_camera(cam, eye, target)


# ----------------------------------------------------------------------------
# 2. PROPERTY GROUP (LUU TRANG THAI CUA PANEL)
# ----------------------------------------------------------------------------
class WT3D_Studio_Properties(bpy.types.PropertyGroup):
    active_tab: bpy.props.EnumProperty(
        name="Phân hệ WT3D",
        description="Chuyển đổi phân hệ điều khiển WT3D Studio phong cách Apple Bento",
        items=[
            ("MATERIALS", "🎨 Vật Liệu", "11 Vật liệu WT3D PBR & 3 Chế độ màu"),
            ("STUDIO", "🌍 Studio", "4 Phông nền & 4 Dàn đèn KeyShot Pro"),
            ("CAMERAS", "🎥 Camera", "7 Góc chụp B2 & Xuất ảnh/video render"),
            ("OPTIMIZE", "⚡ Tối Ưu", "Môi trường CAD Inventor & Chống treo máy"),
        ],
        default="MATERIALS"
    )
    resolution_preset: bpy.props.EnumProperty(
        name="Độ phân giải",
        items=[
            ("4K", "4K UHD (3840x2160)", "Do phan giai 4K sieu net"),
            ("2K", "2K QHD (2560x1440)", "Do phan giai 2K tieu chuan"),
            ("1080P", "Full HD (1920x1080)", "Do phan giai nhanh 1080p")
        ],
        default="4K"
    )
    render_samples: bpy.props.IntProperty(
        name="Samples",
        description="So luong mau lay tia Cycles",
        default=64,
        min=16,
        max=512
    )
    transparent_bg: bpy.props.BoolProperty(
        name="Nền Trong Suốt (Alpha)",
        description="Render nen trong suot de tach nen san pham",
        default=False
    )
    output_dir: bpy.props.StringProperty(
        name="Thư mục xuất",
        subtype='DIR_PATH',
        default="//Renders_B2/"
    )
    video_aspect: bpy.props.EnumProperty(
        name="Tỉ lệ Video",
        items=[
            ("16_9", "16:9 Ngang (B2B/Catalog)", "Video khung ngang"),
            ("9_16", "9:16 Dọc (TikTok/Shorts)", "Video khung doc")
        ],
        default="16_9"
    )
    video_duration: bpy.props.EnumProperty(
        name="Thời lượng",
        items=[
            ("10", "10 Giây (300 frames)", "10s 30fps"),
            ("15", "15 Giây (450 frames)", "15s 30fps")
        ],
        default="10"
    )
    video_style: bpy.props.EnumProperty(
        name="Kiểu quay",
        items=[
            ("TURNTABLE", "🔄 Turntable 360° (Vòng Lặp Vô Tận)", "Xoay tron 360 do"),
            ("DRONE", "🦅 Drone FPV (Bay Lượn Điện Ảnh)", "Bay luon FPV tu xa toi gan")
        ],
        default="TURNTABLE"
    )
    video_engine: bpy.props.EnumProperty(
        name="Render Engine Video",
        items=[
            ("BLENDER_EEVEE_NEXT", "⚡ EEVEE (Siêu Tốc 30s)", "Render sieu nhanh nhe"),
            ("CYCLES", "💎 Cycles OptiX (Dò Tia Siêu Thực)", "Render tia sang PBR dep nhat")
        ],
        default="BLENDER_EEVEE_NEXT"
    )
    color_mode: bpy.props.EnumProperty(
        name="Chế độ màu WT3D",
        items=[
            ("DESIGN", "⭐ DESIGN", "Portfolio, TikTok, Fab, branding (Ban mau thiet ke cao cap)"),
            ("REAL", "🏭 REAL", "Dung de duyet che tao, vat lieu that ngoai cong truong"),
            ("PROCESS", "🔄 PROCESS", "Giai thich dong cong nghe / P&ID theo luu chat"),
            ("DEFAULT", "↶ MẶC ĐỊNH", "Vat lieu xam trung tinh goc ban dau cua CAD Inventor")
        ],
        default="DESIGN"
    )
    mat_category: bpy.props.EnumProperty(
        name="Phân loại Vật Liệu",
        items=[
            ("METALS", "🔩 Kim Loại", "Inox, Thep, Dong, Gang, Nhom"),
            ("POLYMERS", "🧪 Nhựa & Composite", "FRP, u-PVC, PPR, Son Tinh Dien"),
            ("OPTICAL", "💎 Trong Suốt & Dầu", "Acrylic, Kinh, Glycerin"),
            ("ELASTOMERS", "⬛ Cao Su & Silicone", "EPDM, Silicone")
        ],
        default="METALS"
    )


# ----------------------------------------------------------------------------
# 3. OPERATORS (KEYSHOT ENVIRONMENT, LIGHTING, MATERIALS & ANTI-FREEZE)
# ----------------------------------------------------------------------------
class WT3D_OT_AntiFreezeTurbo(bpy.types.Operator):
    """Toi uu phan cung chong treo may, chong lag chuot, chong tran RAM va giu GPU mat me duoi 55 do C"""
    bl_idname = "wt3d.anti_freeze_turbo"
    bl_label = "Chống Treo Máy (Zero-Lag)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        cpu_count = os.cpu_count() or 4
        safe_threads = max(1, cpu_count - 2)
        context.scene.render.threads_mode = 'FIXED'
        context.scene.render.threads = safe_threads

        bpy.context.preferences.edit.undo_memory_limit = 2048
        bpy.context.preferences.edit.undo_steps = 20
        bpy.context.preferences.system.scrollback = 256

        context.scene.cycles.preview_samples = 24
        context.scene.cycles.use_preview_denoising = True
        try:
            context.scene.cycles.preview_denoiser = 'OPTIX'
        except:
            pass
        context.scene.cycles.use_auto_tile = True
        context.scene.cycles.tile_size = 512
        context.scene.cycles.max_bounces = 6
        context.scene.cycles.diffuse_bounces = 3
        context.scene.cycles.glossy_bounces = 3
        context.scene.cycles.transmission_bounces = 4
        context.scene.cycles.transparent_max_bounces = 6

        try:
            context.scene.eevee.taa_render_samples = 32
            context.scene.eevee.taa_samples = 8
        except:
            pass

        # Thiet lap Chong Rang Cua (Anti-Aliasing) chuan sac net
        try:
            bpy.context.preferences.system.viewport_aa = '16'
            bpy.context.preferences.system.anisotropic_filter = 'FILTER_16'
            bpy.context.preferences.system.use_overlay_smooth_wire = True
            bpy.context.preferences.system.use_edit_mode_smooth_wire = True
            context.scene.display.viewport_aa = '16'
            context.scene.display.render_aa = '16'
            context.scene.cycles.pixel_filter_type = 'BLACKMAN_HARRIS'
            context.scene.cycles.filter_width = 1.5
        except:
            pass

        gc.collect()
        try:
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        except:
            pass

        try:
            bpy.ops.wm.save_userpref()
        except:
            pass

        self.report({'INFO'}, f"Da kich hoat Che Do Chong Treo May! (CPU {safe_threads}/{cpu_count} threads, Undo 2GB, Cycles Preview 24 samples OptiX)")
        return {'FINISHED'}

class WT3D_OT_PurgeMemory(bpy.types.Operator):
    """Quet sach toan bo du lieu rac, orphan meshes, textures va giai phong RAM lap tuc"""
    bl_idname = "wt3d.purge_memory"
    bl_label = "Dọn Rác RAM"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        initial_meshes = len(bpy.data.meshes)
        initial_mats = len(bpy.data.materials)
        
        try:
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        except:
            pass
        
        gc.collect()

        freed_meshes = max(0, initial_meshes - len(bpy.data.meshes))
        freed_mats = max(0, initial_mats - len(bpy.data.materials))

        self.report({'INFO'}, f"Da don sach {freed_meshes} mesh rac, {freed_mats} vat lieu rac! RAM da duoc giai phong.")
        return {'FINISHED'}

class WT3D_OT_SetKeyShotEnvironment(bpy.types.Operator):
    """Thiet lap moi truong phong nen chuan KeyShot (1-Click)"""
    bl_idname = "wt3d.set_keyshot_env"
    bl_label = "Phông Nền KeyShot"
    bl_options = {'REGISTER', 'UNDO'}

    env_type: bpy.props.StringProperty()

    def execute(self, context):
        theme = bpy.context.preferences.themes[0]
        v3d = theme.view_3d.space
        v3d.gradients.background_type = 'LINEAR'

        world = context.scene.world
        if not world:
            world = bpy.data.worlds.new("WT3D_World")
            context.scene.world = world
        world.use_nodes = True
        bg_node = next((n for n in world.node_tree.nodes if n.type == 'BACKGROUND'), None)

        if self.env_type == "PURE_WHITE":
            # KeyShot Pure White Studio (Amazon / E-commerce Catalog)
            v3d.gradients.high_gradient = (0.95, 0.96, 0.98)
            v3d.gradients.gradient = (1.0, 1.0, 1.0)
            theme.view_3d.grid = (0.85, 0.85, 0.85, 0.15)
            if bg_node:
                bg_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
                bg_node.inputs['Strength'].default_value = 1.0
            msg = "KeyShot Pure White Studio (Catalog Trắng Tinh)"

        elif self.env_type == "INDUSTRIAL_GREY":
            # KeyShot Industrial Grey Studio (Neutral Tech Pro)
            v3d.gradients.high_gradient = (0.38, 0.40, 0.43)
            v3d.gradients.gradient = (0.20, 0.21, 0.23)
            theme.view_3d.grid = (0.40, 0.40, 0.40, 0.20)
            if bg_node:
                bg_node.inputs['Color'].default_value = (0.32, 0.34, 0.37, 1.0)
                bg_node.inputs['Strength'].default_value = 0.75
            msg = "KeyShot Industrial Grey Studio (Xám Kỹ Thuật Pro)"

        elif self.env_type == "DARK_TECH_NOIR":
            # KeyShot Dark Tech Noir (Apple / OLED Luxury)
            v3d.gradients.high_gradient = (0.12, 0.13, 0.15)
            v3d.gradients.gradient = (0.04, 0.05, 0.06)
            theme.view_3d.grid = (0.20, 0.20, 0.20, 0.15)
            if bg_node:
                bg_node.inputs['Color'].default_value = (0.05, 0.05, 0.07, 1.0)
                bg_node.inputs['Strength'].default_value = 0.35
            msg = "KeyShot Dark Tech Noir (Đen Quyến Rũ OLED)"

        else:
            # Inventor Classic Winter Night
            v3d.gradients.high_gradient = (0.76, 0.82, 0.88)
            v3d.gradients.gradient = (0.93, 0.95, 0.97)
            theme.view_3d.grid = (0.70, 0.74, 0.78, 0.35)
            if bg_node:
                bg_node.inputs['Color'].default_value = (0.95, 0.95, 0.96, 1.0)
                bg_node.inputs['Strength'].default_value = 0.85
            msg = "Autodesk Inventor Winter Night (Xanh Xám Truyền Thống)"

        try:
            bpy.ops.wm.save_userpref()
        except:
            pass

        self.report({'INFO'}, f"Da chuyen sang moi truong: {msg}")
        return {'FINISHED'}

class WT3D_OT_SetKeyShotLightingRig(bpy.types.Operator):
    """Thiet lap dan den Studio chuan KeyShot (3 Diem, Den Dinh, Dual Rim, Tan Deu)"""
    bl_idname = "wt3d.set_keyshot_lighting"
    bl_label = "Dàn Đèn KeyShot"
    bl_options = {'REGISTER', 'UNDO'}

    rig_type: bpy.props.StringProperty()

    def execute(self, context):
        bounds = get_model_bounds(context)
        if not bounds:
            self.report({'WARNING'}, "Khong tim thay mo hinh 3D de can chinh den!")
            return {'CANCELLED'}

        center = bounds["center"]
        radius = bounds["radius"]
        ground_z = bounds["ground_z"]

        def get_or_create_light(name):
            obj = bpy.data.objects.get(name)
            if not obj:
                ldata = bpy.data.lights.new(name=name, type='AREA')
                obj = bpy.data.objects.new(name, ldata)
                context.scene.collection.objects.link(obj)
            else:
                if obj.name not in context.scene.objects:
                    context.scene.collection.objects.link(obj)
            return obj

        key = get_or_create_light("WT3D_KeyLight")
        fill = get_or_create_light("WT3D_FillLight")
        rim = get_or_create_light("WT3D_RimLight")

        base_power = radius * radius * 120.0

        if self.rig_type == "OVERHEAD_DIFFUSER":
            # 1. Den Dinh Dau Showroom (Softbox tran chieu thang xuong)
            key.data.shape = 'RECTANGLE'
            key.data.size = radius * 3.0
            key.data.size_y = radius * 2.5
            key.data.energy = base_power * 1.5
            key.data.color = (1.0, 1.0, 1.0)
            key.location = (center.x, center.y, center.z + radius * 2.4)
            aim_camera(key, key.location, center)

            # Fill truoc mat thap
            fill.data.shape = 'RECTANGLE'
            fill.data.size = radius * 2.0
            fill.data.size_y = radius * 1.2
            fill.data.energy = base_power * 0.35
            fill.data.color = (0.95, 0.98, 1.0)
            fill.location = (center.x, center.y - radius * 2.2, ground_z + radius * 0.4)
            aim_camera(fill, fill.location, center)

            # Rim vien phia sau
            rim.data.shape = 'RECTANGLE'
            rim.data.size = radius * 2.0
            rim.data.size_y = radius * 0.8
            rim.data.energy = base_power * 0.45
            rim.data.color = (1.0, 0.98, 0.95)
            rim.location = (center.x, center.y + radius * 2.0, center.z + radius * 1.2)
            aim_camera(rim, rim.location, center)
            msg = "Đèn Đỉnh Đầu Showroom (Overhead Diffuser)"

        elif self.rig_type == "DUAL_RIM_DRAMATIC":
            # 2. Dual Rim Dien Anh (2 den vien sau chieu doi xung cuc net cho kim loai)
            key.data.shape = 'RECTANGLE'
            key.data.size = radius * 1.8
            key.data.size_y = radius * 1.2
            key.data.energy = base_power * 0.40
            key.data.color = (0.98, 0.98, 1.0)
            key.location = (center.x, center.y - radius * 2.0, center.z + radius * 0.8)
            aim_camera(key, key.location, center)

            # Rim trai sau (135 do)
            fill.data.shape = 'RECTANGLE'
            fill.data.size = radius * 1.5
            fill.data.size_y = radius * 1.0
            fill.data.energy = base_power * 1.25
            fill.data.color = (0.95, 0.98, 1.0)
            fill.location = (center.x - radius * 1.8, center.y + radius * 1.8, center.z + radius * 1.2)
            aim_camera(fill, fill.location, center)

            # Rim phai sau (225 do)
            rim.data.shape = 'RECTANGLE'
            rim.data.size = radius * 1.5
            rim.data.size_y = radius * 1.0
            rim.data.energy = base_power * 1.25
            rim.data.color = (1.0, 0.98, 0.92)
            rim.location = (center.x + radius * 1.8, center.y + radius * 1.8, center.z + radius * 1.2)
            aim_camera(rim, rim.location, center)
            msg = "Dual Rim Viền Điện Ảnh (Sắc Nét Kim Loại)"

        elif self.rig_type == "EVEN_SOFT_BOOTH":
            # 3. Tan Deu 360 do (Softbox lon khong goc chet cho thuong mai dien tu)
            key.data.shape = 'RECTANGLE'
            key.data.size = radius * 2.5
            key.data.size_y = radius * 2.0
            key.data.energy = base_power * 0.70
            key.data.color = (1.0, 1.0, 1.0)
            key.location = (center.x + radius * 1.8, center.y - radius * 1.6, center.z + radius * 1.2)
            aim_camera(key, key.location, center)

            fill.data.shape = 'RECTANGLE'
            fill.data.size = radius * 2.5
            fill.data.size_y = radius * 2.0
            fill.data.energy = base_power * 0.70
            fill.data.color = (1.0, 1.0, 1.0)
            fill.location = (center.x - radius * 1.8, center.y - radius * 1.6, center.z + radius * 1.2)
            aim_camera(fill, fill.location, center)

            rim.data.shape = 'RECTANGLE'
            rim.data.size = radius * 3.0
            rim.data.size_y = radius * 2.0
            rim.data.energy = base_power * 0.70
            rim.data.color = (1.0, 1.0, 1.0)
            rim.location = (center.x, center.y, center.z + radius * 2.2)
            aim_camera(rim, rim.location, center)
            msg = "Tản Đều 360° Không Góc Chết (Studio E-Commerce)"

        else:
            # 4. Studio 3 Diem Chuẩn (Mac dinh)
            key.data.shape = 'RECTANGLE'
            key.data.size = radius * 1.5
            key.data.size_y = radius * 1.0
            key.data.energy = base_power
            key.data.color = (1.0, 0.98, 0.95)
            key.location = (center.x + radius * 1.8, center.y - radius * 1.8, center.z + radius * 1.6)
            aim_camera(key, key.location, center)

            fill.data.shape = 'RECTANGLE'
            fill.data.size = radius * 2.0
            fill.data.size_y = radius * 1.5
            fill.data.energy = base_power * 0.40
            fill.data.color = (0.92, 0.96, 1.0)
            fill.location = (center.x - radius * 2.0, center.y - radius * 1.2, center.z + radius * 0.8)
            aim_camera(fill, fill.location, center)

            rim.data.shape = 'RECTANGLE'
            rim.data.size = radius * 1.8
            rim.data.size_y = radius * 0.8
            rim.data.energy = base_power * 0.70
            rim.data.color = (1.0, 1.0, 1.0)
            rim.location = (center.x, center.y + radius * 2.2, center.z + radius * 2.0)
            aim_camera(rim, rim.location, center)
            msg = "Studio 3 Điểm Tiêu Chuẩn (Key 45°, Fill 40%, Rim 70%)"

        self.report({'INFO'}, f"Da thiet lap: {msg}")
        return {'FINISHED'}

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def hex_to_linear_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    r = srgb_to_linear(int(hex_code[0:2], 16) / 255.0)
    g = srgb_to_linear(int(hex_code[2:4], 16) / 255.0)
    b = srgb_to_linear(int(hex_code[4:6], 16) / 255.0)
    return (round(r, 4), round(g, 4), round(b, 4), 1.0)

# ============================================================================
# WT3D COLOR + GLOSS / ROUGHNESS GUIDE (3 CHẾ ĐỘ PHỐI MÀU CHUYÊN BIỆT)
# 1. REAL: Duyệt chế tạo, vật liệu thật công trường
# 2. DESIGN ★: Portfolio, TikTok, Fab, Branding (11 vật liệu chuẩn thiết kế)
# 3. PROCESS: Giải thích dòng công nghệ / P&ID theo lưu chất
# ============================================================================
WT3D_THEMES = {
    "DESIGN": {
        "label": "DESIGN ★",
        "badge": "Portfolio, TikTok, Fab, Branding",
        "materials": {
            "HMI": ("WT3D_HMI_BlackGlass", "#111315", 0.0, 0.08, 1.0, 0.0, 1.52, 0.0, "01. Kính HMI Glass (Black Glass #111315 | R=0.08)"),
            "INOX": ("WT3D_Inox_Brushed", "#B9C0C5", 0.98, 0.22, 0.10, 0.0, 1.45, 0.60, "02. Inox 304/316 (Brushed #B9C0C5 | R=0.22)"),
            "VALVE": ("WT3D_Tay_Van_Orange", "#F47721", 0.0, 0.28, 0.25, 0.0, 1.45, 0.0, "03. Tay Van Accent (Orange #F47721 | R=0.28)"),
            "PIPE_MAIN": ("WT3D_Ong_Chinh_DeepWaterBlue", "#12527A", 0.0, 0.32, 0.15, 0.0, 1.46, 0.0, "04. Ống Chính (Deep Water Blue #12527A | R=0.32)"),
            "RO_HOUSING": ("WT3D_RO_Housing_SoftWhite", "#F5F6F6", 0.0, 0.34, 0.35, 0.0, 1.48, 0.0, "05. RO Housing (Soft White #F5F6F6 | R=0.34)"),
            "PIPE_CLEAN": ("WT3D_Ong_Sach_Teal", "#258C8C", 0.0, 0.35, 0.10, 0.0, 1.46, 0.0, "06. Ống Sạch / Phụ (Teal #258C8C | R=0.35)"),
            "CABINET": ("WT3D_Tu_Dien_PearlGrey", "#E3E5E5", 0.05, 0.38, 0.15, 0.0, 1.45, 0.0, "07. Tủ Điện (Pearl Grey #E3E5E5 | R=0.38)"),
            "FRAME": ("WT3D_Khung_Skid_Graphite", "#252A2E", 0.10, 0.46, 0.0, 0.0, 1.45, 0.0, "08. Khung Skid (Graphite #252A2E | R=0.46)"),
            "MOTOR": ("WT3D_Motor_Charcoal", "#202326", 0.25, 0.52, 0.0, 0.0, 1.45, 0.0, "09. Motor Bơm (Charcoal #202326 | R=0.52)"),
            "SENSOR": ("WT3D_Sensor_DarkPolymer", "#2C3135", 0.0, 0.55, 0.0, 0.0, 1.46, 0.0, "10. Sensor / Gauge (#2C3135 | R=0.55)"),
            "CABLE": ("WT3D_Cable_SoftBlack", "#1A1C1E", 0.0, 0.68, 0.0, 0.0, 1.50, 0.0, "11. Cable / Cao Su (Soft Black #1A1C1E | R=0.68)"),
            "BRASS": ("WT3D_Dong_Thau_Gold", "#D4AF37", 0.95, 0.20, 0.15, 0.0, 1.45, 0.50, "12. Đồng Thau Kim Loại (Gold Brass #D4AF37 | R=0.20)")
        }
    },
    "REAL": {
        "label": "REAL",
        "badge": "Duyệt chế tạo, vật liệu thật công trường",
        "materials": {
            "HMI": ("WT3D_Real_Kinh_HMI", "#0F1012", 0.0, 0.05, 1.0, 0.0, 1.52, 0.0, "01. Kính Màn Hình HMI (#0F1012 | R=0.05)"),
            "INOX": ("WT3D_Real_Inox_304", "#C8CBCE", 0.98, 0.20, 0.15, 0.0, 1.45, 0.65, "02. Inox 304 Thực Tế (#C8CBCE | R=0.20)"),
            "VALVE": ("WT3D_Real_Tay_Van_DoCam", "#D83A20", 0.0, 0.30, 0.20, 0.0, 1.45, 0.0, "03. Tay Van Đỏ Cam (#D83A20 | R=0.30)"),
            "PIPE_MAIN": ("WT3D_Real_Ong_uPVC_Xam", "#484E55", 0.0, 0.34, 0.0, 0.0, 1.46, 0.0, "04. Ống u-PVC Xám (#484E55 | R=0.34)"),
            "RO_HOUSING": ("WT3D_Real_Vo_Mang_Composite", "#ECEBE6", 0.0, 0.30, 0.40, 0.0, 1.48, 0.0, "05. Vỏ Màng RO Trắng Ngà (#ECEBE6 | R=0.30)"),
            "PIPE_CLEAN": ("WT3D_Real_Ong_PPR_Xanh", "#2D5A3E", 0.0, 0.40, 0.05, 0.0, 1.46, 0.0, "06. Ống PPR Hàn Nhiệt (#2D5A3E | R=0.40)"),
            "CABINET": ("WT3D_Real_Tu_Dien_Ral7035", "#CED2D6", 0.05, 0.40, 0.10, 0.0, 1.45, 0.0, "07. Tủ Điện Ral 7035 (#CED2D6 | R=0.40)"),
            "FRAME": ("WT3D_Real_Khung_MaKem", "#6B7278", 0.85, 0.38, 0.10, 0.0, 1.45, 0.0, "08. Khung Thép Mạ Kẽm (#6B7278 | R=0.38)"),
            "MOTOR": ("WT3D_Real_Motor_Gang_Xanh", "#233342", 0.20, 0.55, 0.0, 0.0, 1.45, 0.0, "09. Motor Bơm Gang Xám (#233342 | R=0.55)"),
            "SENSOR": ("WT3D_Real_Sensor_NhuaDen", "#202020", 0.0, 0.60, 0.0, 0.0, 1.46, 0.0, "10. Sensor Nhựa Đen (#202020 | R=0.60)"),
            "CABLE": ("WT3D_Real_Cap_CaoSu_EPDM", "#151515", 0.0, 0.75, 0.0, 0.0, 1.50, 0.0, "11. Cáp & Đệm EPDM (#151515 | R=0.75)"),
            "BRASS": ("WT3D_Real_Dong_Thau", "#CB9A3B", 0.92, 0.25, 0.15, 0.0, 1.45, 0.55, "12. Đồng Thau Kỹ Thuật (#CB9A3B | R=0.25)")
        }
    },
    "PROCESS": {
        "label": "PROCESS",
        "badge": "Giải thích dòng công nghệ / P&ID",
        "materials": {
            "HMI": ("WT3D_PID_HMI_Display", "#111315", 0.0, 0.08, 1.0, 0.0, 1.52, 0.0, "01. Màn Hình SCADA/HMI (#111315 | R=0.08)"),
            "INOX": ("WT3D_PID_Nuoc_RO_Permeate", "#0D47A1", 0.0, 0.28, 0.20, 0.0, 1.46, 0.0, "02. Nước RO Permeate (#0D47A1 | R=0.28)"),
            "VALVE": ("WT3D_PID_Hoa_Chat_Dosing", "#FBC02D", 0.0, 0.28, 0.25, 0.0, 1.45, 0.0, "03. Đường Hóa Chất / CIP (#FBC02D | R=0.28)"),
            "PIPE_MAIN": ("WT3D_PID_Nuoc_Cap_RawWater", "#4A90E2", 0.0, 0.30, 0.15, 0.0, 1.46, 0.0, "04. Nước Cấp Raw Water (#4A90E2 | R=0.30)"),
            "RO_HOUSING": ("WT3D_PID_Vo_Mang_RO", "#F5F6F6", 0.0, 0.34, 0.35, 0.0, 1.48, 0.0, "05. Vỏ Màng RO Tinh Khiết (#F5F6F6 | R=0.34)"),
            "PIPE_CLEAN": ("WT3D_PID_Nuoc_Loc_Pretreated", "#34A853", 0.0, 0.30, 0.15, 0.0, 1.46, 0.0, "06. Nước Lọc Pretreated (#34A853 | R=0.30)"),
            "CABINET": ("WT3D_PID_Tu_Dien_White", "#E0E0E0", 0.05, 0.38, 0.15, 0.0, 1.45, 0.0, "07. Tủ Điều Khiển PLC (#E0E0E0 | R=0.38)"),
            "FRAME": ("WT3D_PID_Khung_TrungTinh", "#2B2D30", 0.10, 0.50, 0.0, 0.0, 1.45, 0.0, "08. Khung Bệ Trung Tính (#2B2D30 | R=0.50)"),
            "MOTOR": ("WT3D_PID_Bom_DongLuc", "#424242", 0.30, 0.50, 0.0, 0.0, 1.45, 0.0, "09. Bơm Động Lực (#424242 | R=0.50)"),
            "SENSOR": ("WT3D_PID_Tiet_Trung_UV", "#7B1FA2", 0.0, 0.30, 0.20, 0.0, 1.46, 0.0, "10. Tiệt Trùng UV / Khử Khuẩn (#7B1FA2 | R=0.30)"),
            "CABLE": ("WT3D_PID_Duong_Xai_Reject", "#78909C", 0.0, 0.35, 0.10, 0.0, 1.46, 0.0, "11. Đường Nước Thải Reject (#78909C | R=0.35)"),
            "BRASS": ("WT3D_PID_Dong_Thau", "#D4AF37", 0.92, 0.25, 0.15, 0.0, 1.45, 0.55, "12. Đồng Thau Kỹ Thuật (#D4AF37 | R=0.25)")
        }
    },
    "DEFAULT": {
        "label": "MẶC ĐỊNH GỐC",
        "badge": "Vật liệu chuẩn kỹ thuật CAD Inventor",
        "materials": {
            "HMI": ("WT3D_CAD_Default_Kinh", "#1F2327", 0.0, 0.10, 0.8, 0.0, 1.50, 0.0, "01. Kính HMI CAD (#1F2327 | R=0.10)"),
            "INOX": ("WT3D_CAD_Default_Inox", "#BEBCBA", 0.85, 0.25, 0.0, 0.0, 1.45, 0.50, "02. Inox Kim Loại CAD (#BEBCBA | R=0.25)"),
            "VALVE": ("WT3D_CAD_Default_TayVan", "#C84B31", 0.0, 0.35, 0.0, 0.0, 1.45, 0.0, "03. Tay Van Đỏ CAD (#C84B31 | R=0.35)"),
            "PIPE_MAIN": ("WT3D_CAD_Default_OngXam", "#6E747C", 0.0, 0.35, 0.0, 0.0, 1.46, 0.0, "04. Ống uPVC Xám CAD (#6E747C | R=0.35)"),
            "RO_HOUSING": ("WT3D_CAD_Default_Trang", "#E8ECEF", 0.0, 0.35, 0.0, 0.0, 1.48, 0.0, "05. Nhựa Trắng / Vỏ Màng CAD (#E8ECEF | R=0.35)"),
            "PIPE_CLEAN": ("WT3D_CAD_Default_OngPPR", "#2E8A57", 0.0, 0.35, 0.0, 0.0, 1.46, 0.0, "06. Ống PPR Xanh CAD (#2E8A57 | R=0.35)"),
            "CABINET": ("WT3D_CAD_Default_TuDien", "#C5CBD1", 0.05, 0.40, 0.0, 0.0, 1.45, 0.0, "07. Tủ Điện CAD (#C5CBD1 | R=0.40)"),
            "FRAME": ("WT3D_CAD_Default_Khung", "#8B9198", 0.60, 0.35, 0.0, 0.0, 1.45, 0.0, "08. Khung Kim Loại CAD (#8B9198 | R=0.35)"),
            "MOTOR": ("WT3D_CAD_Default_DongCo", "#3E444B", 0.20, 0.45, 0.0, 0.0, 1.45, 0.0, "09. Động Cơ Gang CAD (#3E444B | R=0.45)"),
            "SENSOR": ("WT3D_CAD_Default_DoLuong", "#2D3238", 0.10, 0.55, 0.0, 0.0, 1.46, 0.0, "10. Cảm Biến / Đồng Hồ CAD (#2D3238 | R=0.55)"),
            "CABLE": ("WT3D_CAD_Default_PhuTro", "#1F2124", 0.0, 0.70, 0.0, 0.0, 1.50, 0.0, "11. Phụ Trợ / Đệm Đen CAD (#1F2124 | R=0.70)"),
            "BRASS": ("WT3D_CAD_Default_DongThau", "#CB9A3B", 0.88, 0.28, 0.0, 0.0, 1.45, 0.50, "12. Đồng Thau CAD (#CB9A3B | R=0.28)")
        }
    }
}

import unicodedata, re

def strip_accents(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFD', str(text))
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn').replace('đ', 'd').replace('Đ', 'D').lower()

def classify_rgb(r, g, b):
    # Check green (PPR pipe / body)
    if g > 0.35 and g > r * 1.15 and g > b * 1.15:
        return 'PIPE_CLEAN'
    # Check yellow/brass/gold
    if r > 0.55 and g > 0.38 and b < 0.35:
        return 'BRASS'
    # Check red/orange (Handle / Accent)
    if r > 0.65 and g < 0.35 and b < 0.35:
        return 'VALVE'
    if r > 0.70 and 0.20 <= g <= 0.55 and b < 0.30:
        return 'VALVE'
    # Check blue (Water / Pipe main)
    if b > 0.40 and b > r * 1.20 and b > g * 1.10:
        return 'PIPE_MAIN'
    # Check neutral metal/gray/black/white
    diff = max(abs(r-g), abs(g-b), abs(r-b))
    if diff < 0.08:
        if r > 0.93:
            return 'RO_HOUSING'
        elif r >= 0.50:
            return 'INOX'
        elif r >= 0.35:
            return 'PIPE_MAIN'
        else:
            return 'CABLE'
    return 'FRAME'

def get_reverse_material_map():
    rev = {}
    for theme_key, theme_data in WT3D_THEMES.items():
        for key, spec in theme_data["materials"].items():
            mat_name = spec[0].lower()
            rev[mat_name] = key
    return rev

def determine_slot_category(mat, rev_map):
    if not mat:
        return "FRAME"
    m_name = mat.name.lower()
    
    # 1. Reverse lookup from existing WT3D materials
    if m_name in rev_map:
        return rev_map[m_name]
    for key, spec_key in rev_map.items():
        if key in m_name:
            return spec_key
            
    # 2. Check RGB format in material name (e.g. '203,154,59', '46,138,87', '190,188,186_1')
    match = re.match(r'^(\d+),(\d+),(\d+)', mat.name)
    if match:
        r = int(match.group(1)) / 255.0
        g = int(match.group(2)) / 255.0
        b = int(match.group(3)) / 255.0
        return classify_rgb(r, g, b)
        
    # 3. Check actual diffuse_color or Principled BSDF color
    bsdf = mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes and mat.node_tree else None
    if bsdf and bsdf.inputs.get('Base Color'):
        base_col = bsdf.inputs['Base Color'].default_value
        if base_col:
            cat = classify_rgb(base_col[0], base_col[1], base_col[2])
            if cat != 'FRAME':
                return cat
    if hasattr(mat, 'diffuse_color'):
        diff_col = mat.diffuse_color
        cat = classify_rgb(diff_col[0], diff_col[1], diff_col[2])
        if cat != 'FRAME':
            return cat
            
    # 4. Check semantic keywords in slot material name
    tag = strip_accents(mat.name)
    if any(k in tag for k in ['tay gat', 'tay van', 'handle', 'lever', 'volang', 'vo lang', 'knob', 'accent', 'handwheel', 'cam', 'do', 'orange', 'red']):
        return "VALVE"
    elif any(k in tag for k in ['dong', 'brass', 'bronze', 'gold']):
        return "BRASS"
    elif any(k in tag for k in ['inox', 'ss304', 'ss316', 'sus', 'stainless', 'thep', 'steel', 'metal', 'bolt', 'nut', 'oc', 'vit', 'flange', 'bich']):
        return "INOX"
    elif any(k in tag for k in ['ppr', 'xanh', 'green']):
        return "PIPE_CLEAN"
    elif any(k in tag for k in ['upvc', 'pvc', 'xam', 'grey', 'gray']):
        return "PIPE_MAIN"
    elif any(k in tag for k in ['coil', 'cuon', 'dien', 'den', 'black', 'rubber', 'cao su', 'epdm', 'cable', 'day']):
        return "CABLE"
    elif any(k in tag for k in ['trang', 'white', 'ro', 'housing', 'membrane', 'frp', 'ptfe', 'teflon']):
        return "RO_HOUSING"
    elif any(k in tag for k in ['glass', 'kinh', 'hmi', 'screen', 'lcd']):
        return "HMI"
    elif any(k in tag for k in ['tu dien', 'cabinet', 'panel', 'box', 'dien']):
        return "CABINET"
        
    return "INOX"

def determine_single_part_category(obj, mat, rev_map, min_all_z, count):
    # 1. Reverse lookup from existing material if it's already a WT3D material
    if mat:
        m_lower = mat.name.lower()
        if m_lower in rev_map:
            return rev_map[m_lower]
        for k, v in rev_map.items():
            if k in m_lower:
                return v
        match = re.match(r'^(\d+),(\d+),(\d+)', mat.name)
        if match:
            r = int(match.group(1)) / 255.0
            g = int(match.group(2)) / 255.0
            b = int(match.group(3)) / 255.0
            cat = classify_rgb(r, g, b)
            if cat != 'FRAME':
                return cat

    raw_tag = f"{obj.name} {obj.data.name} {mat.name if mat else ''}"
    tag = strip_accents(raw_tag)

    # A. HMI / Kinh
    if any(k in tag for k in ['hmi', 'screen', 'touch', 'display', 'kinh', 'glass', 'man hinh', 'lcd']):
        return "HMI"
        
    # B. TAY VAN ACCENT (CHI TAY GAT / TAY VAN / NUM / VO LANG / LEVER - TUYET DOI KHONG CHUA 'VALVE' HAY 'VAN' CHUNG CHUNG!)
    if any(k in tag for k in ['tay gat', 'tay van', 'handle', 'lever', 'volang', 'vo lang', 'knob', 'handwheel', 'accent', 'nut xoay']):
        return "VALVE"

    # C. DONG THAU (BRASS)
    if any(k in tag for k in ['dong thau', 'brass', 'bronze', 'dong vang']):
        return "BRASS"

    # D. INOX & KIM LOAI
    if any(k in tag for k in ['inox', 'ss304', 'ss316', 'sus', 'stainless', 'flange', 'bich', 'clamp', 'cum', 'khop noi', 'dau noi', 'ren', 'bolt', 'nut', 'oc vit', 'ti ren']):
        return "INOX"

    # E. THAN VAN / CUM VAN (Neu khong phai la tay gat)
    if any(k in tag for k in ['valve', 'van', 'ball valve', 'van bi', 'van buom', 'check valve', 'van 1 chieu', 'solenoid', 'van dien tu', 'van lay mau', 'van xa khi', 'y-strainer', 'loc y']):
        if any(k in tag for k in ['inox', 'ss', 'sus', 'metal', 'thep']):
            return "INOX"
        elif any(k in tag for k in ['dong', 'brass']):
            return "BRASS"
        elif any(k in tag for k in ['ppr']):
            return "PIPE_CLEAN"
        else:
            return "PIPE_MAIN"

    # F. PHU KIEN DUONG ONG (CO, TE, CUT, RAC CO, MANG SONG)
    if any(k in tag for k in ['co 90', 'co 45', 'cut', 'elbow', 'te', 'tee', 'rac co', 'union', 'thap', 'mang song', 'con thu', 'giam', 'fitting']):
        if any(k in tag for k in ['inox', 'ss', 'sus']):
            return "INOX"
        elif any(k in tag for k in ['ppr']):
            return "PIPE_CLEAN"
        else:
            return "PIPE_MAIN"

    # G. VO MANG RO / BON LOC / COMPOSITE
    if any(k in tag for k in ['ro', 'housing', 'membrane', 'vo mang', 'vessel', 'bon', 'cot loc', 'composite', 'tank', 'frp', 'ap luc']):
        return "RO_HOUSING"

    # H. DUONG ONG CHINH
    if any(k in tag for k in ['main', 'feed', 'inlet', 'header', 'ong chinh', 'tuyen chinh', 'ong cap', 'hut', 'day', 'd60', 'd90', 'd114', 'dn50', 'dn80', 'dn100', 'upvc']):
        return "PIPE_MAIN"

    # I. DUONG ONG SACH / PHU / NHANH / PPR
    if any(k in tag for k in ['clean', 'permeate', 'sach', 'phu', 'branch', 'nhanh', 'pipe', 'ong', 'ppr', 'xa', 'thai', 'drain', 'reject', 'concentrate', 'd27', 'd34', 'd42', 'd49', 'dn20', 'dn25', 'dn32']):
        return "PIPE_CLEAN"

    # J. TU DIEN
    if any(k in tag for k in ['tu dien', 'cabinet', 'enclosure', 'panel', 'box', 'dien', 'control', 'plc', 'hop dien']):
        return "CABINET"

    # K. KHUNG SKID
    if any(k in tag for k in ['skid', 'frame', 'khung', 'be', 'base', 'chan', 'beam', 'column', 'thep', 'u100', 'u120', 'i100', 'hop', 'gia do']):
        return "FRAME"

    # L. MOTOR BOM
    if any(k in tag for k in ['motor', 'pump', 'bom', 'dong co', 'engine', 'dau bom', 'truc dung', 'ly tam', 'ebara', 'grundfos', 'pentax', 'cnp']):
        return "MOTOR"

    # M. CAM BIEN / DONG HO
    if any(k in tag for k in ['sensor', 'cam bien', 'meter', 'gauge', 'dong ho', 'flow', 'trans', 'rotameter', 'ap suat', 'luu luong', 'ec', 'tds', 'ph', 'uv']):
        return "SENSOR"

    # N. CAP / CAO SU / DEM
    if any(k in tag for k in ['cable', 'day', 'rubber', 'cao su', 'dem', 'gasket', 'seal', 'chong rung', 'chan de', 'ruot ga', 'epdm', 'silicon']):
        return "CABLE"

    # Geometric heuristic fallback
    dims = sorted([obj.dimensions.x, obj.dimensions.y, obj.dimensions.z])
    max_dim = dims[2]
    mid_dim = dims[1]
    min_dim = max(dims[0], 0.001)
    ratio = max_dim / min_dim
    vol = obj.dimensions.x * obj.dimensions.y * obj.dimensions.z

    if ratio > 4.0 and max_dim > 0.25:
        return "PIPE_MAIN" if min_dim > 0.045 else "PIPE_CLEAN"
    elif obj.dimensions.z > 0.7 or (ratio > 2.0 and vol > 0.05):
        return "RO_HOUSING"
    elif obj.location.z <= (min_all_z + 0.35) and (obj.dimensions.x > 0.5 or obj.dimensions.y > 0.5):
        return "FRAME"
    elif max_dim < 0.10:
        return "INOX"
    elif vol > 0.08 and obj.location.z > (min_all_z + 0.6):
        return "CABINET"
    elif any(k in obj.name.lower() for k in ['mesh', 'part', 'solid']):
        fallbacks = ["PIPE_MAIN", "INOX", "PIPE_CLEAN", "MOTOR", "FRAME"]
        return fallbacks[count % len(fallbacks)]
    else:
        return "FRAME"


def create_or_sync_material_from_spec(spec):
    name, hex_code, metal, rough, coat, trans, ior, aniso, label = spec
    col = hex_to_linear_rgb(hex_code)
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
    
    # Gan Viewport Display Color cho Solid Mode (KHU TRIET DE MAU XAM)
    mat.diffuse_color = (col[0], col[1], col[2], 1.0)
    mat.roughness = rough
    mat.metallic = metal
    
    bsdf = mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes else None
    if bsdf:
        bsdf.inputs['Base Color'].default_value = col
        bsdf.inputs['Metallic'].default_value = metal
        bsdf.inputs['Roughness'].default_value = rough
        if 'Coat Weight' in bsdf.inputs:
            bsdf.inputs['Coat Weight'].default_value = coat
        if 'IOR' in bsdf.inputs:
            bsdf.inputs['IOR'].default_value = ior
        if 'Anisotropic' in bsdf.inputs:
            bsdf.inputs['Anisotropic'].default_value = aniso
    return mat

class WT3D_OT_AssignWT3DGuideMaterial(bpy.types.Operator):
    """Gan vat lieu cong nghiep chuan WT3D Color + Gloss cho chi tiet dang chon"""
    bl_idname = "wt3d.assign_guide_mat"
    bl_label = "Gán Vật Liệu WT3D Guide"
    bl_options = {'REGISTER', 'UNDO'}

    mat_key: bpy.props.StringProperty()

    def execute(self, context):
        selected_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected_objs:
            self.report({'WARNING'}, "Vui lòng chọn ít nhất 1 chi tiết (Mesh) trước khi gán vật liệu!")
            return {'CANCELLED'}

        mode = context.scene.wt3d_props.color_mode
        theme_cfg = WT3D_THEMES.get(mode, WT3D_THEMES["DESIGN"])
        spec = theme_cfg["materials"].get(self.mat_key)
        if not spec:
            return {'CANCELLED'}

        mat = create_or_sync_material_from_spec(spec)
        for obj in selected_objs:
            if not obj.data.materials:
                obj.data.materials.append(mat)
            else:
                for i in range(len(obj.data.materials)):
                    obj.data.materials[i] = mat

        label = spec[8]
        self.report({'INFO'}, f"Đã gán [{mode}]: {label} cho {len(selected_objs)} chi tiết!")
        return {'FINISHED'}

class WT3D_OT_ApplyColorMode(bpy.types.Operator):
    """Chuyen doi giua 3 che do phoi mau: REAL | DESIGN ★ | PROCESS"""
    bl_idname = "wt3d.apply_color_mode"
    bl_label = "Chuyển Chế Độ Phối Màu"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.StringProperty()

    def execute(self, context):
        if self.mode in WT3D_THEMES:
            context.scene.wt3d_props.color_mode = self.mode
            theme_info = WT3D_THEMES[self.mode]
            if self.mode == "DEFAULT":
                bpy.ops.wt3d.reset_all_materials_cad()
            else:
                bpy.ops.wt3d.auto_assign_wt3d_hierarchy(mode=self.mode, all_objects=True)
            self.report({'INFO'}, f"Đã áp dụng chế độ: {theme_info['label']} ({theme_info['badge']})")
        return {'FINISHED'}

class WT3D_OT_AutoAssignWT3DHierarchy(bpy.types.Operator):
    """Tu dong phan bo vat lieu chuan WT3D Hierarchy cho toan bo cac chi tiet trong Skid theo che do dang chon"""
    bl_idname = "wt3d.auto_assign_wt3d_hierarchy"
    bl_label = "Tự Động Phân Bổ Bảng Màu WT3D Cụm Skid"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.StringProperty(default="")
    all_objects: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        target_mode = self.mode if self.mode in WT3D_THEMES else context.scene.wt3d_props.color_mode
        theme_cfg = WT3D_THEMES.get(target_mode, WT3D_THEMES["DESIGN"])
        mats_dict = theme_cfg["materials"]
        rev_map = get_reverse_material_map()

        # Uu tien toan bo mesh neu all_objects=True hoac khong chon gi
        if self.all_objects or not context.selected_objects:
            targets = [obj for obj in context.scene.objects if obj.type == 'MESH']
        else:
            targets = [obj for obj in context.selected_objects if obj.type == 'MESH']
            if not targets:
                targets = [obj for obj in context.scene.objects if obj.type == 'MESH']

        if not targets:
            self.report({'WARNING'}, "Không tìm thấy chi tiết máy nào trong Scene để phân bổ màu!")
            return {'CANCELLED'}

        # Tinh toan chieu cao Z toi thieu cua Skid de nhan dien khung de
        min_all_z = min(obj.location.z for obj in targets)

        count = 0
        for obj in targets:
            # 0. Luu danh sach vat lieu goc ban dau kem thong so mau 1 lan duy nhat de phuc vu Reset
            if "_wt3d_orig_materials" not in obj and obj.data.materials:
                orig_list = []
                for m in obj.data.materials:
                    if m:
                        m.use_fake_user = True  # Poka-Yoke: Chong Blender don rac tu dong xoa mat datablock
                        bsdf = m.node_tree.nodes.get('Principled BSDF') if m.use_nodes and m.node_tree else None
                        col = list(bsdf.inputs['Base Color'].default_value) if bsdf else list(m.diffuse_color)
                        met = bsdf.inputs['Metallic'].default_value if bsdf else (m.metallic if hasattr(m, 'metallic') else 0.0)
                        rou = bsdf.inputs['Roughness'].default_value if bsdf else (m.roughness if hasattr(m, 'roughness') else 0.4)
                        orig_list.append(f"{m.name}|{col[0]:.4f},{col[1]:.4f},{col[2]:.4f}|{met:.2f}|{rou:.2f}")
                obj["_wt3d_orig_materials"] = orig_list

            num_slots = len(obj.data.materials)
            if num_slots == 0:
                key = determine_single_part_category(obj, None, rev_map, min_all_z, count)
                mat_spec = mats_dict.get(key, mats_dict["FRAME"])
                mat = create_or_sync_material_from_spec(mat_spec)
                obj.data.materials.append(mat)
            elif num_slots == 1:
                m = obj.data.materials[0]
                key = determine_single_part_category(obj, m, rev_map, min_all_z, count)
                mat_spec = mats_dict.get(key, mats_dict.get("FRAME"))
                mat = create_or_sync_material_from_spec(mat_spec)
                obj.data.materials[0] = mat
            else:
                # MULTI-MATERIAL COMPONENT (Van dien tu, Bom, Loc dia, Cum mang...)
                # Phan bo rieng biet tung slot theo mau CAD / ten vat lieu slot do (POKA-YOKE CHONG BI DO/XAM TOAN BO!)
                for i in range(num_slots):
                    m = obj.data.materials[i]
                    slot_key = determine_slot_category(m, rev_map)
                    mat_spec = mats_dict.get(slot_key, mats_dict.get("INOX"))
                    mat = create_or_sync_material_from_spec(mat_spec)
                    obj.data.materials[i] = mat

            count += 1

        # Dam bao moi Viewport deu bat che do mau MATERIAL
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.color_type = 'MATERIAL'

        self.report({'INFO'}, f"[{theme_cfg['label']}] Đã phân bổ màu kỹ thuật chuẩn cho {count} chi tiết máy!")
        return {'FINISHED'}


class WT3D_OT_AssignKeyShotMaterial(bpy.types.Operator):
    """Gan vat lieu PBR cong nghiep chuan KeyShot cho cac chi tiet dang chon"""
    bl_idname = "wt3d.assign_keyshot_mat"
    bl_label = "Gán Vật Liệu KeyShot"
    bl_options = {'REGISTER', 'UNDO'}

    mat_id: bpy.props.StringProperty()

    def execute(self, context):
        selected_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected_objs:
            self.report({'WARNING'}, "Vui long chon it nhat 1 chi tiet (Mesh) truoc khi gan vat lieu!")
            return {'CANCELLED'}

        # Thu vien 17 vat lieu PBR chuan KeyShot
        # (Ten, BaseColor, Metallic, Roughness, Coat, Transmission, IOR, Anisotropic)
        mat_db = {
            # 1. Kim loai
            "INOX_BRUSHED": ("KeyShot_Inox_304_Brushed", (0.86, 0.87, 0.88, 1.0), 0.98, 0.22, 0.20, 0.0, 1.45, 0.65),
            "INOX_MIRROR": ("KeyShot_Inox_316_Mirror", (0.95, 0.95, 0.96, 1.0), 1.0, 0.04, 0.50, 0.0, 1.45, 0.0),
            "STEEL_GALVANIZED": ("KeyShot_Steel_Galvanized", (0.75, 0.76, 0.78, 1.0), 0.85, 0.38, 0.10, 0.0, 1.45, 0.0),
            "BRASS_MACHINED": ("KeyShot_Brass_Machined", (0.90, 0.74, 0.26, 1.0), 0.92, 0.22, 0.20, 0.0, 1.45, 0.40),
            "CAST_IRON_BLACK": ("KeyShot_Cast_Iron_Black", (0.10, 0.11, 0.12, 1.0), 0.30, 0.65, 0.15, 0.0, 1.45, 0.0),
            "ALU_ANODIZED": ("KeyShot_Alu_Anodized_Matte", (0.82, 0.83, 0.85, 1.0), 0.90, 0.35, 0.10, 0.0, 1.45, 0.20),

            # 2. Nhua, Composite & Son
            "FRP_DEEP_BLUE": ("KeyShot_FRP_Deep_Blue", (0.03, 0.25, 0.52, 1.0), 0.03, 0.10, 0.85, 0.0, 1.48, 0.0),
            "FRP_NATURAL_CREAM": ("KeyShot_FRP_Natural_Cream", (0.91, 0.89, 0.83, 1.0), 0.02, 0.14, 0.75, 0.0, 1.48, 0.0),
            "UPVC_DARK_GREY": ("KeyShot_uPVC_Dark_Grey", (0.20, 0.23, 0.26, 1.0), 0.0, 0.32, 0.0, 0.0, 1.46, 0.0),
            "PPR_GREEN": ("KeyShot_PPR_Green", (0.15, 0.42, 0.25, 1.0), 0.0, 0.40, 0.05, 0.0, 1.46, 0.0),
            "POWDER_ORANGE": ("KeyShot_Powder_Orange", (0.92, 0.38, 0.06, 1.0), 0.05, 0.36, 0.35, 0.0, 1.45, 0.0),
            "POWDER_GREEN": ("KeyShot_Powder_Green", (0.08, 0.45, 0.22, 1.0), 0.05, 0.36, 0.35, 0.0, 1.45, 0.0),

            # 3. Trong suot & Dung dich
            "CLEAR_ACRYLIC": ("KeyShot_Clear_Acrylic", (0.98, 0.99, 1.0, 1.0), 0.0, 0.01, 0.0, 1.0, 1.49, 0.0),
            "OPTICAL_GLASS": ("KeyShot_Optical_Glass", (0.95, 0.98, 1.0, 1.0), 0.0, 0.005, 0.0, 1.0, 1.52, 0.0),
            "GLYCERIN_LIQUID": ("KeyShot_Glycerin_Liquid", (0.92, 0.96, 0.98, 1.0), 0.0, 0.01, 0.0, 1.0, 1.47, 0.0),

            # 4. Cao su & Silicone
            "EPDM_RUBBER": ("KeyShot_EPDM_Rubber", (0.06, 0.06, 0.07, 1.0), 0.0, 0.78, 0.0, 0.0, 1.50, 0.0),
            "SILICONE_WHITE": ("KeyShot_Silicone_White", (0.85, 0.86, 0.88, 1.0), 0.0, 0.45, 0.0, 0.35, 1.43, 0.0),
        }

        cfg = mat_db.get(self.mat_id)
        if not cfg:
            return {'CANCELLED'}

        name, col, metal, rough, coat, trans, ior, aniso = cfg

        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
        
        # Gan Viewport Display Color cho Solid Mode (KHU TRIET DE MAU XAM)
        mat.diffuse_color = col
        mat.roughness = rough
        mat.metallic = metal

        bsdf = mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes else None
        if bsdf:
            bsdf.inputs['Base Color'].default_value = col
            bsdf.inputs['Metallic'].default_value = metal
            bsdf.inputs['Roughness'].default_value = rough
            if 'Coat Weight' in bsdf.inputs:
                bsdf.inputs['Coat Weight'].default_value = coat
            if 'Transmission Weight' in bsdf.inputs:
                bsdf.inputs['Transmission Weight'].default_value = trans
            if 'IOR' in bsdf.inputs:
                bsdf.inputs['IOR'].default_value = ior
            if 'Anisotropic' in bsdf.inputs:
                bsdf.inputs['Anisotropic'].default_value = aniso

        for obj in selected_objs:
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)
            else:
                for idx in range(len(obj.data.materials)):
                    obj.data.materials[idx] = mat

        self.report({'INFO'}, f"Da gan vat lieu {name} cho {len(selected_objs)} chi tiet!")
        return {'FINISHED'}

class WT3D_OT_SetViewportMode(bpy.types.Operator):
    """Chuyen doi nhanh giua cac che do hien thi: Solid CAD, PBR Material Preview, Render Cycles"""
    bl_idname = "wt3d.set_viewport_mode"
    bl_label = "Chế Độ Hiển Thị Viewport"
    bl_options = {'REGISTER'}

    mode: bpy.props.StringProperty(default="MATERIAL")

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        sh = space.shading
                        if self.mode == "SOLID":
                            sh.type = 'SOLID'
                            sh.color_type = 'MATERIAL'
                            sh.show_cavity = True
                            sh.cavity_type = 'WORLD'
                            sh.show_shadows = False
                            sh.show_object_outline = True
                        elif self.mode == "MATERIAL":
                            sh.type = 'MATERIAL'
                        elif self.mode == "RENDERED":
                            sh.type = 'RENDERED'
        self.report({'INFO'}, f"Đã chuyển chế độ hiển thị Viewport sang: {self.mode}")
        return {'FINISHED'}

class WT3D_OT_FixAllGrayMaterials(bpy.types.Operator):
    """Khu hoan toan mau xam: Dong bo Base Color Principled BSDF sang Viewport Display Color va ap dung bang mau cho Skid"""
    bl_idname = "wt3d.fix_all_gray_materials"
    bl_label = "Khử Màu Xám (Đồng Bộ Màu)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        synced_mats = 0
        for mat in bpy.data.materials:
            if mat.use_nodes and mat.node_tree:
                bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if bsdf and 'Base Color' in bsdf.inputs:
                    c = bsdf.inputs['Base Color'].default_value
                    mat.diffuse_color = (c[0], c[1], c[2], 1.0)
                    if 'Roughness' in bsdf.inputs:
                        mat.roughness = bsdf.inputs['Roughness'].default_value
                    if 'Metallic' in bsdf.inputs:
                        mat.metallic = bsdf.inputs['Metallic'].default_value
                    synced_mats += 1

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.color_type = 'MATERIAL'

        # Kiem tra mesh chua co vat lieu
        unassigned_meshes = [obj for obj in context.scene.objects if obj.type == 'MESH' and not obj.data.materials]
        if unassigned_meshes:
            bpy.ops.wt3d.auto_assign_wt3d_hierarchy()
            self.report({'INFO'}, f"Đã khử màu xám: Đồng bộ {synced_mats} vật liệu & gán cho {len(unassigned_meshes)} chi tiết!")
        else:
            self.report({'INFO'}, f"Đã khử màu xám: Đồng bộ màu hiển thị cho {synced_mats} vật liệu!")

        return {'FINISHED'}

class WT3D_OT_ResetAllMaterialsToCADDefault(bpy.types.Operator):
    """Khoi phuc vat lieu CAD goc ban dau hoac bang mau CAD ky thuat cho toan bo chi tiet (GAN IN-PLACE KHONG GO CLEAR DE GIU NGUYEN POLYGON INDEX)"""
    bl_idname = "wt3d.reset_all_materials_cad"
    bl_label = "Trả Lại Vật Liệu Mặc Định Gốc"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        default_theme = WT3D_THEMES["DEFAULT"]["materials"]
        count = 0

        for obj in context.scene.objects:
            if obj.type != 'MESH':
                continue

            orig_mats = obj.get("_wt3d_orig_materials")
            restored_slots = False

            if orig_mats:
                # POKA-YOKE: TUYET DOI KHONG DUNG obj.data.materials.clear() VI SE LAM RESET TOAN BO POLYGON MATERIAL_INDEX VE 0!
                for idx, item in enumerate(orig_mats):
                    m_name = str(item)
                    col = None
                    met = 0.0
                    rou = 0.35

                    if '|' in m_name:
                        parts = m_name.split('|')
                        m_name = parts[0]
                        if len(parts) > 1:
                            rgb_p = [float(x) for x in parts[1].split(',')]
                            col = (rgb_p[0], rgb_p[1], rgb_p[2], 1.0)
                        if len(parts) > 2:
                            met = float(parts[2])
                        if len(parts) > 3:
                            rou = float(parts[3])
                    else:
                        match = re.match(r'^(\d+),(\d+),(\d+)', m_name)
                        if match:
                            r = int(match.group(1)) / 255.0
                            g = int(match.group(2)) / 255.0
                            b = int(match.group(3)) / 255.0
                            col = (r, g, b, 1.0)
                            diff = max(abs(r-g), abs(g-b), abs(r-b))
                            if (r > 0.55 and g > 0.38 and b < 0.35) or (diff < 0.08 and r >= 0.50):
                                met = 0.90
                                rou = 0.25
                            else:
                                met = 0.0
                                rou = 0.35

                    m = bpy.data.materials.get(m_name)
                    if not m:
                        m = bpy.data.materials.new(name=m_name)
                        m.use_nodes = True
                    m.use_fake_user = True

                    if col:
                        m.diffuse_color = col
                        bsdf = m.node_tree.nodes.get('Principled BSDF') if m.use_nodes and m.node_tree else None
                        if bsdf:
                            bsdf.inputs['Base Color'].default_value = col
                            bsdf.inputs['Metallic'].default_value = met
                            bsdf.inputs['Roughness'].default_value = rou

                    # Gan in-place de bao toan 100% lien ket mat da giac
                    if idx < len(obj.data.materials):
                        obj.data.materials[idx] = m
                    else:
                        obj.data.materials.append(m)

                while len(obj.data.materials) > len(orig_mats):
                    obj.data.materials.pop(index=len(obj.data.materials)-1)

                restored_slots = True

            if not restored_slots:
                num_slots = len(obj.data.materials)
                rev_map = get_reverse_material_map()
                if num_slots <= 1:
                    key = determine_single_part_category(obj, obj.data.materials[0] if num_slots == 1 else None, rev_map, 0, count)
                    mat_spec = default_theme.get(key, default_theme["FRAME"])
                    mat = create_or_sync_material_from_spec(mat_spec)
                    if num_slots == 0:
                        obj.data.materials.append(mat)
                    else:
                        obj.data.materials[0] = mat
                else:
                    for i in range(num_slots):
                        m = obj.data.materials[i]
                        slot_key = determine_slot_category(m, rev_map)
                        mat_spec = default_theme.get(slot_key, default_theme["INOX"])
                        obj.data.materials[i] = create_or_sync_material_from_spec(mat_spec)

            count += 1

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        sh = space.shading
                        sh.type = 'SOLID'
                        sh.color_type = 'MATERIAL'
                        sh.show_cavity = True
                        sh.cavity_type = 'WORLD'
                        sh.show_shadows = False
                        sh.show_object_outline = True
                        sh.object_outline_color = (0.15, 0.15, 0.15)

        context.scene.wt3d_props.color_mode = "DEFAULT"
        self.report({'INFO'}, f"Đã khôi phục hoàn toàn vật liệu CAD kỹ thuật cho {count} chi tiết máy!")
        return {'FINISHED'}

class WT3D_OT_RevertFileFromDisk(bpy.types.Operator):
    """Nap lai file goc tu o cung (Huy bo moi thay doi chua luu de tro ve trang thai file ban dau)"""
    bl_idname = "wt3d.revert_file_from_disk"
    bl_label = "Nạp Lại File Gốc (Revert)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.data.filepath:
            bpy.ops.wm.revert_mainfile()
            self.report({'INFO'}, "Đã nạp lại file gốc từ đĩa thành công!")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "File chưa được lưu trên đĩa, không thể Revert!")
            return {'CANCELLED'}


class WT3D_OT_SwitchShot(bpy.types.Operator):
    """Chuyen doi goc nhin Camera B2 va nhin qua ong kinh"""
    bl_idname = "wt3d.switch_shot"
    bl_label = "Chuyển góc Camera"
    bl_options = {'REGISTER', 'UNDO'}

    shot_id: bpy.props.StringProperty()

    def execute(self, context):
        apply_shot_transform(context, self.shot_id)
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.region_3d.view_perspective = 'CAMERA'
        self.report({'INFO'}, f"Da chuyen goc nhin B2: {self.shot_id}")
        return {'FINISHED'}

class WT3D_OT_SetupStudioRig(bpy.types.Operator):
    """Tu dong do dac mo hinh moi va dung Studio 3 diem sang + San Shadow Catcher"""
    bl_idname = "wt3d.setup_studio_rig"
    bl_label = "🛠️ Khởi Tạo Studio Cho Dự Án Mới"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.mode != 'OBJECT':
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
            except:
                pass

        bounds = get_model_bounds(context)
        if not bounds:
            self.report({'WARNING'}, "Khong tim thay mo hinh 3D nao trong Scene de khoi tao Studio!")
            return {'CANCELLED'}

        center = bounds["center"]
        radius = bounds["radius"]
        ground_z = bounds["ground_z"]

        ground = bpy.data.objects.get("WT3D_Studio_ShadowCatcher")
        if not ground:
            bpy.ops.mesh.primitive_plane_add(size=radius * 8.0, location=(center.x, center.y, ground_z - 0.002))
            ground = context.active_object
            ground.name = "WT3D_Studio_ShadowCatcher"
            ground.is_shadow_catcher = True
        else:
            ground.location = (center.x, center.y, ground_z - 0.002)
            ground.dimensions = (radius * 8.0, radius * 8.0, 0)

        # Khoi tao dan den 3 diem mac dinh
        bpy.ops.wt3d.set_keyshot_lighting(rig_type="3POINT_STUDIO")

        # Camera mac dinh
        apply_shot_transform(context, "01_OVERALL_HERO")

        # Cau hinh Cycles OptiX & Anti-freeze
        context.scene.render.engine = 'CYCLES'
        caddon = bpy.context.preferences.addons.get('cycles')
        if caddon:
            cpref = caddon.preferences
            cpref.get_devices()
            for dev in ['OPTIX', 'CUDA']:
                if [d for d in cpref.devices if d.type == dev]:
                    cpref.compute_device_type = dev
                    for d in cpref.devices:
                        d.use = (d.type == dev)
                    break
            context.scene.cycles.device = 'GPU'
            context.scene.cycles.use_denoising = True

        bpy.ops.wt3d.anti_freeze_turbo()

        self.report({'INFO'}, f"Da thiet lap Studio hoan chinh cho mo hinh (Radius={radius:.1f})!")
        return {'FINISHED'}

class WT3D_OT_AutoFrame(bpy.types.Operator):
    """Tu dong can chinh lai Camera khong bi cat vat the"""
    bl_idname = "wt3d.auto_frame"
    bl_label = "🎯 Căn Lại Khung Hình"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_shot_transform(context, "01_OVERALL_HERO")
        self.report({'INFO'}, "Da can chinh lai khung hinh theo Bounding Box!")
        return {'FINISHED'}

class WT3D_OT_ApplyInventorTheme(bpy.types.Operator):
    """Thiet lap nen Gradient Xanh-Trang, Nhanh nhe chong lag, Vien net CAD giong het Autodesk Inventor"""
    bl_idname = "wt3d.apply_inventor_theme"
    bl_label = "⚡ 1-Click: Môi Trường Chuẩn Inventor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 1. Background Theme (Inventor Winter Night Blue-Grey Gradient)
        bpy.ops.wt3d.set_keyshot_env(env_type="INVENTOR_CLASSIC")

        # 2. Thao tac chuot & Dieu huong CAD
        inputs = bpy.context.preferences.inputs
        inputs.use_zoom_to_mouse = True
        inputs.use_rotate_around_active = True
        inputs.view_rotate_method = 'TURNTABLE'

        # 3. Kich hoat che do chong treo may toan dien
        bpy.ops.wt3d.anti_freeze_turbo()

        # 4. Viewport Shading & Tat Luoi San (Clean Background)
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.overlay.show_floor = False
                        space.overlay.show_axis_x = False
                        space.overlay.show_axis_y = False
                        space.overlay.show_ortho_grid = False
                        if space.clip_start < 0.04:
                            space.clip_start = 0.05

                        sh = space.shading
                        sh.type = 'SOLID'
                        sh.light = 'STUDIO'
                        sh.color_type = 'MATERIAL'
                        # WORLD cavity: Tinh theo curvature goc mat cong mesh thuc (khong bi soc van Moire depth buffer khi zoom)
                        sh.show_cavity = True
                        sh.cavity_type = 'WORLD'
                        sh.cavity_ridge_factor = 1.0
                        sh.cavity_valley_factor = 1.0
                        sh.show_object_outline = True
                        sh.object_outline_color = (0.15, 0.15, 0.15)
                        sh.show_shadows = False
                        sh.background_type = 'THEME'

        try:
            bpy.ops.wm.save_userpref()
        except:
            pass

        self.report({'INFO'}, "Da thiet lap moi truong Autodesk Inventor (Kem bao ve chong treo may)!")
        return {'FINISHED'}

class WT3D_OT_ToggleGrid(bpy.types.Operator):
    """Bat / Tat luoi san va truc toa do tren Viewport"""
    bl_idname = "wt3d.toggle_grid"
    bl_label = "Lưới Sàn"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        ol = space.overlay
                        new_state = not ol.show_floor
                        ol.show_floor = new_state
                        ol.show_axis_x = new_state
                        ol.show_axis_y = new_state
                        ol.show_ortho_grid = new_state
        return {'FINISHED'}

class WT3D_OT_ToggleShadedEdges(bpy.types.Operator):
    """Bat / Tat vien net ky thuat va tao khoi Cavity (Shaded with Edges)"""
    bl_idname = "wt3d.toggle_shaded_edges"
    bl_label = "Nét Viền CAD"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        sh = space.shading
                        new_state = not sh.show_object_outline
                        sh.show_object_outline = new_state
                        sh.show_cavity = new_state
                        sh.cavity_type = 'WORLD'
                        sh.cavity_ridge_factor = 1.0
                        sh.cavity_valley_factor = 1.0
                        sh.show_shadows = False
                        sh.background_type = 'THEME'
        return {'FINISHED'}

class WT3D_OT_FixViewportRipples(bpy.types.Operator):
    """Khu hoan toan soc van gon song Moire va Shadow Acne khi zoom gan tren mat cong CAD trong Solid Mode"""
    bl_idname = "wt3d.fix_viewport_ripples"
    bl_label = "Khử Sọc Gợn Sóng Khi Zoom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.clip_start < 0.04:
                            space.clip_start = 0.05
                        sh = space.shading
                        sh.show_shadows = False
                        sh.show_cavity = True
                        sh.cavity_type = 'WORLD'
                        sh.cavity_ridge_factor = 1.0
                        sh.cavity_valley_factor = 1.0
                        sh.show_object_outline = True
                        sh.object_outline_color = (0.15, 0.15, 0.15)
                        count += 1
        self.report({'INFO'}, f"Da khu triet de soc gon song Moire tren {count} Viewport 3D!")
        return {'FINISHED'}

class WT3D_OT_RestoreBlenderTheme(bpy.types.Operator):
    """Khoi phuc ve giao dien va mau nen goc cua Blender"""
    bl_idname = "wt3d.restore_blender_theme"
    bl_label = "Về Mặc Định"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        theme = bpy.context.preferences.themes[0]
        v3d = theme.view_3d.space
        v3d.gradients.background_type = 'SINGLE_COLOR'
        v3d.gradients.high_gradient = (0.24, 0.24, 0.24)
        v3d.gradients.gradient = (0.19, 0.19, 0.19)
        theme.view_3d.grid = (0.35, 0.35, 0.35, 0.30)
        
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        sh = space.shading
                        sh.show_object_outline = False
                        sh.show_cavity = False
                        sh.show_shadows = False
                        sh.background_type = 'THEME'

        try:
            bpy.ops.wm.save_userpref()
        except:
            pass

        self.report({'INFO'}, "Da hoan nguyen ve giao dien Blender goc!")
        return {'FINISHED'}

class WT3D_OT_ReloadStudioCode(bpy.types.Operator):
    """Nap lai toan bo ma nguon panel truc tiep tren Viewport ma khong can tat mo lai Blender"""
    bl_idname = "wt3d.reload_code"
    bl_label = "Cập Nhật Mã Nguồn Panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        startup_file = r"C:\Users\PHAN TRONG TAN\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\startup\wt3d_studio_panel.py"
        ztools_file = r"D:\WT3D_Project\Z_Tools\wt3d_studio_panel.py"
        target = startup_file if os.path.exists(startup_file) else ztools_file
        try:
            with open(target, 'r', encoding='utf-8') as f:
                code = f.read()
            exec(code, globals())
            if "reload_wt3d_panel" in globals():
                globals()["reload_wt3d_panel"]()
            elif "register" in globals():
                globals()["register"]()
            self.report({'INFO'}, "Đã nạp lại giao diện Apple Bento WT3D Studio thành công!")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Lỗi nạp lại mã: {e}")
            return {'CANCELLED'}

class WT3D_OT_SetHighAntiAliasing(bpy.types.Operator):
    """Kich hoat khu rang cua cuc dai (16x MSAA + Anisotropic 16x + Blackman-Harris Filter)"""
    bl_idname = "wt3d.set_high_anti_aliasing"
    bl_label = "Khử Răng Cưa Cực Đại"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 1. System Preferences Anti-Aliasing & Anisotropic
        try:
            bpy.context.preferences.system.viewport_aa = '16'
            bpy.context.preferences.system.anisotropic_filter = 'FILTER_16'
            bpy.context.preferences.system.use_overlay_smooth_wire = True
            bpy.context.preferences.system.use_edit_mode_smooth_wire = True
        except:
            pass

        # 2. Scene Viewport Display Anti-Aliasing
        try:
            context.scene.display.viewport_aa = '16'
            context.scene.display.render_aa = '16'
        except:
            pass

        # 3. Cycles Pixel Filter (Anti-Aliasing)
        try:
            context.scene.cycles.pixel_filter_type = 'BLACKMAN_HARRIS'
            context.scene.cycles.filter_width = 1.5
        except:
            pass

        # 4. EEVEE Next Temporal Anti-Aliasing
        try:
            context.scene.eevee.taa_samples = 16
            context.scene.eevee.taa_render_samples = 64
            context.scene.eevee.use_taa_reprojection = True
        except:
            pass

        try:
            bpy.ops.wm.save_userpref()
        except:
            pass

        self.report({'INFO'}, "Đã kích hoạt Khử Răng Cưa Cực Đại (16x MSAA + Lọc Blackman-Harris)!")
        return {'FINISHED'}


def _wt3d_purge_hidden_objects_and_faces(context):
    """Xoa cac object dang an (H / Outliner) va cac mat/part dang an trong Edit Mode (L + H)"""
    removed_objs = 0
    removed_faces = 0
    try:
        if context.active_object and context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

    for obj in list(bpy.data.objects):
        if obj.type == 'MESH':
            is_hidden = False
            try:
                is_hidden = obj.hide_get() or obj.hide_viewport or obj.hide_render
            except Exception:
                is_hidden = obj.hide_viewport or obj.hide_render
            if is_hidden:
                bpy.data.objects.remove(obj, do_unlink=True)
                removed_objs += 1

    mesh_objs = [o for o in context.scene.objects if o.type == 'MESH']
    for obj in mesh_objs:
        try:
            has_hidden_faces = any(p.hide for p in obj.data.polygons)
            if not has_hidden_faces:
                continue
            before_count = len(obj.data.polygons)
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            context.tool_settings.mesh_select_mode = (False, False, True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.reveal(select=True)
            bpy.ops.mesh.delete(type='FACE')
            bpy.ops.object.mode_set(mode='OBJECT')
            after_count = len(obj.data.polygons)
            removed_faces += max(0, before_count - after_count)
            if after_count == 0:
                bpy.data.objects.remove(obj, do_unlink=True)
                removed_objs += 1
        except Exception:
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
            except Exception:
                pass
    return removed_objs, removed_faces


class WT3D_OT_DeleteHiddenParts(bpy.types.Operator):
    """Xoa vinh vien cac chi tiet / part dang an (phim H hoac an trong Edit Mode) khoi file"""
    bl_idname = "wt3d.delete_hidden_parts"
    bl_label = "✂️ Xóa Vĩnh Viễn Part Đang Ẩn"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        removed_objs, removed_faces = _wt3d_purge_hidden_objects_and_faces(context)

        visible_meshes = [o for o in context.scene.objects if o.type == 'MESH' and not o.hide_get() and not o.hide_viewport]
        if not visible_meshes:
            self.report({'ERROR'}, "Không còn đối tượng Mesh nào hiển thị trong Scene! Đã hủy ghi đè để bảo vệ file .blend/.fbx.")
            return {'CANCELLED'}
        if removed_objs == 0 and removed_faces == 0:
            self.report({'INFO'}, "Không có Part hoặc Mặt nào đang ẩn cần xóa!")
        else:
            self.report({'INFO'}, f"Đã xóa sạch {removed_objs} đối tượng ẩn và {removed_faces} mặt (Part) đang ẩn!")
        return {'FINISHED'}


class WT3D_OT_ExportCleanFBXAndGLB(bpy.types.Operator):
    """Xuat lai file .FBX va .GLB sach (Tu dong loai bo 100% cac Part va Mat dang an)"""
    bl_idname = "wt3d.export_clean_fbx_glb"
    bl_label = "📦 Xuất FBX & GLB (Bỏ Part Đang Ẩn)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        blend_path = bpy.data.filepath
        if not blend_path:
            self.report({'ERROR'}, "Vui lòng mở hoặc lưu file .blend trước khi xuất FBX & GLB!")
            return {'CANCELLED'}

        export_dir = os.path.dirname(blend_path)
        base_name = os.path.splitext(os.path.basename(blend_path))[0]
        fbx_path = os.path.join(export_dir, f"{base_name}.fbx")
        glb_path = os.path.join(export_dir, f"{base_name}.glb")

        removed_objs, removed_faces = _wt3d_purge_hidden_objects_and_faces(context)

        visible_meshes = [o for o in context.scene.objects if o.type == 'MESH' and not o.hide_get() and not o.hide_viewport]
        if not visible_meshes:
            self.report({'ERROR'}, "Không còn đối tượng Mesh nào hiển thị trong Scene! Đã hủy ghi đè để bảo vệ file .blend/.fbx.")
            return {'CANCELLED'}

        try:
            bpy.ops.export_scene.fbx(
                filepath=fbx_path,
                use_selection=False,
                use_visible=True,
                object_types={'MESH'},
                axis_forward='-Z',
                axis_up='Y',
                global_scale=1.0,
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_NONE',
                use_space_transform=True,
                bake_space_transform=True,
                mesh_smooth_type='FACE',
                use_mesh_modifiers=True,
                path_mode='COPY',
                embed_textures=True
            )
        except Exception as e:
            self.report({'ERROR'}, f"Lỗi xuất FBX: {e}")
            return {'CANCELLED'}

        try:
            bpy.ops.export_scene.gltf(
                filepath=glb_path,
                export_format='GLB',
                use_visible=True,
                export_yup=True,
                export_apply=True,
                export_materials='EXPORT'
            )
        except Exception:
            pass

        try:
            bpy.ops.wm.save_as_mainfile(filepath=blend_path, compress=True)
            if os.path.exists(blend_path + "1"):
                os.remove(blend_path + "1")
        except Exception:
            pass

        self.report({'INFO'}, f"Đã xuất FBX & GLB sạch (bỏ {removed_objs} obj ẩn, {removed_faces} mặt ẩn) -> {base_name}.fbx")
        return {'FINISHED'}

class WT3D_OT_SmoothCadNormals(bpy.types.Operator):
    """Lam min cac mat cong da giac CAD (ong nuoc, bon loc, co cut) giu nguyen goc vuong 30°"""
    bl_idname = "wt3d.smooth_cad_normals"
    bl_label = "Làm Mịn Mặt Cong CAD"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        targets = selected_meshes if selected_meshes else [obj for obj in context.scene.objects if obj.type == 'MESH']

        if not targets:
            self.report({'WARNING'}, "Không tìm thấy chi tiết dạng Mesh nào để làm mịn!")
            return {'CANCELLED'}

        orig_active = context.view_layer.objects.active
        orig_selected = [obj for obj in context.selected_objects]

        success_count = 0
        for obj in targets:
            context.view_layer.objects.active = obj
            obj.select_set(True)
            try:
                bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30))
                success_count += 1
            except Exception:
                try:
                    for poly in obj.data.polygons:
                        poly.use_smooth = True
                    success_count += 1
                except:
                    pass

        # Restore previous selection
        for obj in context.scene.objects:
            obj.select_set(obj in orig_selected)
        if orig_active and orig_active.name in context.scene.objects:
            context.view_layer.objects.active = orig_active

        self.report({'INFO'}, f"Đã làm mịn mặt cong và khử răng cưa cho {success_count} chi tiết CAD!")
        return {'FINISHED'}

class WT3D_OT_ToggleViewportRender(bpy.types.Operator):
    """Bat / Tat che do xem Dò Tia Thoi Gian Thuc (Viewport Shading Rendered)"""
    bl_idname = "wt3d.toggle_rendered_view"
    bl_label = "👁️ Bật Dò Tia Thời Gian Thực"

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.shading.type == 'RENDERED':
                            space.shading.type = 'SOLID'
                        else:
                            space.shading.type = 'RENDERED'
        return {'FINISHED'}

class WT3D_OT_BatchRenderAll(bpy.types.Operator):
    """Tu dong chup & luu ca 7 goc B2 vao thu muc xuat anh"""
    bl_idname = "wt3d.batch_render_all"
    bl_label = "🚀 BATCH RENDER CẢ 7 GÓC B2"

    def execute(self, context):
        bounds = get_model_bounds(context)
        if not bounds:
            self.report({'WARNING'}, "Khong tim thay mo hinh 3D nao trong Scene de Batch Render!")
            return {'CANCELLED'}

        props = context.scene.wt3d_props
        scene = context.scene

        res_map = {"4K": (3840, 2160), "2K": (2560, 1440), "1080P": (1920, 1080)}
        w, h = res_map.get(props.resolution_preset, (3840, 2160))
        scene.render.resolution_x = w
        scene.render.resolution_y = h
        scene.cycles.samples = props.render_samples
        scene.render.film_transparent = props.transparent_bg

        out_dir = get_safe_output_dir(props.output_dir)
        os.makedirs(out_dir, exist_ok=True)

        base_name = get_smart_model_name(context)

        shots = [
            ("00_LOW_ANGLE", f"{base_name}_00_LowAngle_Hero.png"),
            ("01_OVERALL_HERO", f"{base_name}_01_Overall_Hero.png"),
            ("02_PIPING_ROUTING", f"{base_name}_02_Piping_Routing.png"),
            ("03_TOP_PLAN", f"{base_name}_03_Top_Plan_Layout.png"),
            ("04_FRONT_ELEVATION", f"{base_name}_05_Front_Elevation.png"),
            ("05_RIGHT_PROFILE", f"{base_name}_06_Right_Profile.png"),
            ("06_DETAIL_CLOSEUP", f"{base_name}_08_Detail_CloseUp_1.png"),
        ]

        t0 = time.time()
        for shot_id, filename in shots:
            apply_shot_transform(context, shot_id)
            filepath = os.path.join(out_dir, filename)
            scene.render.filepath = filepath
            bpy.ops.render.render(write_still=True)

        total_time = time.time() - t0
        self.report({'INFO'}, f"Da render thanh cong 7 goc B2 trong {total_time:.1f}s vao: {out_dir}")
        
        try:
            os.startfile(out_dir)
        except:
            pass

        return {'FINISHED'}

class WT3D_OT_BackgroundBatchRender(bpy.types.Operator):
    """Render ca 7 goc B2 chay ngam (Detached Process) - Blender GUI van nhe tanh 100%, khong treo hay do may!"""
    bl_idname = "wt3d.background_batch_render"
    bl_label = "⚡ RENDER NGẦM 7 GÓC (CHỐNG TREO MÁY)"
    bl_description = "Render ngam trong tien trinh doc lap o che do uu tien thap, giao dien Blender van xoay muot ma khong he bi treo"

    def execute(self, context):
        bounds = get_model_bounds(context)
        if not bounds:
            self.report({'WARNING'}, "Khong tim thay mo hinh 3D nao trong Scene de Render!")
            return {'CANCELLED'}

        props = context.scene.wt3d_props
        out_dir = get_safe_output_dir(props.output_dir)
        os.makedirs(out_dir, exist_ok=True)

        temp_dir = tempfile.gettempdir()
        temp_blend = os.path.join(temp_dir, f"wt3d_bg_batch_{int(time.time())}.blend")
        try:
            bpy.ops.wm.save_as_mainfile(filepath=temp_blend, copy=True)
        except Exception as e:
            self.report({'ERROR'}, f"Khong the tao file snapshot tam: {e}")
            return {'CANCELLED'}

        blender_exe = bpy.app.binary_path
        py_cmd = "import bpy; bpy.ops.wt3d.batch_render_all()"

        cmd = [
            blender_exe,
            "-b", temp_blend,
            "--python-expr", py_cmd
        ]

        DETACHED_PROCESS = 0x00000008
        BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
        flags = DETACHED_PROCESS | BELOW_NORMAL_PRIORITY_CLASS

        try:
            subprocess.Popen(
                cmd,
                creationflags=flags,
                close_fds=True
            )
            self.report({'INFO'}, f"Da khoi dong Render Ngam 7 goc B2 (Chong treo)! Anh xuat tai: {out_dir}")
        except Exception as e:
            self.report({'ERROR'}, f"Loi khoi dong render ngam: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

class WT3D_OT_CreateVideoAnimation(bpy.types.Operator):
    """Tu dong tao quy dao quay phim Camera 360 do hoac FPV Drone va chay thu tren Viewport"""
    bl_idname = "wt3d.create_video_animation"
    bl_label = "▶️ Xem Thử Quỹ Đạo Video"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.wt3d_props
        scene = context.scene
        bounds = get_model_bounds(context)
        if not bounds:
            self.report({'WARNING'}, "Khong tim thay mo hinh 3D de tao quy dao quay phim!")
            return {'CANCELLED'}

        center = bounds["center"]
        radius = bounds["radius"]
        ground_z = bounds["ground_z"]
        lz = bounds["size"].z

        if props.video_aspect == '9_16':
            scene.render.resolution_x = 1080
            scene.render.resolution_y = 1920
        else:
            scene.render.resolution_x = 1920
            scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100
        scene.render.fps = 30

        aspect = scene.render.resolution_x / scene.render.resolution_y
        sensor_width = 36.0
        sensor_height = sensor_width / aspect

        duration_sec = int(props.video_duration)
        total_frames = duration_sec * 30
        scene.frame_start = 1
        scene.frame_end = total_frames

        emp = bpy.data.objects.get("WT3D_Turntable_Center")
        if not emp:
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=center)
            emp = context.active_object
            emp.name = "WT3D_Turntable_Center"
        else:
            emp.location = center

        emp.animation_data_clear()

        cam = get_or_create_camera(scene)
        cam.animation_data_clear()
        cam_data = cam.data
        cam_data.type = 'PERSP'
        cam_data.lens = 50.0

        limiting_dim = min(sensor_width, sensor_height)
        tan_half = (limiting_dim / 2.0) / cam_data.lens
        dist = (radius / tan_half) * 1.30

        if props.video_style == 'TURNTABLE':
            cam.parent = emp
            cam.matrix_parent_inverse.identity()
            cam.location = mathutils.Vector((dist * 0.70, -dist * 0.70, radius * 0.75))
            aim_camera(cam, cam.location, (0, 0, 0))

            emp.rotation_euler = (0, 0, 0)
            emp.keyframe_insert(data_path="rotation_euler", frame=1)
            emp.rotation_euler = (0, 0, math.radians(360))
            emp.keyframe_insert(data_path="rotation_euler", frame=total_frames + 1)

            if emp.animation_data and emp.animation_data.action:
                for fc in emp.animation_data.action.fcurves:
                    for kf in fc.keyframe_points:
                        kf.interpolation = 'LINEAR'

        elif props.video_style == 'DRONE':
            cam.parent = None
            cam.matrix_parent_inverse.identity()
            emp.rotation_euler = (0, 0, 0)

            eye_f1 = center + mathutils.Vector((radius * 2.2, -radius * 2.2, radius * 1.8))
            aim_camera(cam, eye_f1, center)
            cam.keyframe_insert(data_path="location", frame=1)
            cam.keyframe_insert(data_path="rotation_euler", frame=1)

            f_mid = int(total_frames * 0.45)
            eye_mid = center + mathutils.Vector((-radius * 0.9, -radius * 1.0, ground_z + lz * 0.6))
            target_mid = mathutils.Vector((center.x, center.y, ground_z + lz * 0.7))
            aim_camera(cam, eye_mid, target_mid)
            cam.keyframe_insert(data_path="location", frame=f_mid)
            cam.keyframe_insert(data_path="rotation_euler", frame=f_mid)

            eye_end = center + mathutils.Vector((radius * 1.6, -radius * 1.6, radius * 1.0))
            aim_camera(cam, eye_end, center)
            cam.keyframe_insert(data_path="location", frame=total_frames)
            cam.keyframe_insert(data_path="rotation_euler", frame=total_frames)

            if cam.animation_data and cam.animation_data.action:
                for fc in cam.animation_data.action.fcurves:
                    for kf in fc.keyframe_points:
                        kf.interpolation = 'BEZIER'

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.region_3d.view_perspective = 'CAMERA'

        scene.frame_current = 1
        bpy.ops.screen.animation_play()

        self.report({'INFO'}, f"Da tao quy dao {props.video_style} ({duration_sec}s)! Dang chay xem thu...")
        return {'FINISHED'}

class WT3D_OT_RenderVideoMP4(bpy.types.Operator):
    """Render toan bo quy dao chuyen dong truc tiep thanh file MP4 H.264 (1-Click)"""
    bl_idname = "wt3d.render_video_mp4"
    bl_label = "🎬 1-CLICK XUẤT VIDEO MP4"

    def execute(self, context):
        bounds = get_model_bounds(context)
        if not bounds:
            self.report({'WARNING'}, "Khong tim thay mo hinh 3D de xuat Video MP4!")
            return {'CANCELLED'}

        props = context.scene.wt3d_props
        scene = context.scene

        res = bpy.ops.wt3d.create_video_animation()
        if 'CANCELLED' in res:
            self.report({'WARNING'}, "Khong the tao quy dao video!")
            return {'CANCELLED'}

        try:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        except:
            pass

        if props.video_engine == 'BLENDER_EEVEE_NEXT':
            try:
                scene.render.engine = 'BLENDER_EEVEE_NEXT'
            except:
                try:
                    scene.render.engine = 'BLENDER_EEVEE'
                except:
                    scene.render.engine = 'CYCLES'
        else:
            scene.render.engine = 'CYCLES'
            scene.cycles.device = 'GPU'
            scene.cycles.samples = 16
            scene.cycles.use_denoising = True

        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'HIGH'
        scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

        out_dir = get_safe_output_dir(props.output_dir)
        os.makedirs(out_dir, exist_ok=True)
        base_name = get_smart_model_name(context)

        tag = "Shorts_9x16" if props.video_aspect == '9_16' else "Catalog_16x9"
        mp4_path = os.path.join(out_dir, f"{base_name}_{props.video_style}_{tag}.mp4")
        scene.render.filepath = mp4_path

        t0 = time.time()
        bpy.ops.render.render(animation=True)
        elapsed = time.time() - t0

        self.report({'INFO'}, f"Da xuat xong Video MP4 trong {elapsed:.1f}s: {mp4_path}")

        try:
            os.startfile(mp4_path)
        except:
            pass

        return {'FINISHED'}

class WT3D_OT_BackgroundVideoRender(bpy.types.Operator):
    """Xuat Video MP4 chay ngam (Detached Process) - Blender GUI van nhe tanh 100%, khong treo hay do may!"""
    bl_idname = "wt3d.background_video_render"
    bl_label = "⚡ XUẤT VIDEO NGẦM (CHỐNG TREO MÁY)"
    bl_description = "Xuat video MP4 trong tien trinh doc lap o che do uu tien thap, Blender van su dung binh thuong khong bi do"

    def execute(self, context):
        bounds = get_model_bounds(context)
        if not bounds:
            self.report({'WARNING'}, "Khong tim thay mo hinh 3D nao de xuat Video MP4!")
            return {'CANCELLED'}

        res = bpy.ops.wt3d.create_video_animation()
        if 'CANCELLED' in res:
            self.report({'WARNING'}, "Khong the tao quy dao video!")
            return {'CANCELLED'}

        try:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        except:
            pass

        props = context.scene.wt3d_props
        out_dir = get_safe_output_dir(props.output_dir)
        os.makedirs(out_dir, exist_ok=True)

        temp_dir = tempfile.gettempdir()
        temp_blend = os.path.join(temp_dir, f"wt3d_bg_video_{int(time.time())}.blend")
        try:
            bpy.ops.wm.save_as_mainfile(filepath=temp_blend, copy=True)
        except Exception as e:
            self.report({'ERROR'}, f"Khong the tao file snapshot tam: {e}")
            return {'CANCELLED'}

        blender_exe = bpy.app.binary_path
        py_cmd = "import bpy; bpy.ops.wt3d.render_video_mp4()"

        cmd = [
            blender_exe,
            "-b", temp_blend,
            "--python-expr", py_cmd
        ]

        DETACHED_PROCESS = 0x00000008
        BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
        flags = DETACHED_PROCESS | BELOW_NORMAL_PRIORITY_CLASS

        try:
            subprocess.Popen(
                cmd,
                creationflags=flags,
                close_fds=True
            )
            self.report({'INFO'}, f"Da khoi dong Xuat Video MP4 Ngam (Chong treo)! Video xuat tai: {out_dir}")
        except Exception as e:
            self.report({'ERROR'}, f"Loi khoi dong render video ngam: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

class WT3D_OT_OpenOutputFolder(bpy.types.Operator):
    """Mo thu muc chua anh render va video tren Windows Explorer"""
    bl_idname = "wt3d.open_folder"
    bl_label = "📂 Mở Thư Mục Xuất File"

    def execute(self, context):
        props = context.scene.wt3d_props
        out_dir = get_safe_output_dir(props.output_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        try:
            os.startfile(out_dir)
        except Exception as e:
            self.report({'ERROR'}, f"Khong mo duoc thu muc: {e}")
        return {'FINISHED'}


# ----------------------------------------------------------------------------
# 4. GIAO DIEN DO HOA (UI SIDEBAR PANEL - PHIM N)
# ----------------------------------------------------------------------------
def reload_wt3d_panel():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass
    try:
        del bpy.types.Scene.wt3d_props
    except:
        pass
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"[WT3D] Error registering {cls}: {e}")
    bpy.types.Scene.wt3d_props = bpy.props.PointerProperty(type=WT3D_Studio_Properties)
    print("[WT3D] Giao dien Apple Bento da duoc reload thanh cong!")

class WT3D_PT_MasterPanel(bpy.types.Panel):
    bl_label = "WT3D Studio Pro"
    bl_idname = "WT3D_PT_master_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'WT3D Studio'

    def draw(self, context):
        layout = self.layout
        props = context.scene.wt3d_props

        # --------------------------------------------------------------------
        # TOP NAVIGATION: APPLE BENTO SEGMENTED TABS
        # --------------------------------------------------------------------
        row_tabs = layout.row(align=True)
        row_tabs.scale_y = 1.35
        row_tabs.prop(props, "active_tab", expand=True)

        layout.separator(factor=0.5)

        # ====================================================================
        # TAB 1: 🎨 PHỐI MÀU & 11 VẬT LIỆU WT3D (DEFAULT)
        # ====================================================================
        if props.active_tab == "MATERIALS":
            cur_mode = props.color_mode if props.color_mode in WT3D_THEMES else "DESIGN"
            theme_cfg = WT3D_THEMES[cur_mode]
            mats = theme_cfg["materials"]

            # Card 1: 3 Che Do Mau
            box_mode = layout.box()
            box_mode.label(text="🎨 Chế Độ Hiển Thị & Bảng Màu Skid", icon='COLOR')

            # Chuyen doi che do Viewport: Solid CAD, PBR Material Preview, Render Cycles
            row_vmode = box_mode.row(align=True)
            row_vmode.scale_y = 1.15
            row_vmode.operator("wt3d.set_viewport_mode", text="🎨 Màu CAD", icon='SHADING_SOLID').mode = 'SOLID'
            row_vmode.operator("wt3d.set_viewport_mode", text="💎 Xem PBR", icon='MATERIAL').mode = 'MATERIAL'
            row_vmode.operator("wt3d.set_viewport_mode", text="📸 Render", icon='SHADING_RENDERED').mode = 'RENDERED'
            
            row_modes = box_mode.row(align=True)
            row_modes.scale_y = 1.3
            
            row_modes.operator("wt3d.apply_color_mode", text="🏭 REAL", icon='CHECKBOX_HLT' if cur_mode == "REAL" else 'MODIFIER').mode = "REAL"
            row_modes.operator("wt3d.apply_color_mode", text="⭐ DESIGN", icon='CHECKBOX_HLT' if cur_mode == "DESIGN" else 'SOLO_ON').mode = "DESIGN"
            row_modes.operator("wt3d.apply_color_mode", text="🔄 PROCESS", icon='CHECKBOX_HLT' if cur_mode == "PROCESS" else 'FORCE_VORTEX').mode = "PROCESS"
            row_modes.operator("wt3d.apply_color_mode", text="↶ MẶC ĐỊNH", icon='CHECKBOX_HLT' if cur_mode == "DEFAULT" else 'LOOP_BACK').mode = "DEFAULT"

            box_mode.label(text=f"📌 {theme_cfg['label']}: {theme_cfg['badge']}", icon='INFO')

            col_auto = box_mode.column(align=True)
            col_auto.scale_y = 1.25
            col_auto.operator("wt3d.auto_assign_wt3d_hierarchy", text=f"⚡ 1-Chạm: Tự Động Phân Bổ 11 Vật Liệu Cho Skid", icon='AUTO')

            row_fix = box_mode.row(align=True)
            row_fix.operator("wt3d.fix_all_gray_materials", text="🛠️ Khử Màu Xám (Đồng Bộ)", icon='COLOR')
            row_fix.operator("wt3d.reset_all_materials_cad", text="↶ Trả Lại Gốc", icon='LOOP_BACK')
            row_fix.operator("wt3d.revert_file_from_disk", text="🔄 Nạp Lại File", icon='FILE_REFRESH')

            # 11 VAT LIEU CHUAN HIERARCHY
            # Nhom 1: Sieu bong
            box_g1 = layout.box()
            box_g1.label(text="🌟 1. Bề Mặt Siêu Bóng (Gloss > 70%)", icon='SHADING_RENDERED')
            col_g1 = box_g1.column(align=True)
            col_g1.operator("wt3d.assign_guide_mat", text=mats["HMI"][8], icon='RESTRICT_VIEW_OFF').mat_key = "HMI"
            col_g1.operator("wt3d.assign_guide_mat", text=mats["INOX"][8], icon='SHADING_RENDERED').mat_key = "INOX"
            col_g1.operator("wt3d.assign_guide_mat", text=mats["VALVE"][8], icon='COLOR_RED').mat_key = "VALVE"
            col_g1.operator("wt3d.assign_guide_mat", text=mats["BRASS"][8], icon='COLORSET_04_VEC').mat_key = "BRASS"

            # Nhom 2: Loc & Ong
            box_g2 = layout.box()
            box_g2.label(text="💧 2. Thiết Bị Lọc & Đường Ống (Gloss 60-70%)", icon='MESH_CYLINDER')
            col_g2 = box_g2.column(align=True)
            col_g2.operator("wt3d.assign_guide_mat", text=mats["PIPE_MAIN"][8], icon='COLOR_BLUE').mat_key = "PIPE_MAIN"
            col_g2.operator("wt3d.assign_guide_mat", text=mats["RO_HOUSING"][8], icon='MESH_CYLINDER').mat_key = "RO_HOUSING"
            col_g2.operator("wt3d.assign_guide_mat", text=mats["PIPE_CLEAN"][8], icon='COLOR_GREEN').mat_key = "PIPE_CLEAN"

            # Nhom 3: Ket cau & Co dien
            box_g3 = layout.box()
            box_g3.label(text="⚙️ 3. Kết Cấu, Cơ Điện & Phụ Trợ (Gloss 30-55%)", icon='PREFERENCES')
            col_g3 = box_g3.column(align=True)
            col_g3.operator("wt3d.assign_guide_mat", text=mats["CABINET"][8], icon='WINDOW').mat_key = "CABINET"
            col_g3.operator("wt3d.assign_guide_mat", text=mats["FRAME"][8], icon='MESH_CUBE').mat_key = "FRAME"
            col_g3.operator("wt3d.assign_guide_mat", text=mats["MOTOR"][8], icon='FORCE_VORTEX').mat_key = "MOTOR"
            col_g3.operator("wt3d.assign_guide_mat", text=mats["SENSOR"][8], icon='TRACKER').mat_key = "SENSOR"
            col_g3.operator("wt3d.assign_guide_mat", text=mats["CABLE"][8], icon='STRANDS').mat_key = "CABLE"

            # 17 Vat lieu mo rong
            box_ext = layout.box()
            box_ext.label(text="💎 17 Vật Liệu Mở Rộng KeyShot", icon='MATERIAL')
            box_ext.prop(props, "mat_category", expand=True)

            if props.mat_category == "METALS":
                col_m = box_ext.column(align=True)
                col_m.operator("wt3d.assign_keyshot_mat", text="Inox 304 Xước Hairline", icon='NODE_TEXTURE').mat_id = "INOX_BRUSHED"
                col_m.operator("wt3d.assign_keyshot_mat", text="Inox 316 Bóng Gương Chrome", icon='SHADING_RENDERED').mat_id = "INOX_MIRROR"
                col_m.operator("wt3d.assign_keyshot_mat", text="Thép Mạ Kẽm (Khung, Bulong)", icon='MODIFIER').mat_id = "STEEL_GALVANIZED"
                col_m.operator("wt3d.assign_keyshot_mat", text="Đồng Thau Khớp Nối Ren", icon='COLORSET_04_VEC').mat_id = "BRASS_MACHINED"
                col_m.operator("wt3d.assign_keyshot_mat", text="Gang Đúc Sơn Đen Sần", icon='RESTRICT_RENDER_OFF').mat_id = "CAST_IRON_BLACK"
                col_m.operator("wt3d.assign_keyshot_mat", text="Nhôm Anod Bạc Mờ", icon='SHADING_SOLID').mat_id = "ALU_ANODIZED"
            elif props.mat_category == "POLYMERS":
                col_p = box_ext.column(align=True)
                col_p.operator("wt3d.assign_keyshot_mat", text="FRP Xanh Đậm Pentair", icon='MATSPHERE').mat_id = "FRP_DEEP_BLUE"
                col_p.operator("wt3d.assign_keyshot_mat", text="FRP Trắng Ngà Bồn Lọc", icon='MATSPHERE').mat_id = "FRP_NATURAL_CREAM"
                col_p.operator("wt3d.assign_keyshot_mat", text="Nhựa u-PVC Xám Đậm", icon='COLORSET_07_VEC').mat_id = "UPVC_DARK_GREY"
                col_p.operator("wt3d.assign_keyshot_mat", text="Nhựa PPR Xanh Hàn Nhiệt", icon='COLORSET_03_VEC').mat_id = "PPR_GREEN"
                col_p.operator("wt3d.assign_keyshot_mat", text="Sơn Tĩnh Điện Cam An Toàn", icon='COLORSET_02_VEC').mat_id = "POWDER_ORANGE"
                col_p.operator("wt3d.assign_keyshot_mat", text="Sơn Tĩnh Điện Xanh Lá WT3D", icon='COLORSET_03_VEC').mat_id = "POWDER_GREEN"
            elif props.mat_category == "OPTICAL":
                col_o = box_ext.column(align=True)
                col_o.operator("wt3d.assign_keyshot_mat", text="Mica Acrylic Trong Suốt", icon='MOD_FLUID').mat_id = "CLEAR_ACRYLIC"
                col_o.operator("wt3d.assign_keyshot_mat", text="Kính Cường Lực / Ống UV", icon='SHADING_RENDERED').mat_id = "OPTICAL_GLASS"
                col_o.operator("wt3d.assign_keyshot_mat", text="Dầu Glycerin Đồng Hồ Áp", icon='MOD_FLUID').mat_id = "GLYCERIN_LIQUID"
            elif props.mat_category == "ELASTOMERS":
                col_e = box_ext.column(align=True)
                col_e.operator("wt3d.assign_keyshot_mat", text="Cao Su EPDM Đen Nhám", icon='RESTRICT_RENDER_OFF').mat_id = "EPDM_RUBBER"
                col_e.operator("wt3d.assign_keyshot_mat", text="Silicone Trắng Đục Làm Kín", icon='SHADING_SOLID').mat_id = "SILICONE_WHITE"

        # ====================================================================
        # TAB 2: 🌍 STUDIO & ÁNH SÁNG KEYSHOT PRO
        # ====================================================================
        elif props.active_tab == "STUDIO":
            col_setup = layout.column(align=True)
            col_setup.scale_y = 1.2
            col_setup.operator("wt3d.setup_studio_rig", text="⚡ Khởi Tạo Studio Cho Dự Án Mới", icon='PREFERENCES')

            row_view = layout.row(align=True)
            row_view.operator("wt3d.toggle_rendered_view", text="Bật Render Thật", icon='SHADING_RENDERED')
            row_view.operator("wt3d.auto_frame", text="Căn Toàn Cảnh", icon='VIEW_ZOOM')

            box_env = layout.box()
            box_env.label(text="🌍 4 Môi Trường Phông Nền", icon='WORLD')
            grid_env = box_env.grid_flow(columns=2, align=True)
            grid_env.operator("wt3d.set_keyshot_env", text="Trắng Pure White", icon='IMAGE_BACKGROUND').env_type = "PURE_WHITE"
            grid_env.operator("wt3d.set_keyshot_env", text="Xám Industrial", icon='SHADING_SOLID').env_type = "INDUSTRIAL_GREY"
            grid_env.operator("wt3d.set_keyshot_env", text="Đen Tech Noir", icon='RESTRICT_RENDER_OFF').env_type = "DARK_TECH_NOIR"
            grid_env.operator("wt3d.set_keyshot_env", text="Xanh Inventor", icon='LIGHT').env_type = "INVENTOR_CLASSIC"

            box_light = layout.box()
            box_light.label(text="💡 4 Dàn Đèn Studio KeyShot", icon='LIGHT_SUN')
            grid_rig = box_light.grid_flow(columns=2, align=True)
            grid_rig.operator("wt3d.set_keyshot_lighting", text="3-Điểm Studio", icon='LIGHT_AREA').rig_type = "3POINT_STUDIO"
            grid_rig.operator("wt3d.set_keyshot_lighting", text="Đỉnh Showroom", icon='LIGHT_SUN').rig_type = "OVERHEAD_DIFFUSER"
            grid_rig.operator("wt3d.set_keyshot_lighting", text="Dual Rim Viền", icon='LIGHT_POINT').rig_type = "DUAL_RIM_DRAMATIC"
            grid_rig.operator("wt3d.set_keyshot_lighting", text="Tản Đều 360°", icon='LIGHT_SPOT').rig_type = "EVEN_SOFT_BOOTH"

            key_l = bpy.data.objects.get("WT3D_KeyLight")
            fill_l = bpy.data.objects.get("WT3D_FillLight")
            rim_l = bpy.data.objects.get("WT3D_RimLight")

            if key_l and key_l.data:
                box_light.prop(key_l.data, "energy", text="Đèn Chính (Key)")
            if fill_l and fill_l.data:
                box_light.prop(fill_l.data, "energy", text="Đèn Phụ (Fill)")
            if rim_l and rim_l.data:
                box_light.prop(rim_l.data, "energy", text="Đèn Viền (Rim)")

            box_light.prop(props, "transparent_bg", text="Nền Trong Suốt (Alpha)", icon='IMAGE_ALPHA')

        # ====================================================================
        # TAB 3: 🎥 7 GÓC CHỤP & XUẤT BẢN RENDER
        # ====================================================================
        elif props.active_tab == "CAMERAS":
            box_cam = layout.box()
            box_cam.label(text="🎥 7 Góc Chụp Chuẩn B2 (Inventor)", icon='CAMERA_DATA')
            col_cam = box_cam.column(align=True)
            col_cam.operator("wt3d.switch_shot", text="00. Góc Thấp Hero (Ngước Lên)", icon='TRIA_UP').shot_id = "00_LOW_ANGLE"
            col_cam.operator("wt3d.switch_shot", text="01. Phối Cảnh 3/4 Vàng (Overall)", icon='VIEW_PERSPECTIVE').shot_id = "01_OVERALL_HERO"
            col_cam.operator("wt3d.switch_shot", text="02. Soi Tuyến Đường Ống (Routing)", icon='ORIENTATION_GIMBAL').shot_id = "02_PIPING_ROUTING"
            col_cam.operator("wt3d.switch_shot", text="03. Hình Chiếu Bằng (Top 90°)", icon='AXIS_TOP').shot_id = "03_TOP_PLAN"
            col_cam.operator("wt3d.switch_shot", text="04. Hình Chiếu Đứng (Front View)", icon='AXIS_FRONT').shot_id = "04_FRONT_ELEVATION"
            col_cam.operator("wt3d.switch_shot", text="05. Hình Chiếu Cạnh (Right View)", icon='AXIS_SIDE').shot_id = "05_RIGHT_PROFILE"
            col_cam.operator("wt3d.switch_shot", text="06. Cận Cảnh Cụm Van & Ren (Macro)", icon='ZOOM_SELECTED').shot_id = "06_DETAIL_CLOSEUP"

            box_render = layout.box()
            box_render.label(text="🚀 Xuất Bản Render & Video", icon='OUTPUT')
            box_render.prop(props, "render_resolution")
            box_render.prop(props, "render_samples")

            col_btn = box_render.column(align=True)
            col_btn.scale_y = 1.2
            col_btn.operator("wt3d.background_batch_render", text="⚡ Render Ngầm 7 Góc (Không Treo Máy)", icon='RENDER_STILL')
            col_btn.operator("wt3d.batch_render_all", text="📸 Render Trực Tiếp 7 Góc", icon='CAMERA_DATA')

            layout.separator(factor=0.3)
            box_vid = layout.box()
            box_vid.label(text="🎬 Video Showreel TikTok & Web", icon='SEQUENCE')
            box_vid.prop(props, "video_duration")
            box_vid.prop(props, "video_style")
            box_vid.prop(props, "video_engine")
            
            col_vbtn = box_vid.column(align=True)
            col_vbtn.scale_y = 1.2
            col_vbtn.operator("wt3d.background_video_render", text="⚡ Xuất Video Ngầm (Zero-Lag)", icon='FILE_MOVIE')
            col_vbtn.operator("wt3d.render_video_mp4", text="🎬 Xuất Video MP4 Trực Tiếp", icon='PLAY')

            layout.separator(factor=0.3)
            layout.operator("wt3d.open_folder", text="📂 Mở Thư Mục Xuất File", icon='FILE_FOLDER')

        # ====================================================================
        # TAB 4: ⚡ CAD & TỐI ƯU HÓA (CHỐNG TREO MÁY & KHỬ SỌC)
        # ====================================================================
        elif props.active_tab == "OPTIMIZE":
            box_inv = layout.box()
            box_inv.label(text="⚡ Môi Trường Inventor & Hiển Thị CAD", icon='WINDOW')
            
            col_cad = box_inv.column(align=True)
            col_cad.scale_y = 1.25
            col_cad.operator("wt3d.apply_inventor_theme", text="⚡ 1-Click: Môi Trường Chuẩn Inventor", icon='LIGHT')
            col_cad.operator("wt3d.export_clean_fbx_glb", text="📦 Xuất FBX & GLB (Bỏ Part Đang Ẩn)", icon='EXPORT')
            col_cad.operator("wt3d.delete_hidden_parts", text="✂️ Xóa Vĩnh Viễn Part Đang Ẩn", icon='TRASH')

            box_fix = layout.box()
            box_fix.label(text="🛠️ Tinh Chỉnh & Khử Lỗi Viewport", icon='BRUSH_DATA')
            col_fix = box_fix.column(align=True)
            col_fix.scale_y = 1.2
            col_fix.operator("wt3d.fix_viewport_ripples", text="🛠️ Khử Sọc Gợn Sóng / Moire Khi Zoom", icon='BRUSH_DATA')

            row_edge = col_fix.row(align=True)
            row_edge.operator("wt3d.toggle_shaded_edges", text="📐 Nét Viền CAD", icon='MOD_OUTLINE')
            row_edge.operator("wt3d.toggle_grid", text="井 Lưới Sàn", icon='GRID')

            row_aa = col_fix.row(align=True)
            row_aa.operator("wt3d.set_high_anti_aliasing", text="✨ Khử Răng Cưa (16x)", icon='ANTIALIASED')
            row_aa.operator("wt3d.smooth_cad_normals", text="🌀 Mịn Mặt Cong (30°)", icon='MOD_SMOOTH')

            box_guard = layout.box()
            box_guard.label(text="🛡️ Bảo Vệ Phần Cứng & Bộ Nhớ", icon='FREEZE')
            col_guard = box_guard.column(align=True)
            col_guard.scale_y = 1.15
            row_g = col_guard.row(align=True)
            row_g.operator("wt3d.anti_freeze_turbo", text="🛡️ Chống Treo Máy", icon='FREEZE')
            row_g.operator("wt3d.purge_memory", text="🧹 Dọn Rác RAM", icon='TRASH')

            col_guard.operator("wt3d.restore_blender_theme", text="↶ Về Giao Diện Blender Gốc", icon='LOOP_BACK')

            layout.separator(factor=0.5)
            col_rel = layout.column(align=True)
            col_rel.scale_y = 1.3
            col_rel.operator("wt3d.reload_code", text="🔄 Nạp Lại Panel (Hot-Reload)", icon='FILE_REFRESH')


# ----------------------------------------------------------------------------
# 5. REGISTRATION
# ----------------------------------------------------------------------------
classes = (
    WT3D_Studio_Properties,
    WT3D_OT_AntiFreezeTurbo,
    WT3D_OT_PurgeMemory,
    WT3D_OT_SetKeyShotEnvironment,
    WT3D_OT_SetKeyShotLightingRig,
    WT3D_OT_AssignWT3DGuideMaterial,
    WT3D_OT_ApplyColorMode,
    WT3D_OT_AutoAssignWT3DHierarchy,
    WT3D_OT_AssignKeyShotMaterial,
    WT3D_OT_SetViewportMode,
    WT3D_OT_FixAllGrayMaterials,
    WT3D_OT_ResetAllMaterialsToCADDefault,
    WT3D_OT_RevertFileFromDisk,
    WT3D_OT_SwitchShot,
    WT3D_OT_SetupStudioRig,
    WT3D_OT_AutoFrame,
    WT3D_OT_ApplyInventorTheme,
    WT3D_OT_ToggleShadedEdges,
    WT3D_OT_FixViewportRipples,
    WT3D_OT_ToggleGrid,
    WT3D_OT_RestoreBlenderTheme,
    WT3D_OT_ReloadStudioCode,
    WT3D_OT_SetHighAntiAliasing,
    WT3D_OT_DeleteHiddenParts,
    WT3D_OT_ExportCleanFBXAndGLB,
    WT3D_OT_SmoothCadNormals,
    WT3D_OT_ToggleViewportRender,
    WT3D_OT_BatchRenderAll,
    WT3D_OT_BackgroundBatchRender,
    WT3D_OT_CreateVideoAnimation,
    WT3D_OT_RenderVideoMP4,
    WT3D_OT_BackgroundVideoRender,
    WT3D_OT_OpenOutputFolder,
    WT3D_PT_MasterPanel,
)

_WT3D_LAST_MAT_SIG = (-1, -1)

@bpy.app.handlers.persistent
def _wt3d_auto_sync_imported_materials(scene, depsgraph=None):
    """Tu dong khoi phuc PBR & do trong suot (Clear/Transparent) ngay khi nguoi dung Import .obj / .fbx / .glb vao Blender."""
    global _WT3D_LAST_MAT_SIG
    try:
        mat_cnt = len(bpy.data.materials)
        obj_cnt = len(bpy.data.objects)
        sig = (mat_cnt, obj_cnt)
        if sig == _WT3D_LAST_MAT_SIG or mat_cnt == 0:
            return
        _WT3D_LAST_MAT_SIG = sig

        import sys
        z_tools = r"D:\WT3D_Project\Z_Tools"
        if os.path.isdir(z_tools) and z_tools not in sys.path:
            sys.path.insert(0, z_tools)
        try:
            import wt3d_pbr_and_decal_master as pbr_decal
            pbr_decal.apply_inventor_pbr_materials()
        except Exception:
            for mat in bpy.data.materials:
                if not mat or not mat.use_nodes or not mat.node_tree:
                    continue
                bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if not bsdf:
                    continue
                a = float(bsdf.inputs['Alpha'].default_value) if 'Alpha' in bsdf.inputs else 1.0
                bc = list(bsdf.inputs['Base Color'].default_value)
                if a < 0.98:
                    mat.blend_method = 'BLEND'
                    if hasattr(mat, "surface_render_method"):
                        try:
                            mat.surface_render_method = 'BLENDED'
                        except Exception:
                            pass
                    if 'Transmission Weight' in bsdf.inputs:
                        bsdf.inputs['Transmission Weight'].default_value = max(float(bsdf.inputs['Transmission Weight'].default_value), round(1.0 - a, 3))
                mat.diffuse_color = (bc[0], bc[1], bc[2], a)

        # Auto-apply '1-Click: Môi Trường Chuẩn Inventor' theme & viewport shading on load/import so user never sees silver glare!
        try:
            theme = bpy.context.preferences.themes[0]
            v3d = theme.view_3d.space
            v3d.gradients.background_type = 'LINEAR'
            v3d.gradients.high_gradient = (0.76, 0.82, 0.88)
            v3d.gradients.gradient = (0.93, 0.95, 0.97)
            theme.view_3d.grid = (0.70, 0.74, 0.78, 0.35)
        except Exception:
            pass
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.clip_start = 0.05
                            space.clip_end = 10000.0
                            try:
                                space.overlay.show_floor = False
                                space.overlay.show_axis_x = False
                                space.overlay.show_axis_y = False
                                space.overlay.show_ortho_grid = False
                                space.overlay.show_relationship_lines = False
                                space.overlay.show_extras = False
                                sh = space.shading
                                sh.type = 'SOLID'
                                sh.light = 'STUDIO'
                                sh.color_type = 'MATERIAL'
                                sh.show_cavity = True
                                sh.cavity_type = 'WORLD'
                                sh.cavity_ridge_factor = 1.0
                                sh.cavity_valley_factor = 1.0
                                sh.show_object_outline = True
                                sh.object_outline_color = (0.15, 0.15, 0.15)
                                sh.show_shadows = False
                                sh.background_type = 'THEME'
                                sh.use_scene_lights = False
                                sh.use_scene_world = False
                                sh.studiolight_intensity = 0.85
                            except Exception:
                                pass
    except Exception:
        pass

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.wt3d_props = bpy.props.PointerProperty(type=WT3D_Studio_Properties)
    if _wt3d_auto_sync_imported_materials not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(_wt3d_auto_sync_imported_materials)
    if _wt3d_auto_sync_imported_materials not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(_wt3d_auto_sync_imported_materials)
    print("[WT3D] WT3D Studio Panel v1.3.0 (KeyShot Pro Edition) da duoc khoi tao thanh cong!")

def unregister():
    if _wt3d_auto_sync_imported_materials in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_wt3d_auto_sync_imported_materials)
    if _wt3d_auto_sync_imported_materials in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_wt3d_auto_sync_imported_materials)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.wt3d_props

if __name__ == "__main__":
    register()
