import lux

out_path = r"d:\WT3D_Project\Z_Tools\lux_methods.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== LUX MODULE METHODS ===\n")
    for item in dir(lux):
        f.write(item + "\n")
        
    try:
        env_node = lux.getSceneTree().find(lux.NODE_TYPE_ENVIRONMENT)[0]
        f.write("\n=== ENVIRONMENT NODE METHODS ===\n")
        for item in dir(env_node):
            f.write(item + "\n")
    except Exception as e:
        f.write("\nCould not get Environment Node: " + str(e))

print("Done! Saved to " + out_path)
