import requests
import cloudscraper
import xml.etree.ElementTree as ET

scraper = cloudscraper.create_scraper()

SUPABASE_URL = "https://abfqwrkiehthppxxjser.supabase.co"
SUPABASE_KEY = "sb_publishable_HNRw8Yu7J1KVMZCYi6DKUQ_-d9-dBgF"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def sync_games():
    print("🚀 جاري سحب الألعاب وتخطي الحماية...")
    url = "https://an1.com/feed/"
    response = scraper.get(url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            
            data = {
                "name": title,
                "icon": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Picsart_logo.svg/512px-Picsart_logo.svg.png",
                "download_url": link,
                "description": "نسخة مهكرة ومعدلة جاهزة للتحميل",
                "category": "ألعاب مهكرة"
            }
            
            res = requests.post(f"{SUPABASE_URL}/rest/v1/apps", json=data, headers=headers)
            print(f"تم إضافة: {title}")

if __name__ == "__main__":
    sync_games()
