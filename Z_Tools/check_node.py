import lux
nodes = list(lux.getSceneTree().find("Plastic_Filter_Housi"))
if nodes:
    node = nodes[0]
    print("Node:", node)
    print("Node type:", type(node))
    print("Node dir:", dir(node))
else:
    print("Node not found")
