import sys
import os
import json
import urllib.request
import urllib.error
from datetime import datetime

def main():
    if len(sys.argv) < 3:
        print("Usage: python DeepSeek_Metadata_5Version.py <ModelName> <OutputDir> [Dimensions]")
        sys.exit(1)
        
    model_name = sys.argv[1]
    out_dir = sys.argv[2]
    dimensions = sys.argv[3] if len(sys.argv) > 3 else "N/A"
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    out_file = os.path.join(out_dir, "Z_DeepSeek_Metadata_Dashboard.html")
    
    # Read API Key
    api_key = ""
    env_path = r"C:\Users\ADMIN\.env"
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as ef:
            for line in ef:
                if line.startswith("DEEPSEEK_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    
    if not api_key:
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        
    if not api_key:
        print("ERROR: Không tìm thấy DEEPSEEK_API_KEY trong .env")
        sys.exit(1)
    
    prompt = f"""
You are an elite B2B mechanical engineering copywriter and SEO expert. 
Your task is to generate highly engaging, unique metadata (Titles, Descriptions, Tags) for an industrial 3D model.

Model Name Base (Vietnamese or English): {model_name}
Dimensions: {dimensions}

Generate EXACTLY 6 blocks of JSON data. Return ONLY valid JSON format. Do not use Markdown JSON tags like ```json.
The JSON must have the following keys:
"cgtrader": {{"title": "...", "description": "...", "tags": "..."}}
"yt_cinematic": {{"title": "...", "description": "...", "tags": "..."}}
"yt_xray": {{"title": "...", "description": "...", "tags": "..."}}
"short_v1": {{"title": "...", "description": "...", "tags": "..."}}
"short_v2": {{"title": "...", "description": "...", "tags": "..."}}
"short_macro": {{"title": "...", "description": "...", "tags": "..."}}

Guidelines:
- "cgtrader": Focus on exact specs, geometry, industrial use-case, and why it's worth buying for engineering.
- "yt_cinematic": Long-form YT video (16:9). Epic, slow paced. Focus on "Cinematic Walkthrough" and B2B sales pitch.
- "yt_xray": Long-form YT video (16:9). Focus on "Internal anatomy", "Wireframe breakdown", "Reverse Engineering".
- "short_v1": 9:16 Shorts. Fast action. Title must pop (e.g. "Epic Industrial Design 🔥"). Include "#Shorts".
- "short_v2": 9:16 Shorts. Hyper cuts, Kamikaze dive. Title e.g. "Insane Engineering 🚀". Include "#Shorts".
- "short_macro": 9:16 Shorts. Super close-up details. Title e.g. "Perfect CAD Details 💎". Include "#Shorts".

For descriptions in YouTube/Shorts, ALWAYS include this hook at the end:
"Get the native 3D source files here 👇
🔗 CGTrader: https://www.cgtrader.com/designers/tanphan1105
🔗 Fab: https://www.fab.com/sellers/Trong%20Tan%20Phan"

Output pure JSON.
"""

    url = 'https://api.deepseek.com/v1/chat/completions'
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional JSON generator. Return ONLY raw JSON without any markdown formatting."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    )

    try:
        response = urllib.request.urlopen(req, timeout=45)
        response_data = json.loads(response.read().decode('utf-8'))
        output_txt = response_data['choices'][0]['message']['content'].strip()
        
        # Strip markdown if AI leaked it
        if output_txt.startswith("```json"):
            output_txt = output_txt[7:]
        if output_txt.startswith("```"):
            output_txt = output_txt[3:]
        if output_txt.endswith("```"):
            output_txt = output_txt[:-3]
            
        seo_data = json.loads(output_txt)
        
        # Build HTML Dashboard
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>MAXSKILLS 5-VISION METADATA</title>
<style>
body {{ font-family: 'Segoe UI', Tahoma, Arial, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }}
h1 {{ color: #58a6ff; text-align: center; margin-bottom: 2px; }}
h3.subtitle {{ color: #8b949e; text-align: center; margin-top: 5px; margin-bottom: 30px; }}
.card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
.c-cg {{ border-left: 4px solid #f9826c; }}
.c-yt {{ border-left: 4px solid #ff0000; }}
.c-sh {{ border-left: 4px solid #bb86fc; }}
h2 {{ font-size: 18px; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-top:0; }}
.c-cg h2 {{ color: #f9826c; }}
.c-yt h2 {{ color: #ff0000; }}
.c-sh h2 {{ color: #bb86fc; }}
h3 {{ color: #8b949e; font-size: 13px; margin-top: 15px; text-transform: uppercase; letter-spacing: 1px; }}
.data-box {{ background: #010409; padding: 15px; border-radius: 6px; font-family: monospace; white-space: pre-wrap; font-size: 14px; border: 1px solid #21262d; position: relative; margin-top: 5px; }}
.copy-btn {{ position: absolute; top: 10px; right: 10px; background: #238636; color: white; border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: bold; transition: 0.2s; }}
.copy-btn:hover {{ background: #2ea043; }}
</style>
<script>
function copyText(btn, id) {{
    var text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text);
    var old = btn.innerText; btn.innerText = 'Copied!';
    setTimeout(() => {{ btn.innerText = old; }}, 2000);
}}
</script>
</head><body>
<h1>🤖 DEEPSEEK B2B METADATA ENGINE</h1>
<h3 class="subtitle">Model: {model_name} | Size: {dimensions}</h3>
"""
        # Formatter helper
        def make_block(key, title, css_class):
            if key not in seo_data: return ""
            d = seo_data[key]
            d_title = d.get('title', '')
            d_desc = d.get('description', '')
            
            # --- MỎ NEO TÀI CHÍNH & KIẾM TIỀN (MONETIZATION SUITE) ---
            music_credit = ""
            if key == 'yt_cinematic':
                music_credit = "🎵 Music provided by Infraction No Copyright Music\nSpotify: https://spoti.fi/3D18oVw\n(Monetization Safe)"
            elif key == 'yt_xray':
                music_credit = "🎵 Music by Karl Casey @ White Bat Audio\nLicense: Royalty Free & Copyright Free"
            elif key == 'short_v1':
                music_credit = "🎵 Music provided by NoCopyrightSounds (NCS).\nFree Download / Stream: http://ncs.io"
            elif key in ['short_v2', 'short_macro']:
                music_credit = "🎵 Audio licensed via YouTube Audio Library / FreeSound CC0"
            
            b2b_sales_hook = f"""
==============================
📥 DOWNLOAD NATIVE 3D CAD FILES:
💎 CGTrader Pro Assets: https://www.cgtrader.com/designers/tanphan1105
💎 Fab Store: https://www.fab.com/sellers/Trong%20Tan%20Phan

🤝 FOR BUSINESS & CUSTOM ENGINEERING:
Require custom industrial layouts, P&ID, or 3D animations?
📧 Email: trongtan.p@icloud.com
📞 WhatsApp/Zalo: +84985267326

⭐ Support the channel by Subscribing for more elite mechanical designs!
{music_credit}
=============================="""
            
            d_desc = d_desc.replace("Get the native 3D source files here 👇", "").replace("🔗 CGTrader: https://www.cgtrader.com/designers/tanphan1105", "").replace("🔗 Fab: https://www.fab.com/sellers/Trong%20Tan%20Phan", "").strip()
            
            d_desc += "\n\n" + b2b_sales_hook
            
            d_tags = d.get('tags', '')
            return f"""
<div class="card {css_class}">
    <h2>{title}</h2>
    <h3>Title (Under 60 Chars)</h3>
    <div class="data-box"><button class="copy-btn" onclick="copyText(this, 't_{key}')">Copy</button><span id="t_{key}">{d_title}</span></div>
    <h3>Description & Tags</h3>
    <div class="data-box"><button class="copy-btn" onclick="copyText(this, 'd_{key}')">Copy</button><span id="d_{key}">{d_desc}\n\nTAGS:\n{d_tags}</span></div>
</div>"""

        html += make_block('cgtrader', '🛒 CGTRADER / FAB.COM (SALES PAGE)', 'c-cg')
        html += make_block('yt_cinematic', '🎞️ YOUTUBE 1: CINEMATIC WALKTHROUGH (16:9)', 'c-yt')
        html += make_block('yt_xray', '🎞️ YOUTUBE 2: TECHNICAL X-RAY (16:9)', 'c-yt')
        html += make_block('short_v1', '📱 SHORTS 1: SUPERCAR V1 (FAST CUT)', 'c-sh')
        html += make_block('short_v2', '📱 SHORTS 2: SUPERCAR V2 (HYPER CUT)', 'c-sh')
        html += make_block('short_macro', '📱 SHORTS 3: MACRO FOCUS (DETAIL)', 'c-sh')

        html += "</body></html>"
        
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"SUCCESS: Đã tạo file {out_file}")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
