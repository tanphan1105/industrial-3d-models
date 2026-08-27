import re
import os
import glob
import shutil

preview_dir = r'd:\WT3D_Project\Preview_Image'
target_img_dir = r'd:\WT3D_Project\deploy\images'
local_img_dir = r'd:\WT3D_Project\images'

os.makedirs(target_img_dir, exist_ok=True)
os.makedirs(local_img_dir, exist_ok=True)

# Define items with a 'folder_hint' to find the right directory
skids = [
    {"title": "RO Water Treatment System 1m³/h", "tag": "RO System", "desc": "Industrial reverse osmosis system with PLC control, Auto CIP.", "hint": "Industrial_Ro_Water_Treatment_System"},
    {"title": "Ozone Generator 50-100 g/h", "tag": "Ozone System", "desc": "Industrial corona discharge ozone generator skid.", "hint": "Ozone_Generator"},
    {"title": "Automatic FRP Filter (Motorized)", "tag": "Filtration Skid", "desc": "Automatic FRP sand & carbon filter tank with PLC motorized valves.", "hint": "Motorized"},
    {"title": "Automatic FRP Filter (Runxin)", "tag": "Filtration Skid", "desc": "20 m³/h industrial RO pretreatment with RUNXIN control valve.", "hint": "RUNXIN Control Valve"},
    {"title": "Mineral Dosing & RO Frame Station", "tag": "Dosing System", "desc": "Stainless steel mineral dosing station and RO assembly frame.", "hint": "CHAM KHOANG"}
]

components = [
    {"title": "FRP RO Membrane Housing 4040", "tag": "Membrane Housing", "desc": "Single pressure vessel for 4040 reverse osmosis membrane elements.", "hint": "4040_Single"},
    {"title": "Dual FRP RO Membrane Housing 4040", "tag": "Membrane Housing", "desc": "Twin assembly of 4040 pressure vessels for parallel RO operation.", "hint": "Dual_Frp"},
    {"title": "Triple Element Pressure Vessel", "tag": "Membrane Housing", "desc": "Multi-element FRP pressure vessel for large-scale industrial RO systems.", "hint": "Triple Element"},
    {"title": "FRP RO Membrane Housing 8040", "tag": "Membrane Housing", "desc": "Heavy-duty 8040 pressure vessel for high-capacity industrial reverse osmosis.", "hint": "8040"},
    
    {"title": "SS304 Filter Housing 20-Inch", "tag": "Filter Housing", "desc": "Single cartridge stainless steel 304 filter housing.", "hint": "SS304_Filter_Housing_1_Cartridge"},
    {"title": "SS304 3-Cartridge Filter Housing", "tag": "Filter Housing", "desc": "Stainless steel housing accommodating three 20-inch filter cartridges.", "hint": "304_Stainless_Steel_3_Cartridge"},
    {"title": "SS304 7-Cartridge Filter Housing", "tag": "Filter Housing", "desc": "High flow rate housing for seven 20-inch water filter cartridges.", "hint": "304_Stainless_Steel_7_Cartridge"},
    {"title": "SS304 Multi-Cartridge Housing 7x40", "tag": "Filter Housing", "desc": "Industrial-scale multi-cartridge housing fitting seven 40-inch PP filters.", "hint": "7_40_Inch"},
    {"title": "SS Household Water Filter 40 Micron", "tag": "Filter Housing", "desc": "Stainless steel household water pre-filter with 40-micron mesh.", "hint": "Household_Water_Filter"},
    
    {"title": "Plastic Filter Housing 20-Inch", "tag": "Filter Housing", "desc": "Standard single cartridge plastic filter housing for 20-inch PP filters.", "hint": "Plastic_Filter_Housing_1_Cartridge"},
    {"title": "Big Blue Water Filter Housing 20-Inch", "tag": "Filter Housing", "desc": "High flow Big Blue housing for heavy-duty water treatment filtration.", "hint": "Big_Blue"},
    {"title": "Dual 20-Inch Plastic Filter Housing", "tag": "Filter Housing", "desc": "Two-stage 20-inch plastic water filter housing assembly.", "hint": "Dual_20_Inch"},
    {"title": "Triple 20-Inch Water Filter Set", "tag": "Filter Housing", "desc": "Complete 3-stage pre-filtration system with triple housings.", "hint": "Triple_20_Inch"},
    
    {"title": "FRP Water Filter Tank 14x65 Inch", "tag": "Tank Vessel", "desc": "Blue composite FRP pressure vessel tank for sand or carbon media.", "hint": "14_65_Inch"},
    {"title": "2-Inch Angle Backwash Filter Valve", "tag": "Valve Component", "desc": "Angle backwash valve designed for agricultural and industrial irrigation.", "hint": "Angle_Backwash"},
    {"title": "3/4-Inch Y-Type Disc Filter 120 Mesh", "tag": "Filter Component", "desc": "Male thread Y-type disc filter for drip irrigation and fine filtration.", "hint": "3_4_1_Male"},
    {"title": "Transparent Plastic Disc Filter 2-Inch", "tag": "Filter Component", "desc": "2-inch male thread transparent plastic disc filter for visual inspection.", "hint": "Transparent_Plastic_Disc_Filter"},
    {"title": "Screen Type Irrigation Filter 120 Mesh", "tag": "Filter Component", "desc": "High-efficiency screen filter for agricultural and industrial water systems.", "hint": "Screen_Type"}
]

