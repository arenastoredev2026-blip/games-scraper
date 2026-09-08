import os
import requests
import cloudscraper
import xml.etree.ElementTree as ET


# تحميل متغيرات البيئة من ملف .env محلي (اختياري، لا تقم بإضافة .env للمخزن)


scraper = cloudscraper.create_scraper()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_KEY environment variables. Set them in your environment or GitHub Secrets.")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


def sync_games():
    print("🚀 جاري سحب الألعاب وتخطي الحماية...")
    url = "https://an1.com/feed/"
    try:
        response = scraper.get(url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print("فشل في جلب الخلاصة:", e)
        return

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print("فشل في تحليل XML:", e)
        return

    for item in root.findall('.//item'):
        title_el = item.find('title')
        link_el = item.find('link')
        if title_el is None or link_el is None:
            continue
        title = title_el.text or ""
        link = link_el.text or ""
        if not title or not link:
            continue

        data = {
            "name": title,
            "icon": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Picsart_logo.svg/512px-Picsart_logo.svg.png",
            "download_url": link,
            "description": "نسخة مهكرة ومعدلة جاهزة للتحميل",
            "category": "ألعاب مهكرة"
        }

        try:
            res = requests.post(f"{SUPABASE_URL}/rest/v1/apps", json=data, headers=headers, timeout=15)
            res.raise_for_status()
            print(f"تم إضافة: {title}")
        except Exception as e:
            print(f"فشل إضافة {title}:", e)


if __name__ == "__main__":
    sync_games()
