import os
import requests
import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

SUPABASE_URL = "https://abfqwrkiehthppxxjser.supabase.co"
SUPABASE_KEY = "sb_publishable_HNRw8Yu7J1KVMZCYi6DKUQ_-d9-dBgF"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def scrape_full_catalog(max_pages=30):
    print("🚀 بدء سحب كتالوج الألعاب الضخم...")
    total_added = 0
    
    for page in range(1, max_pages + 1):
        url = f"https://an1.com/games/page/{page}/" if page > 1 else "https://an1.com/games/"
        print(f"📄 جاري سحب الصفحة [{page}]...")
        
        try:
            res = scraper.get(url)
            if res.status_code != 200:
                print(f"⚠️ توقف عند الصفحة {page} (كود الاستجابة: {res.status_code})")
                break
                
            soup = BeautifulSoup(res.text, 'html.parser')
            # البحث عن كافة مربعات الألعاب في الصفحة
            game_cards = soup.find_all('div', class_='item')
            
            if not game_cards:
                print("🏁 اكتمل سحب جميع الألعاب المتاحة.")
                break
                
            for card in game_cards:
                link_tag = card.find('a')
                img_tag = card.find('img')
                
                if link_tag and img_tag:
                    title = img_tag.get('alt', '').strip() or link_tag.text.strip()
                    link = link_tag.get('href', '')
                    icon = img_tag.get('src', '') or img_tag.get('data-src', '')
                    
                    if title and link:
                        data = {
                            "name": title,
                            "icon": icon if icon.startswith('http') else f"https://an1.com{icon}",
                            "download_url": link,
                            "description": f"تحميل لعبة {title} نسخة مهكرة ومعدلة برابط مباشر",
                            "category": "ألعاب مهكرة"
                        }
                        
                        r = requests.post(f"{SUPABASE_URL}/rest/v1/apps", json=data, headers=headers)
                        if r.status_code in [200, 201]:
                            total_added += 1
                            print(f"✅ [{total_added}] تم إضافة: {title}")
                            
        except Exception as e:
            print(f"❌ خطأ أثناء معالجة الصفحة {page}: {e}")

if __name__ == "__main__":
    # يمكن زيادة عدد الصفحات بزيادة الرقم 30
    scrape_full_catalog(max_pages=30)
