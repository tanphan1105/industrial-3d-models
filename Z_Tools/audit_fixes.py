import re

file_path = r'd:\WT3D_Project\landing_page_v3_master.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Thêm Gradient đậm xíu cho Hero
hero_css = r"""
.hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  height: calc(100svh - 140px);
  min-height: 500px;
  background: radial-gradient(ellipse at center top, #ffffff 0%, #dcdce2 100%);
}
"""
content = re.sub(
    r'\.hero\s*\{\s*position:\s*relative;\s*display:\s*flex;\s*align-items:\s*center;\s*justify-content:\s*center;\s*overflow:\s*hidden;\s*height:\s*calc\(100svh - 140px\);\s*min-height:\s*500px;\s*\}',
    hero_css.strip(),
    content
)

# 2. Xóa thẻ Article "New folder"
content = re.sub(
    r'<article class="mc rv"[^>]*>.*?New folder.*?</article>',
    '',
    content,
    flags=re.DOTALL
)

# 3. Xóa đuôi .iam
content = content.replace("Transparent Plastic Disc Filter 2 Inch Male Thread.iam", "Transparent Plastic Disc Filter 2 Inch Male Thread")

# 4. Sửa 22+ thành 20+
content = content.replace('<div class="m-stat-n">22+</div>', '<div class="m-stat-n">20+</div>')

# 5. Cập nhật Footer Menu
old_footer_menu = """
      <ul>
        <li><a href="#systems">RO Skid 30 m³/h</a></li>
        <li><a href="#systems">RO Skid 10 m³/h</a></li>
        <li><a href="#systems">Filtration Skid</a></li>
        <li><a href="#equipment">Ozone Generator</a></li>
        <li><a href="#equipment">HP Pump</a></li>
        <li><a href="#equipment">Membrane Housing</a></li>
      </ul>
"""

new_footer_menu = """
      <ul>
        <li><a href="#systems">RO System Packages</a></li>
        <li><a href="#systems">Ozone Generators</a></li>
        <li><a href="#equipment">Membrane Housings</a></li>
        <li><a href="#equipment">Filter Housings</a></li>
        <li><a href="#equipment">Tanks & Valves</a></li>
      </ul>
"""
content = content.replace(old_footer_menu.strip(), new_footer_menu.strip())

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Executed all audit fixes and styling updates successfully.")
