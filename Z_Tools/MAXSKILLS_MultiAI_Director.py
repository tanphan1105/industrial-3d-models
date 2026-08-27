import bpy
import sys
import math
import mathutils
import os

print("\n============================================================")
print(" MAXSKILLS V5 - MULTI-AGENT CINEMATIC DIRECTOR (BLENDER) ")
print("============================================================\n")

argv = sys.argv
if "--" not in argv:
    print("FATAL: No arguments provided. Need FBX path and Output path.")
    sys.exit(1)

args = argv[argv.index("--") + 1:]
obj_path = args[0]
output_path = args[1]

# ==========================================================
# EXPERT 1: THE OPTIMIZER AI (Hệ Thống Ép Xung)
# ==========================================================
def optimizer_ai(samples=256):
    print("▶ [Optimizer AI] Đang khởi động: Dọn RAM, Ép xung GPU & AI Khử nhiễu...")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = samples
    bpy.context.scene.cycles.use_denoising = True # AI OptiX/OpenImage Denoise
    
    # Cấu trúc B2B Shorts (9:16 4K Ultra-HD)
    bpy.context.scene.render.resolution_x = 2160
    bpy.context.scene.render.resolution_y = 3840
    
    try:
        preferences = bpy.context.preferences
        cycles_preferences = preferences.addons['cycles'].preferences
        cycles_preferences.compute_device_type = 'CUDA' # Dùng Card rời
        for device in cycles_preferences.get_devices()[0]: # cuda devices
            device.use = True
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.cycles.samples = samples # Giữ nguyên 256 samples cho GPU
        print("  => Đã bẻ khóa thành công GPU Acceleration! (Hardcore Mode)")
    except:
        bpy.context.scene.cycles.device = 'CPU'
        bpy.context.scene.cycles.samples = 64 # Giảm gấp 4 lần để chống cháy nổ CPU
        # Phân mảnh luồng để chừa RAM cho HĐH
        bpy.context.scene.render.threads_mode = 'FIXED'
        bpy.context.scene.render.threads = max(1, os.cpu_count() - 2) 
        print(f"  => CPU Safe Mode Kích hoạt: Giảm tải mẫu Render xuống 64 + Chừa 2 Cores cho Windows.")

# ==========================================================
# THỰC THI LÕI: IMPORT FILE
# ==========================================================
optimizer_ai(samples=256)

print(f"▶ [System] Đang Import File FBX/OBJ: {os.path.basename(obj_path)}")
if obj_path.lower().endswith(".fbx"):
    bpy.ops.import_scene.fbx(filepath=obj_path)
else:
    bpy.ops.wm.obj_import(filepath=obj_path)

objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not objects:
    print("FATAL: Import rỗng!")
    sys.exit(1)

min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

for obj in objects:
    for v in obj.bound_box:
        vw = obj.matrix_world @ mathutils.Vector(v)
        min_x, min_y, min_z = min(min_x, vw.x), min(min_y, vw.y), min(min_z, vw.z)
        max_x, max_y, max_z = max(max_x, vw.x), max(max_y, vw.y), max(max_z, vw.z)

