import re
import os
import glob
import shutil

preview_dir = r'd:\WT3D_Project\Preview_Image'
batch_dir = r'd:\WT3D_Project\1_Exports_Batch'
target_img_dir = r'd:\WT3D_Project\deploy\images'
local_img_dir = r'd:\WT3D_Project\images'

os.makedirs(target_img_dir, exist_ok=True)
os.makedirs(local_img_dir, exist_ok=True)

# Gán chính xác từng đường dẫn
img_map = {
    # Skids (5 items)
    "RO Water Treatment System 1m³/h": {"tag": "RO System", "desc": "Industrial reverse osmosis system with PLC control.", "src": r"d:\WT3D_Project\1_Exports_Batch\Industrial_Ro_Water_Treatment_System_1m_H_Plc_Controlled_Auto_Cip_4_4040_Membranes\Industrial_Ro_Water_Treatment_System_1m_H_Plc_Controlled_Auto_Cip_4_4040_Membranes_Hero.jpg"},
    "Ozone Generator 50-100 g/h": {"tag": "Ozone System", "desc": "Industrial corona discharge ozone generator skid.", "src": r"d:\WT3D_Project\Preview_Image\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology\Industrial_Ozone_Generator_50_100_Gh_Corona_Discharge_Technology_Hero.jpg"},
    "Automatic FRP Filter 48x72 (Motorized)": {"tag": "Filtration Skid", "desc": "Automatic FRP sand & carbon filter tank with PLC motorized valves.", "src": r"d:\WT3D_Project\1_Exports_Batch\FRP Sand & Carbon Filter Tank 48x72  20 m3h Pretreatment for Industrial RO System  RUNXIN Autovalve\FRP Sand & Carbon Filter Tank 48x72  20 m3h Pretreatment for Industrial RO System  RUNXIN Autovalve_Hero.jpg"},
    "Automatic FRP Filter 48x72 (Runxin)": {"tag": "Filtration Skid", "desc": "20 m³/h industrial RO pretreatment with RUNXIN control valve.", "src": r"d:\WT3D_Project\Preview_Image\Frp_Water_Filter_Tank_14_65_Inch_Blue_Composite_Pressure_Vessel\Frp_Water_Filter_Tank_14_65_Inch_Blue_Composite_Pressure_Vessel_01_Overall_Hero.jpg"},
    "Mineral Dosing & RO Frame Station": {"tag": "Dosing System", "desc": "Stainless steel mineral dosing station and RO assembly frame.", "src": r"d:\WT3D_Project\1_Exports_Batch\Industrial_Ro_Water_Treatment_System_1m_H_Plc_Controlled_Auto_Cip_4_4040_Membranes\Industrial_Ro_Water_Treatment_System_1m_H_Plc_Controlled_Auto_Cip_4_4040_Membranes_02_Top_Plan_Layout.jpg"},

    # Components
    "FRP RO Membrane Housing 4040": {"tag": "Membrane Housing", "desc": "Single pressure vessel for 4040 reverse osmosis elements.", "src": r"d:\WT3D_Project\Preview_Image\Frp_Ro_Membrane_Housing_4040_Single_Pressure_Vessel_For_Reverse_Osmosis_System\Frp_Ro_Membrane_Housing_4040_Single_Pressure_Vessel_For_Reverse_Osmosis_System_01_Overall_Hero.jpg"},
    "Dual FRP RO Membrane Housing 4040": {"tag": "Membrane Housing", "desc": "Twin assembly of 4040 pressure vessels for parallel RO operation.", "src": r"d:\WT3D_Project\Preview_Image\Dual_Frp_Ro_Membrane_Housing_4040_2_Pressure_Vessels_For_Reverse_Osmosis_System\Dual_Frp_Ro_Membrane_Housing_4040_2_Pressure_Vessels_For_Reverse_Osmosis_System_01_Overall_Hero.jpg"},
    "Triple Element Pressure Vessel": {"tag": "Membrane Housing", "desc": "Multi-element FRP pressure vessel for large-scale RO systems.", "src": r"d:\WT3D_Project\Preview_Image\Triple Element Pressure Vessel for Industrial RO System\Triple Element Pressure Vessel for Industrial RO System_01_Overall_Hero.jpg"},
    "FRP RO Membrane Housing 8040": {"tag": "Membrane Housing", "desc": "Heavy-duty 8040 pressure vessel for high-capacity RO.", "src": r"d:\WT3D_Project\Preview_Image\Frp_Ro_Membrane_Housing_8040_Pressure_Vessel_For_Industrial_Reverse_Osmosis_System\Frp_Ro_Membrane_Housing_8040_Pressure_Vessel_For_Industrial_Reverse_Osmosis_System_01_Overall_Hero.jpg"},
    "SS304 Filter Housing 20-Inch": {"tag": "Filter Housing", "desc": "Single cartridge stainless steel 304 filter housing.", "src": r"d:\WT3D_Project\Preview_Image\SS304_Filter_Housing_1_Cartridge_20_Inch_Pp_Cartridge\SS304_Filter_Housing_1_Cartridge_20_Inch_Pp_Cartridge_01_Overall_Hero.jpg"},
    "SS304 3-Cartridge Filter Housing": {"tag": "Filter Housing", "desc": "Stainless steel housing accommodating three 20-inch filter cartridges.", "src": r"d:\WT3D_Project\Preview_Image\304_Stainless_Steel_3_Cartridge_Filter_Housing_20_Inch\304_Stainless_Steel_3_Cartridge_Filter_Housing_20_Inch_01_Overall_Hero.jpg"},
    "SS304 7-Cartridge Filter Housing": {"tag": "Filter Housing", "desc": "High flow rate housing for seven 20-inch water filter cartridges.", "src": r"d:\WT3D_Project\Preview_Image\304_Stainless_Steel_7_Cartridge_Filter_Housing_20_Inch\304_Stainless_Steel_7_Cartridge_Filter_Housing_20_Inch_01_Overall_Hero.jpg"},
    "SS304 Multi-Cartridge Housing 7x40": {"tag": "Filter Housing", "desc": "Industrial-scale multi-cartridge housing fitting seven 40-inch PP filters.", "src": r"d:\WT3D_Project\Preview_Image\Stainless_Steel_304_Multi_Cartridge_Filter_Housing_7_40_Inch_Pp_Filters_1_5_Micron\Stainless_Steel_304_Multi_Cartridge_Filter_Housing_7_40_Inch_Pp_Filters_1_5_Micron_01_Overall_Hero.jpg"},
    "SS Household Water Filter 40 Micron": {"tag": "Filter Housing", "desc": "Stainless steel household water pre-filter with 40-micron mesh.", "src": r"d:\WT3D_Project\Preview_Image\Stainless_Steel_Household_Water_Filter_40_Micron_Cartridge\Stainless_Steel_Household_Water_Filter_40_Micron_Cartridge_01_Overall_Hero.jpg"},
    "Plastic Filter Housing 20-Inch": {"tag": "Filter Housing", "desc": "Standard single cartridge plastic filter housing for 20-inch PP filters.", "src": r"d:\WT3D_Project\Preview_Image\Plastic_Filter_Housing_1_Cartridge_20_Inch_Pp_Cartridge\Plastic_Filter_Housing_1_Cartridge_20_Inch_Pp_Cartridge_01_Overall_Hero.jpg"},
    "Big Blue Water Filter Housing 20-Inch": {"tag": "Filter Housing", "desc": "High flow Big Blue housing for heavy-duty water treatment.", "src": r"d:\WT3D_Project\Preview_Image\Big_Blue_Water_Filter_Housing_20_Inch_High_Flow_Water_Treatment_Filter\Big_Blue_Water_Filter_Housing_20_Inch_High_Flow_Water_Treatment_Filter_01_Overall_Hero.jpg"},
    "Dual 20-Inch Plastic Filter Housing": {"tag": "Filter Housing", "desc": "Two-stage 20-inch plastic water filter housing assembly.", "src": r"d:\WT3D_Project\Preview_Image\Dual_20_Inch_Plastic_Water_Filter_Housing_2_Cartridge_Pre_Filter_Assembly\Dual_20_Inch_Plastic_Water_Filter_Housing_2_Cartridge_Pre_Filter_Assembly_01_Overall_Hero.jpg"},
    "Triple 20-Inch Water Filter Set": {"tag": "Filter Housing", "desc": "Complete 3-stage pre-filtration system with triple housings.", "src": r"d:\WT3D_Project\Preview_Image\Triple_20_Inch_Water_Filter_Housing_Set_3_Stage_Pre_Filtration_System\Triple_20_Inch_Water_Filter_Housing_Set_3_Stage_Pre_Filtration_System_01_Overall_Hero.jpg"},
    "2-Inch Angle Backwash Filter Valve": {"tag": "Valve Component", "desc": "Angle backwash valve designed for agricultural and industrial irrigation.", "src": r"d:\WT3D_Project\Preview_Image\2_Inch_Angle_Backwash_Filter_Valve_For_Irrigation\2_Inch_Angle_Backwash_Filter_Valve_For_Irrigation_01_Overall_Hero.jpg"},
    "3/4-Inch Y-Type Disc Filter 120 Mesh": {"tag": "Filter Component", "desc": "Male thread Y-type disc filter for drip irrigation and fine filtration.", "src": r"d:\WT3D_Project\Preview_Image\3_4_1_Male_Thread_Y_Type_Disc_Filter_120_Mesh\3_4_1_Male_Thread_Y_Type_Disc_Filter_120_Mesh_01_Overall_Hero.jpg"},
    "Transparent Plastic Disc Filter 2-Inch": {"tag": "Filter Component", "desc": "2-inch male thread transparent plastic disc filter for visual inspection.", "src": r"d:\WT3D_Project\Preview_Image\Transparent_Plastic_Disc_Filter_2_Inch_Male_Thread.iam\Transparent_Plastic_Disc_Filter_2_Inch_Male_Thread.iam_01_Overall_Hero.jpg"},
    "Screen Type Irrigation Filter 120 Mesh": {"tag": "Filter Component", "desc": "High-efficiency screen filter for agricultural and industrial water systems.", "src": r"d:\WT3D_Project\Preview_Image\Screen_Type_Irrigation_Filter_120_Mesh\Screen_Type_Irrigation_Filter_120_Mesh_01_Overall_Hero.jpg"}
}

