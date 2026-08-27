import lux

def scan_materials():
    out_path = r"d:\WT3D_Project\Z_Tools\inventor_materials_scan.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Node Material Scan\n")
        f.write("========================\n")
        
        nodes = list(lux.getSceneTree().find(lux.NODE_TYPE_OBJECT)) or []
        for node in nodes:
            node_name = node.getName()
            try:
                # Try getting material directly from node
                if hasattr(node, "getMaterial"):
                    mat = node.getMaterial()
                    mat_name = mat.getName() if hasattr(mat, "getName") else str(mat)
                    f.write(f"Node: {node_name} | node.getMaterial(): {mat_name}\n")
                else:
                    f.write(f"Node: {node_name} | No getMaterial()\n")
            except Exception as e:
                f.write(f"Node: {node_name} | ERROR: {e}\n")
    print(f"✅ Saved scan to: {out_path}")

scan_materials()
