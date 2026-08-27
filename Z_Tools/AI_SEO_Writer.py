import sys
import os
import json
import urllib.request
import urllib.error

def main():
    if len(sys.argv) < 3:
        print("Usage: python AI_SEO_Writer.py <input.txt> <output.txt>")
        sys.exit(1)
        
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    
    with open(in_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
        
    if not text:
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("")
        sys.exit(0)

    # Đọc Key DeepSeek bảo mật từ file .env của Sếp
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
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("ENGINEERING SPECIFICATIONS & NOTES:\n• " + text.replace("\n", "\n• "))
        sys.exit(1)
    
    prompt = f"""
You are an elite B2B mechanical sales engineer for industrial CAD assets.
Your goal is to parse the user's brief notes (often in Vietnamese) about a mechanical design or industrial system, and transform them into a HIGHLY PROFESSIONAL, accurate, and appealing English bulleted list for a 3D CAD model description.

Raw Input Notes:
{text}

Instructions:
1. Translate all Vietnamese technical terms to standard B2B English terminology (e.g., 'inox 304' -> '304 Stainless Steel', 'bơm' -> 'Pump', 'tủ điện' -> 'Control Panel', etc.).
2. Format the output as a clean bulleted list starting each line with '• '.
3. Add professional flair, implying high precision and industrial grade (e.g. Instead of just "Has a pump", say "Integrated high-performance industrial pump module").
4. At the very end of your response, leave one blank line, then generate a comma-separated list of exactly 15 highly-targeted SEO tags (suitable for YouTube, CGTrader, and Fab). Include tags like #3DModel, #CAD, #Engineering, #Industrial, and specific equipment terms. Start the tags section with 'TAGS: '.
5. DO NOT OUTPUT ANY CONVERSATIONAL TEXT. JUST EXACTLY RETURN THE BULLETED TEXT AND THE TAGS.
"""

    url = 'https://api.deepseek.com/v1/chat/completions'
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional B2B translation and copywriting assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
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
        response = urllib.request.urlopen(req, timeout=15)
        response_data = json.loads(response.read().decode('utf-8'))
        output_txt = response_data['choices'][0]['message']['content'].strip()
        
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("ENGINEERING SPECIFICATIONS & HIGHLIGHTS:\n" + output_txt + "\n")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        # Fallback to pure copy if error
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("ENGINEERING SPECIFICATIONS & NOTES:\n• " + text.replace("\n", "\n• "))

if __name__ == "__main__":
    main()
