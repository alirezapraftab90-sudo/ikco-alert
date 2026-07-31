import os
import requests
from bs4 import BeautifulSoup
import hashlib

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://esale.ikco.ir"

STATE_FILE = "last_hash.txt"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)


def get_page_hash():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers, timeout=30)

    soup = BeautifulSoup(r.text, "html.parser")

    # حذف بخش‌هایی که معمولاً تغییرات بی‌اهمیت دارند
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)

    return hashlib.sha256(text.encode()).hexdigest()


def main():

    new_hash = get_page_hash()

    old_hash = ""

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            old_hash = f.read().strip()

    if old_hash and old_hash != new_hash:
        send_message(
            "🚗 احتمال تغییر در سایت ایران خودرو وجود دارد.\n\n"
            "سایت را بررسی کن:\n"
            "https://esale.ikco.ir"
        )

    with open(STATE_FILE, "w") as f:
        f.write(new_hash)


if __name__ == "__main__":
    main()
