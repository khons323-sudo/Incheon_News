import os
import requests
import feedparser
import json

RSS_URL = "https://news.google.com/rss/search?q=영종도+남북동&hl=ko&gl=KR&ceid=KR:ko"
STATE_FILE = "last_goyang_scrap.json"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def load_sent_links():
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            # 구버전 호환: {"link": "..."} 형식도 처리
            if isinstance(data, dict) and "links" in data:
                return set(data["links"])
            elif isinstance(data, dict) and "link" in data:
                return {data["link"]}
    except:
        pass
    return set()

def save_sent_links(links: set):
    with open(STATE_FILE, "w") as f:
        json.dump({"links": list(links)}, f, ensure_ascii=False, indent=2)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

# 이미 보낸 링크 목록 불러오기
sent_links = load_sent_links()

feed = feedparser.parse(RSS_URL)

new_entries = [e for e in feed.entries if e.link not in sent_links]

# 오래된 기사부터 순서대로 전송 (시간순)
for entry in reversed(new_entries):
    send_telegram(f"🗞️ 새 기사: {entry.title}\n{entry.link}")
    sent_links.add(entry.link)

if new_entries:
    save_sent_links(sent_links)
    print(f"{len(new_entries)}개 새 기사 전송 완료")
else:
    print("새 기사 없음")
