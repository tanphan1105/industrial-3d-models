import re

with open(r'd:\WT3D_Project\landing_page_v3_master.html','r',encoding='utf-8') as f:
    content = f.read()

print("Water Treatment present:", "Water Treatment" in content)
print("New folder present:", "New folder" in content)
print(".iam present:", ".iam" in content)
print("Real-world Scale present:", "Real-world Scale" in content)
print("RO System Packages present:", "RO System Packages" in content)
print("20+ present:", "20+" in content)
print("scrollTrack -1 present:", "scrollTrack('track-skids', -1)" in content)

articles = re.findall(r'<article class="mc rv"', content)
print("Total cards:", len(articles))
