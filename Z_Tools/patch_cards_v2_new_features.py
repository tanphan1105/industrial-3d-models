# patch_cards_v2_new_features.py
# Áp dụng 4 tính năng từ bản mới vào tất cả 21 cards trong master.html:
# 1. AR badge (góc phải ảnh)
# 2. Hover overlay với Fab + CGTrader quick-buy buttons
# 3. CGTrader button song song Fab trong footer card
# 4. Thêm "Formats: OBJ / FBX / GLB" spec row

from bs4 import BeautifulSoup

SRC = r'd:\WT3D_Project\landing_page_v3_master.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
cards = soup.find_all('article', class_='mc')
print(f"Found {len(cards)} cards")

FAB_URL  = "https://www.fab.com/sellers/Trong%20Tan%20Phan"
CGT_URL  = "https://www.cgtrader.com/designers/tanphan1105"

changed = 0
for card in cards:
    mt = card.find('div', class_='mt')
    if not mt:
        continue

    # ── 1. Thêm AR badge nếu chưa có ──
    if not mt.find('div', class_='mt-ar'):
        ar_badge = soup.new_tag('div', attrs={'class': 'mt-ar'})
        ar_badge.string = 'AR'
        mt.append(ar_badge)

    # ── 2. Thêm hover overlay nếu chưa có ──
    if not mt.find('div', class_='mt-hover'):
        hover_div = BeautifulSoup(f'''
        <div class="mt-hover">
          <a href="{FAB_URL}" target="_blank" rel="noopener" class="mt-hover-btn mt-hover-fab">⬡ Fab</a>
          <a href="{CGT_URL}" target="_blank" rel="noopener" class="mt-hover-btn mt-hover-cgt">◈ CGTrader</a>
        </div>''', 'html.parser')
        mt.append(hover_div)

    mb = card.find('div', class_='mb')
    if not mb:
        continue

    # ── 3. Thêm CGTrader button vào .mf nếu chưa có ──
    mf = mb.find('div', class_='mf')
    if mf and not mf.find('a', class_='mf-cgt'):
        # Đổi class nút Fab từ mf-p → mf-fab + thêm nút CGTrader
        fab_btn = mf.find('a', class_='mf-p')
        if fab_btn:
            fab_btn['class'] = ['mf-fab']
            fab_btn.string = '⬡ Fab.com'
        cgt_btn = BeautifulSoup(
            f'<a href="{CGT_URL}" target="_blank" rel="noopener" class="mf-cgt">◈ CGTrader</a>',
            'html.parser')
        mf.append(cgt_btn)

    # ── 4. Thêm Format spec row vào .sp nếu chưa có ──
    sp = mb.find('div', class_='sp')
    if sp and not any('Format' in str(r) for r in sp.find_all('div', class_='sp-r')):
        fmt_row = BeautifulSoup(
            '<div class="sp-r"><span class="sp-k">Formats</span>'
            '<span class="sp-v">OBJ / FBX / GLB</span></div>',
            'html.parser')
        sp.append(fmt_row)

    changed += 1

print(f"Patched {changed} cards")

result = str(soup)
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(result)

print("Done. File saved.")