def find_hero_image(hint):
    # Find folder matching hint
    folders = [f for f in os.listdir(preview_dir) if os.path.isdir(os.path.join(preview_dir, f))]
    target_folder = None
    for f in folders:
        if hint.lower() in f.lower():
            target_folder = f
            break
            
    if not target_folder:
        return None
        
    folder_path = os.path.join(preview_dir, target_folder)
    
    # Try to find 'Hero' image first
    imgs = glob.glob(os.path.join(folder_path, '*Hero*.jpg'))
    if not imgs:
        imgs = glob.glob(os.path.join(folder_path, '*.jpg'))
        
    if imgs:
        # Get the shortest name or first
        imgs.sort(key=len)
        return imgs[0]
    return None

card_template = """
    <article class="mc rv" style="background:var(--bg-s)">
      <div class="mt" style="background:var(--bg-t);position:relative">
        <div style="position:absolute;top:16px;left:16px;background:rgba(255,255,255,0.8);backdrop-filter:blur(10px);padding:4px 12px;border-radius:100px;font-size:10px;font-family:var(--fm);color:var(--tx-s);font-weight:600;z-index:2;letter-spacing:0.05em">{tag}</div>
        <img src="{img_path}" alt="{title}" loading="lazy" style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block">
      </div>
      <div class="mb">
        <h3>{title}</h3>
        <p>{desc}</p>
        <div class="sp">
          <div class="sp-r"><span class="sp-k">Feature</span><span class="sp-v" style="color:var(--ac)">AR Ready</span></div>
          <div class="sp-r"><span class="sp-k">Textures</span><span class="sp-v">4K PBR</span></div>
          <div class="sp-r"><span class="sp-k">Formats</span><span class="sp-v">USDZ / GLB</span></div>
        </div>
        <div class="mf" style="margin-top:24px">
          <a href="https://www.fab.com/sellers/Trong%20Tan%20Phan" target="_blank" class="mf-p">Get on Fab</a>
          <a href="https://www.cgtrader.com/designers/tanphan1105" target="_blank" class="mf-s">CGTrader</a>
        </div>
      </div>
    </article>
"""

def process_items(items, prefix):
    html = []
    for i, item in enumerate(items):
        src_img = find_hero_image(item['hint'])
        if src_img:
            ext = os.path.splitext(src_img)[1]
            new_img_name = f"{prefix}_{i}{ext}"
            
            # Copy to local and deploy folder
            shutil.copy(src_img, os.path.join(local_img_dir, new_img_name))
            shutil.copy(src_img, os.path.join(target_img_dir, new_img_name))
            
            # Update item data
            item['img_path'] = f"images/{new_img_name}"
        else:
            item['img_path'] = "ozone_generator_hero.jpg" # fallback
            
        html.append(card_template.format(**item))
    return "".join(html)

skids_html = f'\n  <div class="mg">\n{process_items(skids, "skid")}  </div>\n'
components_html = f'\n  <div class="mg">\n{process_items(components, "comp")}  </div>\n'

file_path = r'd:\WT3D_Project\landing_page_v3_master.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace skids grid
content = re.sub(
    r'(<section class="sec" id="systems">.*?<p>.*?</p>\n  </div>).*?(</section>)',
    rf'\1{skids_html}\2',
    content,
    flags=re.DOTALL
)

# Replace equipment grid
content = re.sub(
    r'(<section class="sec sec-dark" id="equipment">.*?<p>.*?</p>\n  </div>).*?(</section>)',
    rf'\1{components_html}\2',
    content,
    flags=re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully injected 23 cards with real images!")
