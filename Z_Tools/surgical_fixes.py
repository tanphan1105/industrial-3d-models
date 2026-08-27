import re

file_path = r'd:\WT3D_Project\landing_page_v3_master.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix arrow onclick: pass direction 1/-1 instead of fixed pixel offset
content = content.replace("scrollTrack('track-skids', -400)", "scrollTrack('track-skids', -1)")
content = content.replace("scrollTrack('track-skids', 400)", "scrollTrack('track-skids', 1)")
content = content.replace("scrollTrack('track-comps', -400)", "scrollTrack('track-comps', -1)")
content = content.replace("scrollTrack('track-comps', 400)", "scrollTrack('track-comps', 1)")

# 2. Fix H1 headline
content = content.replace("Water &amp; Ozone.<br>", "Water Treatment.<br>")
content = content.replace("Water & Ozone.<br>", "Water Treatment.<br>")
content = content.replace("Advanced Oxidation Systems, RO skids, and industrial components", "Reverse Osmosis Systems, filtration skids, and industrial components")

# 3. Fix Mega CTA Vietnamese text
content = content.replace(
    "Gi\u00e1m s\u00e1t th\u1eddi gian th\u1ef1c.",
    "Real-world Scale."
)
content = content.replace(
    'D\u1eef li\u1ec7u <span class="gr">tr\u1ef1c quan.</span>',
    'Engineering <span class="gr">Precision.</span>'
)
content = content.replace(
    "Kh\u00e1m ph\u00e1 tr\u1ecdn b\u1ed9 27+ m\u00f4 h\u00ecnh k\u1ef9 thu\u1eadt ch\u00ednh x\u00e1c tuy\u1ec7t \u0111\u1ed1i. T\u1ed1i \u01b0u cho m\u00f4i tr\u01b0\u1eddng th\u1ef1c t\u1ebf \u1ea3o, Unreal Engine, WebGL v\u00e0 thi\u1ebft k\u1ebf ph\u00e2n x\u01b0\u1edfng.",
    "Explore the complete library of 20+ engineering-accurate 3D models. Optimized for AR/VR, Unreal Engine, WebGL, and industrial plant design."
)
content = content.replace("Kh\u00e1m ph\u00e1 tr\u00ean Fab", "Explore on Fab")
content = content.replace("Xem tr\u00ean CGTrader", "View on CGTrader")

# 4. Fix stats count and language
content = content.replace("M\u00f4 h\u00ecnh c\u00f4ng nghi\u1ec7p", "Industrial Models")
content = content.replace("V\u1eadt li\u1ec7u v\u1eadt l\u00fd", "Physical Textures")
content = content.replace(">27+<", ">20+<")

# 5. Fix .iam in card title
content = content.replace("Transparent Plastic Disc Filter 2 Inch Male Thread.iam", "Transparent Plastic Disc Filter 2 Inch Male Thread")

# 6. Remove 'New folder' card
content = re.sub(
    r'[ \t]*<article class="mc rv"[^>]*>(?:(?!</article>).)*?New folder(?:(?!</article>).)*?</article>\s*',
    '',
    content,
    flags=re.DOTALL
)

# 7. Footer: update Products list
footer_old = """<li><a href="#systems">RO Skid 30 m\u00b3/h</a></li>
        <li><a href="#systems">RO Skid 10 m\u00b3/h</a></li>
        <li><a href="#systems">Filtration Skid</a></li>
        <li><a href="#equipment">Ozone Generator</a></li>
        <li><a href="#equipment">HP Pump</a></li>
        <li><a href="#equipment">Membrane Housing</a></li>"""

footer_new = """<li><a href="#systems">RO System Packages</a></li>
        <li><a href="#systems">Ozone Generators</a></li>
        <li><a href="#equipment">Membrane Housings</a></li>
        <li><a href="#equipment">Filter Housings</a></li>
        <li><a href="#equipment">Tanks &amp; Valves</a></li>"""

content = content.replace(footer_old, footer_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("All surgical fixes applied successfully!")