card_template = """
    <article class="mc rv" style="background:var(--bg-s)">
      <div class="mt" style="background:var(--bg-t);position:relative">
        <div style="position:absolute;top:16px;left:16px;background:rgba(255,255,255,0.8);backdrop-filter:blur(10px);padding:4px 12px;border-radius:100px;font-size:10px;font-family:var(--fm);color:var(--tx-s);font-weight:600;z-index:2;letter-spacing:0.05em">{tag}</div>
        <img src="{img_path}" alt="{title}" loading="lazy" style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block">
      </div>
      <div class="mb">
        <h3 style="font-size:18px;margin-bottom:8px">{title}</h3>
        <p style="font-size:13px;line-height:1.5;color:var(--tx-s);margin-bottom:16px">{desc}</p>
        <div class="sp">
          <div class="sp-r"><span class="sp-k">Feature</span><span class="sp-v" style="color:var(--ac)">AR Ready</span></div>
          <div class="sp-r"><span class="sp-k">Textures</span><span class="sp-v">4K PBR</span></div>
          <div class="sp-r"><span class="sp-k">Formats</span><span class="sp-v">USDZ / GLB</span></div>
        </div>
        <div class="mf" style="margin-top:20px">
          <a href="https://www.fab.com/sellers/Trong%20Tan%20Phan" target="_blank" class="mf-p">Get on Fab</a>
          <a href="https://www.cgtrader.com/designers/tanphan1105" target="_blank" class="mf-s">CGTrader</a>
        </div>
      </div>
    </article>
"""

def generate_section(keys, prefix):
    html = []
    for i, key in enumerate(keys):
        item = img_map[key]
        src_img = item["src"]
        
        new_img_name = f"c_{prefix}_{i}.jpg"
        if os.path.exists(src_img):
            shutil.copy(src_img, os.path.join(local_img_dir, new_img_name))
            shutil.copy(src_img, os.path.join(target_img_dir, new_img_name))
            item['img_path'] = f"images/{new_img_name}"
        else:
            item['img_path'] = "ozone_generator_hero.jpg"
            
        item['title'] = key
        html.append(card_template.format(**item))
    return "".join(html)

skids_keys = list(img_map.keys())[:5]
components_keys = list(img_map.keys())[5:]

# CHANGED: Use carousel-track instead of mg
skids_html = f'\n  <div class="carousel-track">\n{generate_section(skids_keys, "s")}  </div>\n'
components_html = f'\n  <div class="carousel-track">\n{generate_section(components_keys, "c")}  </div>\n'

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

print("Successfully injected 22 cards with mapped images and carousel layout!")
