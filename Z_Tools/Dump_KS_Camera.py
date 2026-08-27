import lux
import luxmath

out_path = r"d:\WT3D_Project\Z_Tools\debug_camera.txt"

with open(out_path, "w", encoding="utf-8") as f:
    try:
        lux.setStandardView(lux.VIEW_ISOMETRIC)
        f.write("Standard View: ISOMETRIC set successfully.\n")
        
        f.write("LookAt: " + str(lux.getCameraLookAt()) + "\n")
        f.write("Distance: " + str(lux.getCameraDistance()) + "\n")
        
        try:
            sph = lux.getSphericalCamera()
            f.write("SphericalCamera: " + str(sph) + "\n")
        except Exception as e:
            f.write("getSphericalCamera failed: " + str(e) + "\n")
            
        try:
            bb = lux.getSceneBoundingBox()
            f.write("getSceneBoundingBox: " + str(bb) + "\n")
            if hasattr(bb, "center"):
                f.write("  center: " + str(bb.center()) + "\n")
            elif hasattr(bb, "getCenter"):
                f.write("  getCenter: " + str(bb.getCenter()) + "\n")
        except Exception as e:
            f.write("getSceneBoundingBox failed: " + str(e) + "\n")
            
    except Exception as e:
        f.write("Error: " + str(e) + "\n")

print("Done! Saved to " + out_path)
