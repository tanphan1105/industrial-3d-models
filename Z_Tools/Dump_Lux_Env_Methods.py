import lux

out_path = r"d:\WT3D_Project\Z_Tools\lux_env_methods.txt"

with open(out_path, "w", encoding="utf-8") as f:
    try:
        env = lux.getActiveEnvironment()
        f.write("=== ACTIVE ENVIRONMENT METHODS ===\n")
        f.write("Type: " + str(type(env)) + "\n\n")
        for item in dir(env):
            f.write(item + "\n")
    except Exception as e:
        f.write("\nCould not get Active Environment: " + str(e))

print("Done! Saved to " + out_path)