cx, cy, cz = (min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2
dx, dy, dz = max_x - min_x, max_y - min_y, max_z - min_z
max_dim = max(dx, dy, dz)

# Khắc phục bug Clip_End: Các máy Skid công nghiệp to hơn 100m (do sai scale export) 
# bắt buộc phải mở khẩu độ sâu lấy nét cực đại để không bị tàng hình.
print(f"  => BBOX Detected: Bán kính lớn nhất = {max_dim:.2f} đơn vị")

# ==========================================================
# EXPERT 2: THE ALCHEMIST AI (Chuyên Gia Vật Liệu PBR)
# ==========================================================
def alchemist_ai():
    print("▶ [Alchemist AI] Phân tích mã màu & Tiêm Vật lý Điện ảnh...")
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            color = bsdf.inputs["Base Color"].default_value
            r, g, b, a = color[0], color[1], color[2], color[3] if len(color)>3 else 1.0
            
            sat = max(r,g,b) - min(r,g,b) # Độ rực rỡ
            lum = 0.2126*r + 0.7152*g + 0.0722*b # Độ chói
            
            if a < 0.99 or "glass" in mat.name.lower():
                # Profile: ACRYLIC / GLASS (Kính/Cốc học trong suốt)
                bsdf.inputs["Transmission"].default_value = 1.0
                bsdf.inputs["Roughness"].default_value = 0.02
                bsdf.inputs["Metallic"].default_value = 0.0
            elif sat < 0.15 and lum > 0.25:
                # Profile: BRUSHED STAINLESS STEEL (Inox 304 xước / Khung thép)
                bsdf.inputs["Metallic"].default_value = 0.9
                bsdf.inputs["Roughness"].default_value = 0.38
                # Boot contrast cho Inox chân thực hơn
                bsdf.inputs["Base Color"].default_value = (lum*0.8, lum*0.8, lum*0.85, 1)
            elif sat < 0.15 and lum <= 0.25:
                # Profile: INDUSTRIAL RUBBER (Gioăng cao su / Cáp điện đen)
                bsdf.inputs["Metallic"].default_value = 0.0
                bsdf.inputs["Roughness"].default_value = 0.75 # Sần sùi hút sáng
            else:
                # Profile: GLOSSY PVC / POWDER COATING (Nhựa uPVC xanh/đỏ hoặc Sơn tĩnh điện)
                bsdf.inputs["Metallic"].default_value = 0.0
                bsdf.inputs["Roughness"].default_value = 0.25 # Bóng mượt
                try:
                    if "Coat Weight" in bsdf.inputs:
                        bsdf.inputs["Coat Weight"].default_value = 1.0
                        bsdf.inputs["Coat Roughness"].default_value = 0.05
                except:
                    pass

alchemist_ai()

# ==========================================================
# EXPERT 3: THE GAFFER AI (Đạo Diễn Ánh Sáng Studio)
# ==========================================================
def gaffer_ai(cx, cy, cz, max_dim, min_z):
    print("▶ [Gaffer AI] Tính vùng an toàn & Thả họng đèn Studio (3-Point Tech)...")
    # Sàn Studio Infinity Catch-Shadow
    bpy.ops.mesh.primitive_plane_add(size=max_dim*50, location=(cx, cy, min_z))
    floor = bpy.context.active_object
    floor.name = "InfinityFloor"
    mat_floor = bpy.data.materials.new(name="Matte_Studio_Floor")
    mat_floor.use_nodes = True
    mat_floor.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.52, 1)
    mat_floor.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    floor.data.materials.append(mat_floor)
    
    world = bpy.data.worlds.new("StudioWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.2, 0.2, 0.2, 1) 

    def add_light(name, loc, target, energy, color, size):
        ld = bpy.data.lights.new(name=name, type='AREA')
        ld.energy, ld.size, ld.color = energy, size, color
        lo = bpy.data.objects.new(name=name, object_data=ld)
        bpy.context.collection.objects.link(lo)
        lo.location = loc
        ldir = mathutils.Vector(target) - mathutils.Vector(loc)
        lo.rotation_euler = ldir.to_track_quat('-Z', 'Y').to_euler()
    
    tc = (cx, cy, cz)
    # 1. Overhead Key (Trắng lạnh xưởng)
    add_light("OverheadKey", (cx + max_dim*0.5, cy - max_dim*0.5, cz + max_dim*2.5), tc, max_dim*max_dim*200, (0.95, 0.98, 1.0), max_dim*1.5)
    # 2. Tech Rim (Cam ấm lướt nhẹ các viền thép)
    add_light("WarmRim", (cx - max_dim*1.8, cy + max_dim*1.8, cz + max_dim*0.5), tc, max_dim*max_dim*180, (1.0, 0.8, 0.6), max_dim*2)
    # 3. Ambient Fill (Bù sáng mảng tối)
    add_light("BounceFill", (cx - max_dim*2, cy - max_dim*2, cz + max_dim), tc, max_dim*max_dim*80, (1.0, 1.0, 1.0), max_dim*3)

gaffer_ai(cx, cy, cz, max_dim, min_z)

# ==========================================================
# EXPERT 4: THE CINEMATOGRAPHER AI (Đạo Diễn Máy Quay)
# ==========================================================
def cinematographer_ai(cx, cy, cz, max_dim):
    print("▶ [Cinematographer] Khóa tiêu cự chuẩn 70mm chống méo ảnh B2B...")
    cam_data = bpy.data.cameras.new(name="B2BCam")
    cam_data.lens = 70 # Góc 70mm chuẩn kỹ thuật chân thực
    
    # Bug Fix: Các file Assembly hệ mm siêu to (10,000 mm) có thể bị cắt tàng hình
    cam_data.clip_end = max_dim * 20.0 
    
    cam = bpy.data.objects.new("B2BCam", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    
    # Góc ISO 45 độ, cao vừa đủ
    omult = 2.4 # Đưa máy xa ra tí để vừa cái khung 9:16 dọc
    cam.location = (cx + max_dim * omult, cy - max_dim * omult, cz + max_dim * 0.9)
    ldir = mathutils.Vector((cx, cy, cz)) - cam.location
    cam.rotation_euler = ldir.to_track_quat('-Z', 'Y').to_euler()

cinematographer_ai(cx, cy, cz, max_dim)

# ==========================================================
# FINAL RENDER
# ==========================================================
print(f"\n[Multi-Agent System] BẮT ĐẦU RENDER BỨC ẢNH HOÀN HẢO TỚI: {output_path} ...")
bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
print("\n[SUCCESS] MAXSKILLS MULTI-AI ĐÃ HOÀN TẤT NHIỆM VỤ ĐẠO DIỄN!")
