import re
import os

skids = [
    {"title": "RO Water Treatment System 1m³/h", "tag": "RO System", "desc": "Industrial reverse osmosis system with PLC control, Auto CIP, and 4x 4040 membranes."},
    {"title": "Ozone Generator 50-100 g/h", "tag": "Ozone System", "desc": "Industrial corona discharge ozone generator skid. Engineered with detailed cooling layout and transformers."},
    {"title": "Automatic FRP Filter 48x72 (Motorized)", "tag": "Filtration Skid", "desc": "Automatic FRP sand & carbon filter tank with PLC motorized butterfly valves for RO feed water."},
    {"title": "Automatic FRP Filter 48x72 (Runxin)", "tag": "Filtration Skid", "desc": "20 m³/h industrial RO pretreatment sand & carbon filter with RUNXIN control valve."},
    {"title": "Mineral Dosing & RO Frame Station", "tag": "Dosing System", "desc": "Stainless steel mineral dosing station and RO assembly frame for industrial applications."}
]

components = [
    {"title": "FRP RO Membrane Housing 4040", "tag": "Membrane Housing", "desc": "Single pressure vessel for 4040 reverse osmosis membrane elements."},
    {"title": "Dual FRP RO Membrane Housing 4040", "tag": "Membrane Housing", "desc": "Twin assembly of 4040 pressure vessels for parallel RO operation."},
    {"title": "Triple Element Pressure Vessel", "tag": "Membrane Housing", "desc": "Multi-element FRP pressure vessel for large-scale industrial RO systems."},
    {"title": "FRP RO Membrane Housing 8040", "tag": "Membrane Housing", "desc": "Heavy-duty 8040 pressure vessel for high-capacity industrial reverse osmosis."},
    
    {"title": "SS304 Filter Housing 20-Inch", "tag": "Filter Housing", "desc": "Single cartridge stainless steel 304 filter housing for 20-inch PP cartridges."},
    {"title": "SS304 3-Cartridge Filter Housing", "tag": "Filter Housing", "desc": "Stainless steel housing accommodating three 20-inch filter cartridges."},
    {"title": "SS304 7-Cartridge Filter Housing", "tag": "Filter Housing", "desc": "High flow rate housing for seven 20-inch water filter cartridges."},
    {"title": "SS304 Multi-Cartridge Housing 7x40", "tag": "Filter Housing", "desc": "Industrial-scale multi-cartridge housing fitting seven 40-inch PP filters."},
    {"title": "SS Household Water Filter 40 Micron", "tag": "Filter Housing", "desc": "Stainless steel household water pre-filter with 40-micron washable mesh."},
    
    {"title": "Plastic Filter Housing 20-Inch", "tag": "Filter Housing", "desc": "Standard single cartridge plastic filter housing for 20-inch PP filters."},
    {"title": "Big Blue Water Filter Housing 20-Inch", "tag": "Filter Housing", "desc": "High flow Big Blue housing for heavy-duty water treatment filtration."},
    {"title": "Dual 20-Inch Plastic Filter Housing", "tag": "Filter Housing", "desc": "Two-stage 20-inch plastic water filter housing assembly for pre-filtration."},
    {"title": "Triple 20-Inch Water Filter Set", "tag": "Filter Housing", "desc": "Complete 3-stage pre-filtration system with triple 20-inch housings."},
    
    {"title": "FRP Water Filter Tank 14x65 Inch", "tag": "Tank Vessel", "desc": "Blue composite FRP pressure vessel tank for sand or carbon media."},
    {"title": "2-Inch Angle Backwash Filter Valve", "tag": "Valve Component", "desc": "Angle backwash valve designed for agricultural and industrial irrigation."},
    {"title": "3/4-Inch Y-Type Disc Filter 120 Mesh", "tag": "Filter Component", "desc": "Male thread Y-type disc filter for drip irrigation and fine filtration."},
    {"title": "Transparent Plastic Disc Filter 2-Inch", "tag": "Filter Component", "desc": "2-inch male thread transparent plastic disc filter for visual inspection."},
    {"title": "Screen Type Irrigation Filter 120 Mesh", "tag": "Filter Component", "desc": "High-efficiency screen filter for agricultural and industrial water systems."}
]

card_template = """
    <article class="mc rv" style="background:var(--bg-s)">
      <div class="mt" style="background:var(--bg-t);display:flex;align-items:center;justify-content:center;aspect-ratio:16/9;position:relative">
        <div style="position:absolute;top:16px;left:16px;background:rgba(255,255,255,0.8);backdrop-filter:blur(10px);padding:4px 12px;border-radius:100px;font-size:10px;font-family:var(--fm);color:var(--tx-s);font-weight:600;z-index:2;letter-spacing:0.05em">{tag}</div>
        <div style="color:var(--tx-t);text-align:center">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="opacity:0.5;margin-bottom:8px;display:inline-block"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
          <div style="font-size:11px;font-family:var(--fm);letter-spacing:0.05em">IMAGE PLACEHOLDER</div>
        </div>
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

def generate_html(items):
    return "".join([card_template.format(**item) for item in items])

skids_html = f'\n  <div class="mg">\n{generate_html(skids)}  </div>\n'
components_html = f'\n  <div class="mg">\n{generate_html(components)}  </div>\n'

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

print("Successfully injected 23 cards into landing_page_v3_master.html")
