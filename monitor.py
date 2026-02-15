import os
import requests
import feedparser
import json

RSS_URL = "https://news.google.com/rss/search?q=영종도+남북동&hl=ko&gl=KR&ceid=KR:ko"
STATE_FILE = "last_goyang_scrap.json"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_last_link():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("link")
    except:
        return None

def save_last(link):
    with open(STATE_FILE, "w") as f:
        json.dump({"link": link}, f)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

feed = feedparser.parse(RSS_URL)
latest = feed.entries[0]
last_link = get_last_link()

if latest.link != last_link:
    send_telegram(f"🗞️ 새 기사: {latest.title}\n{latest.link}")
    save_last(latest.link)


