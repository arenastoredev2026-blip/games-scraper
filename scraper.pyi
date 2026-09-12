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

def scrape_full_catalog(max_pages=5):
    # خلينا التطبيقات في الأول عشان تتسحب وتظهر معاك بسرعة
    sections = [
        {"path": "apps", "category": "تطبيقات معدلة", "desc_prefix": "تطبيق"},
        {"path": "games", "category": "ألعاب مهكرة", "desc_prefix": "لعبة"}
    ]
    
    total_added = 0
    
    for section in sections:
        print(f"\n🚀 بدء سحب كتالوج {section['category']}...")
        
        for page in range(1, max_pages + 1):
            # تحديد الرابط بناءً على القسم (تطبيقات أو ألعاب)
            url = f"https://an1.com/{section['path']}/page/{page}/" if page > 1 else f"https://an1.com/{section['path']}/"
            print(f"📄 جاري سحب الصفحة [{page}] من قسم {section['category']}...")
            
            try:
                res = scraper.get(url)
                if res.status_code != 200:
                    print(f"⚠️ توقف عند الصفحة {page} (كود الاستجابة: {res.status_code})")
                    break
                    
                soup = BeautifulSoup(res.text, 'html.parser')
                # البحث عن كافة مربعات التطبيقات/الألعاب في الصفحة
                cards = soup.find_all('div', class_='item')
                
                if not cards:
                    print(f"🏁 اكتمل سحب جميع الـ {section['category']} المتاحة في هذا القسم.")
                    break
                    
                for card in cards:
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
                                "description": f"تحميل {section['desc_prefix']} {title} نسخة مهكرة ومعدلة برابط مباشر",
                                "category": section['category']
                            }
                            
                            r = requests.post(f"{SUPABASE_URL}/rest/v1/apps", json=data, headers=headers)
                            if r.status_code in [200, 201]:
                                total_added += 1
                                print(f"✅ [{total_added}] تم إضافة: {title} ({section['category']})")
                                
            except Exception as e:
                print(f"❌ خطأ أثناء معالجة الصفحة {page} من قسم {section['category']}: {e}")

if __name__ == "__main__":
    # محددين 5 صفحات بس عشان نجرب، ولما تتأكد إنها شغالة ممكن تخليها 30 أو 50 براحتك
    scrape_full_catalog(max_pages=5)
