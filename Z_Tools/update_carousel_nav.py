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

# Lấy tất cả ảnh Hero
all_imgs = glob.glob(os.path.join(preview_dir, '**', '*.jpg'), recursive=True) + glob.glob(os.path.join(batch_dir, '**', '*.jpg'), recursive=True)
folder_map = {}
for img in all_imgs:
    folder = os.path.basename(os.path.dirname(img))
    if 'Hero' in img or 'Overall' in img:
        if folder not in folder_map or 'Hero' in img:
            folder_map[folder] = img

# Build items dynamically
def clean_title(name):
    # Thay thế gạch dưới và định dạng lại
    name = name.replace("_", " ")
    # Bỏ các phần đuôi dư thừa để không quá dài
    name = re.sub(r'For Reverse Osmosis.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'For Industrial.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'High Flow Water.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'Plc Controlled.*', 'PLC', name, flags=re.IGNORECASE)
    name = name.strip()
    if len(name) > 65:
        name = name[:65] + "..."
    return name

items = []
for folder, img_path in folder_map.items():
    # Phân loại Skid hay Component
    is_skid = False
    lower_f = folder.lower()
    if 'system' in lower_f or 'skid' in lower_f or 'generator' in lower_f or 'plc' in lower_f or 'runxin' in lower_f:
        is_skid = True
        
    tag = "System & Skid" if is_skid else "Equipment Component"
    if 'housing' in lower_f: tag = "Housing"
    if 'filter' in lower_f and not is_skid: tag = "Filter"
    if 'valve' in lower_f: tag = "Valve"
    if 'tank' in lower_f and not is_skid: tag = "Tank"
    
    items.append({
        "folder": folder,
        "title": clean_title(folder),
        "tag": tag,
        "desc": f"Engineering-grade 3D model: {clean_title(folder)}.",
        "src": img_path,
        "is_skid": is_skid
    })

# Sắp xếp để những món chính lên đầu
items.sort(key=lambda x: (not x['is_skid'], x['title']))

card_template = """
    <article class="mc rv" style="background:var(--bg-s);flex:0 0 min(85vw,360px);scroll-snap-align:start">
      <div class="mt" style="background:var(--bg-t);position:relative">
        <div style="position:absolute;top:16px;left:16px;background:rgba(255,255,255,0.8);backdrop-filter:blur(10px);padding:4px 12px;border-radius:100px;font-size:10px;font-family:var(--fm);color:var(--tx-s);font-weight:600;z-index:2;letter-spacing:0.05em">{tag}</div>
        <img src="{img_path}" alt="{title}" loading="lazy" style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block;pointer-events:none">
      </div>
      <div class="mb">
        <h3 style="font-size:16px;line-height:1.4;margin-bottom:8px">{title}</h3>
        <p style="font-size:13px;line-height:1.5;color:var(--tx-s);margin-bottom:16px">{desc}</p>
        <div class="sp">
          <div class="sp-r"><span class="sp-k">Feature</span><span class="sp-v" style="color:var(--ac)">AR Ready</span></div>
        </div>
        <div class="mf" style="margin-top:20px">
          <a href="https://www.fab.com/sellers/Trong%20Tan%20Phan" target="_blank" class="mf-p" style="padding:10px 20px;font-size:13px">Get on Fab</a>
        </div>
      </div>
    </article>
"""

skids_html_list = []
comps_html_list = []

for i, item in enumerate(items):
    src_img = item["src"]
    new_img_name = f"auto_{i}.jpg"
    shutil.copy(src_img, os.path.join(local_img_dir, new_img_name))
    shutil.copy(src_img, os.path.join(target_img_dir, new_img_name))
    item['img_path'] = f"images/{new_img_name}"
    
    if item['is_skid']:
        skids_html_list.append(card_template.format(**item))
    else:
        comps_html_list.append(card_template.format(**item))

def wrap_carousel(cards, section_id):
    return f"""
  <div style="position:relative;margin:0 -20px;padding:0 20px">
    <button class="nav-btn prev-btn" onclick="scrollTrack('{section_id}', -400)" style="position:absolute;left:20px;top:40%;transform:translateY(-50%);z-index:10;background:rgba(255,255,255,0.9);border:1px solid rgba(0,0,0,0.1);width:40px;height:40px;border-radius:50%;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:center;transition:all 0.2s">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </button>
    
    <div class="carousel-track" id="{section_id}" style="display:flex;gap:24px;overflow-x:auto;scroll-snap-type:x mandatory;padding:10px 20px 40px;scrollbar-width:none;-webkit-overflow-scrolling:touch;cursor:grab">
{ "".join(cards) }
    </div>
    
    <button class="nav-btn next-btn" onclick="scrollTrack('{section_id}', 400)" style="position:absolute;right:20px;top:40%;transform:translateY(-50%);z-index:10;background:rgba(255,255,255,0.9);border:1px solid rgba(0,0,0,0.1);width:40px;height:40px;border-radius:50%;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:center;transition:all 0.2s">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>
  </div>
"""

skids_final = wrap_carousel(skids_html_list, "track-skids")
comps_final = wrap_carousel(comps_html_list, "track-comps")

js_logic = """
<script>
function scrollTrack(id, offset) {
  const track = document.getElementById(id);
  track.scrollBy({ left: offset, behavior: 'smooth' });
}

document.querySelectorAll('.carousel-track').forEach(track => {
  let isDown = false;
  let startX;
  let scrollLeft;
  
  track.addEventListener('mousedown', (e) => {
    isDown = true;
    track.style.cursor = 'grabbing';
    startX = e.pageX - track.offsetLeft;
    scrollLeft = track.scrollLeft;
  });
  track.addEventListener('mouseleave', () => {
    isDown = false;
    track.style.cursor = 'grab';
  });
  track.addEventListener('mouseup', () => {
    isDown = false;
    track.style.cursor = 'grab';
  });
  track.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - track.offsetLeft;
    const walk = (x - startX) * 2;
    track.scrollLeft = scrollLeft - walk;
  });
});
</script>
</body>
"""

file_path = r'd:\WT3D_Project\landing_page_v3_master.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace skids grid
content = re.sub(
    r'(<section class="sec" id="systems">.*?<p>.*?</p>\n  </div>).*?(</section>)',
    rf'\1{skids_final}\2',
    content,
    flags=re.DOTALL
)

# Replace equipment grid
content = re.sub(
    r'(<section class="sec sec-dark" id="equipment">.*?<p>.*?</p>\n  </div>).*?(</section>)',
    rf'\1{comps_final}\2',
    content,
    flags=re.DOTALL
)

# Thêm Javascript trước thẻ </body>
if '<script>function scrollTrack' not in content:
    content = content.replace('</body>', js_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully injected accurate titles and interactive carousel!")
