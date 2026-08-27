import re
path = r'd:\WT3D_Project\Z_Tools\Auto_KeyShot_Render.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'safe\(lux\.([a-zA-Z0-9_]+),', r'lux_safe("\1",', text)
text = re.sub(r'safe\(lux\.([a-zA-Z0-9_]+)\)', r'lux_safe("\1")', text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Regex replacement successful.")
