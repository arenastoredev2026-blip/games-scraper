import os
import requests
import cloudscraper
import feedparser

scraper = cloudscraper.create_scraper()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://abfqwrkiehthppxxjser.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_HNRw8Yu7J1KVMZCYi6DKUQ_-d9-dBgF")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def sync_games():
    print("🚀 جاري جلب الألعاب...")
    url = "https://an1.com/feed/"
    response = scraper.get(url)
    
    print(f"📡 حالة استجابة موقع الألعاب: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ فشل فتح الموقع، كود الاستجابة: {response.status_code}")
        return

    # تحليل البيانات باستخدام feedparser المرنة مع الـ RSS
    feed = feedparser.parse(response.content)
    print(f"📦 تم العثور على {len(feed.entries)} لعبة في القائمة")

    for entry in feed.entries:
        title = entry.get('title', 'بدون عنوان')
        link = entry.get('link', '')

        data = {
            "name": title,
            "icon": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Picsart_logo.svg/512px-Picsart_logo.svg.png",
            "download_url": link,
            "description": "نسخة مهكرة ومعدلة جاهزة للتحميل",
            "category": "ألعاب مهكرة"
        }

        res = requests.post(f"{SUPABASE_URL}/rest/v1/apps", json=data, headers=headers)
        
        if res.status_code in [200, 201]:
            print(f"✅ تم إضافة: {title}")
        else:
            print(f"❌ فشل إضافة [{title}] - السبب: ({res.status_code}) {res.text}")

if __name__ == "__main__":
    sync_games()
