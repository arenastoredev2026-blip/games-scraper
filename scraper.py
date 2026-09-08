import os
import requests
import cloudscraper
import xml.etree.ElementTree as ET

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

    try:
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        print(f"📦 تم العثور على {len(items)} لعبة في القائمة")

        for item in items:
            title = item.find('title').text if item.find('title') is not None else "بدون عنوان"
            link = item.find('link').text if item.find('link') is not None else ""

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
                print(f"❌ فشل إضافة [{title}] - السبب من Supabase: ({res.status_code}) {res.text}")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء تحليل البيانات: {e}")

if __name__ == "__main__":
    sync_games()
