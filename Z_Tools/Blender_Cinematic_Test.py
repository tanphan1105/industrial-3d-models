import bpy
import sys
import math
import mathutils

# 1. Parse arguments (Input OBJ and Output Image)
argv = sys.argv
if "--" not in argv:
    print("No arguments provided. Need OBJ file path and output image path.")
    sys.exit(1)

args = argv[argv.index("--") + 1:]
obj_path = args[0]
output_path = args[1]

# 2. Clear Scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 3. Setup Render Engine (Cycles - Hollywood Ray Tracing)
bpy.context.scene.render.engine = 'CYCLES'
try:
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.scene.cycles.device = 'GPU'
except:
    pass
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1920
bpy.context.scene.cycles.samples = 256 # Tăng độ nét thêm chút cho realistic
bpy.context.scene.world = bpy.data.worlds.new("World")
bpy.context.scene.world.use_nodes = True
bg_node = bpy.context.scene.world.node_tree.nodes["Background"]
# Đổi nền sang xám Studio thực tế thay vì tối thui không gian
bg_node.inputs[0].default_value = (0.3, 0.3, 0.3, 1) 
bg_node.inputs[1].default_value = 1.0

# 4. Import OBJ or FBX
if obj_path.lower().endswith(".fbx"):
    bpy.ops.import_scene.fbx(filepath=obj_path)
else:
    bpy.ops.wm.obj_import(filepath=obj_path)

# ... Calculate bounds
objects = bpy.context.selected_objects
if not objects:
    print("Failed to import model")
    sys.exit(1)

min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

for obj in objects:
    for v in obj.bound_box:
        vw = obj.matrix_world @ mathutils.Vector(v)
        min_x, min_y, min_z = min(min_x, vw.x), min(min_y, vw.y), min(min_z, vw.z)
        max_x, max_y, max_z = max(max_x, vw.x), max(max_y, vw.y), max(max_z, vw.z)

cx = (min_x + max_x) / 2
cy = (min_y + max_y) / 2
cz = (min_z + max_z) / 2
dx = max_x - min_x
dy = max_y - min_y
dz = max_z - min_z
max_dim = max(dx, dy, dz)

# 6. ENHANCE Materials - SMART AI HEURISTIC (Color-Based)
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        # Lấy thông số màu RGB từ Inventor
        color = bsdf.inputs["Base Color"].default_value
        r, g, b, a = color[0], color[1], color[2], color[3] if len(color)>3 else 1.0
        
        # Công thức tính độ rực màu (Saturation) và độ sáng (Luminance)
        saturation = max(r,g,b) - min(r,g,b)
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        # Nếu có độ trong suốt (Alpha < 1) -> Biến thành Kính/Nhựa Trong
        if a < 0.99:
            bsdf.inputs["Transmission"].default_value = 1.0
            bsdf.inputs["Roughness"].default_value = 0.05
            bsdf.inputs["Metallic"].default_value = 0.0
        
        # Nếu là màu Xám / Trắng bạc (Inox, Nhôm, Thép)
        elif saturation < 0.15 and luminance > 0.25:
            bsdf.inputs["Metallic"].default_value = 0.85
            bsdf.inputs["Roughness"].default_value = 0.25 # Thép bóng bẩy
            
        # Nếu là Đen hoặc Xám đậm (Cao su, Đệm Ron, Gang đúc)
        elif saturation < 0.15 and luminance <= 0.25:
            bsdf.inputs["Metallic"].default_value = 0.2
            bsdf.inputs["Roughness"].default_value = 0.65 # Sần sùi

        # Nếu có màu sắc rực rỡ (Xanh, Đỏ, Vàng) -> Sơn tĩnh điện công nghiệp hoặc Nhựa màu
        else:
            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Roughness"].default_value = 0.35
            # Phủ một lớp bóng bẩy bên ngoài (Clearcoat) giả lập sơn dầu bóng
            try:
                if "Coat Weight" in bsdf.inputs:
                    bsdf.inputs["Coat Weight"].default_value = 1.0
                    bsdf.inputs["Coat Roughness"].default_value = 0.05
            except:
                pass


# 7. Add Professional Studio Floor (để hứng bóng đổ)
bpy.ops.mesh.primitive_plane_add(size=max_dim*20, location=(cx, cy, min_z))
floor = bpy.context.active_object
floor.name = "StudioFloor"

# Chỉnh vật liệu sàn màu Xám sáng (Matte Studio Grey)
mat_floor = bpy.data.materials.new(name="Matte_Studio_Floor")
mat_floor.use_nodes = True
bf = mat_floor.node_tree.nodes["Principled BSDF"]
bf.inputs["Base Color"].default_value = (0.5, 0.5, 0.53, 1) # Xám lạnh công nghiệp
bf.inputs["Roughness"].default_value = 0.7 # Hơi nhám để phân tán bóng mềm
bf.inputs["Specular IOR Level"].default_value = 0.2
floor.data.materials.append(mat_floor)


# 8. Setup Camera
cam_data = bpy.data.cameras.new(name="CinematicCam")
cam_data.lens = 50
cam_obj = bpy.data.objects.new("CinematicCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Camera Angle
offset_mult = 2.0
cam_obj.location = (cx + max_dim * offset_mult, cy - max_dim * offset_mult, cz + max_dim * 0.8) # Hạ góc máy xuống một chút để thấy sàn rõ hơn
direction = mathutils.Vector((cx, cy, cz)) - cam_obj.location
cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# 9. Setup Lighting - REALISTIC DAYLIGHT STUDIO
def add_area_light(name, loc, target, energy, color, size):
    light_data = bpy.data.lights.new(name=name, type='AREA')
    light_data.energy = energy
    light_data.size = size
    light_data.color = color
    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = loc
    ldir = mathutils.Vector(target) - mathutils.Vector(loc)
    light_obj.rotation_euler = ldir.to_track_quat('-Z', 'Y').to_euler()
    return light_obj

target_center = (cx, cy, cz)

# Key Light (Mô phỏng ánh sáng Mặt trời hắt từ trần nhà xưởng) - Trắng ấm nhẹ
add_area_light("OverheadSun", (cx + max_dim*0.5, cy - max_dim*0.5, cz + max_dim*2.5), target_center, max_dim*max_dim*200, (1.0, 0.95, 0.9), max_dim*1.5)

# Fill Light (Ánh sáng môi trường phòng rộng) - Trắng tinh
add_area_light("AmbientFill", (cx - max_dim*1.5, cy - max_dim*1.5, cz + max_dim*0.5), target_center, max_dim*max_dim*80, (1.0, 1.0, 1.0), max_dim*3)

# Rim/Bounce (Ánh sáng hắt từ sàn bật lên / cửa sổ) - Trắng lạnh tự nhiên
add_area_light("WindowBounce", (cx - max_dim*1.5, cy + max_dim*1.5, cz - max_dim*0.5), target_center, max_dim*max_dim*150, (0.9, 0.95, 1.0), max_dim*2)

# 9. Render the shot!
print(f"Rendering Cinematic Frame to: {output_path}")
bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
print("SUPER RENDER COMPLETE!")
