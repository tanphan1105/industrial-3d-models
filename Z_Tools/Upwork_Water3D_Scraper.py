import feedparser
import time
import json
import os
import sys
from datetime import datetime

# Sửa lỗi in Emoji trên Windows console
sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# B2B UPWORK RSS SCRAPER - WATER TREATMENT & 3D NICHE
# ==============================================================================
# Hướng dẫn lấy Link RSS từ Upwork:
# 1. Lên Upwork tìm kiếm với từ khóa: (water OR filtration OR treatment) AND (3d OR render OR webgl OR animation)
# 2. Bấm vào nút RSS (icon sóng WiFi) để lấy link.
# 3. Dán link đó vào biến UPWORK_RSS_URL bên dưới.

UPWORK_RSS_URL = "https://www.upwork.com/ab/feed/jobs/rss?q=%28water+OR+filtration+OR+treatment%29+AND+%283d+OR+render+OR+webgl+OR+animation%29"

# Bộ lọc từ khóa Vàng (Chỉ báo những Job chứa ít nhất 1 từ trong này)
TARGET_KEYWORDS = [
    "water treatment", "water filtration", "purification", "reverse osmosis",
    "3d render", "3d video", "webgl", "three.js", "threejs", 
    "blender", "industrial equipment", "water plant", "cad to 3d", "product animation"
]

# Đảm bảo file json lưu cùng thư mục với script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEEN_JOBS_FILE = os.path.join(SCRIPT_DIR, "seen_jobs.json")

# Thông tin Bot Telegram (Sếp điền vào để nhận thông báo về điện thoại)
TELEGRAM_BOT_TOKEN = "os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")"
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen_jobs(seen_jobs):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(seen_jobs, f)

def send_telegram_alert(job_title, job_link, budget):
    """Gửi tin báo động về điện thoại Sếp qua Telegram"""
    if TELEGRAM_BOT_TOKEN == "ĐIỀN_TOKEN_BOT_VÀO_ĐÂY":
        return # Bỏ qua nếu Sếp chưa cấu hình Telegram
    
    import requests
    msg = f"🚨 **CÓ JOB 3D NGÀNH NƯỚC MỚI!**\n\n📌 Tiêu đề: {job_title}\n💰 Ngân sách: {budget}\n🔗 Link Apply: {job_link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def check_upwork():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang rình Job trên Upwork...")
    
    try:
        feed = feedparser.parse(UPWORK_RSS_URL)
        seen_jobs = load_seen_jobs()
        new_jobs_found = 0

        for entry in feed.entries:
            job_id = entry.link
            
            # Bỏ qua nếu job này đã quét rồi
            if job_id in seen_jobs:
                continue

            title = entry.title.lower()
            summary = entry.description.lower()
            
            # Quét xem có đúng ngách Lọc nước / 3D không
            is_target_niche = any(kw in title or kw in summary for kw in TARGET_KEYWORDS)
            
            if is_target_niche:
                # Trích xuất thử ngân sách hoặc giá theo giờ nếu có trong description
                budget = "Thỏa thuận / Chưa rõ"
                if "<b>Budget</b>:" in entry.description:
                    budget_start = entry.description.find("<b>Budget</b>:") + 14
                    budget_end = entry.description.find("<br />", budget_start)
                    budget = f"Fixed: {entry.description[budget_start:budget_end].strip()}"
                elif "<b>Hourly Range</b>:" in entry.description:
                    hourly_start = entry.description.find("<b>Hourly Range</b>:") + 20
                    hourly_end = entry.description.find("<br />", hourly_start)
                    budget = f"Hourly: {entry.description[hourly_start:hourly_end].strip()}"

                print("\n=============================================")
                print(f"🔥 CÓ CON MỒI MỚI: {entry.title}")
                print(f"💰 Ngân sách: {budget}")
                print(f"🔗 Link: {entry.link}")
                print("=============================================\n")
                
                # Bắn thông báo Telegram
                send_telegram_alert(entry.title, entry.link, budget)
                
                seen_jobs.append(job_id)
                new_jobs_found += 1

        if new_jobs_found > 0:
            save_seen_jobs(seen_jobs)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã tìm thấy {new_jobs_found} job mới!")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Chưa có job mới. Tiếp tục rình rập...")

    except Exception as e:
        print(f"Lỗi cào dữ liệu: {e}")

if __name__ == "__main__":
    print("🚀 KHỞI ĐỘNG CỖ MÁY SĂN JOB 3D NGÀNH NƯỚC (UPWORK) 🚀")
    print("Bot sẽ tự động quét 15 phút một lần...")
    
    while True:
        check_upwork()
        # Nghỉ 15 phút (900 giây) rồi quét tiếp để tránh bị Upwork chặn IP
        time.sleep(900)
