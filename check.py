import os
import time
import hashlib
import requests
from bs4 import BeautifulSoup


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://customer.ikco.ir/circular/"

HASH_FILE = "last_hash.txt"
STATUS_FILE = "last_status.txt"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=data, timeout=20)


def get_page_hash():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def send_status_if_needed():

    now = time.time()

    last_status = 0

    if os.path.exists(STATUS_FILE):

        with open(STATUS_FILE, "r") as f:
            last_status = float(f.read().strip())


    if now - last_status >= 1800:

        send_message(
            "🤖 وضعیت ربات ایران خودرو\n\n"
            "✅ بررسی سایت انجام شد\n"
            "❌ بخشنامه جدیدی پیدا نشد.\n\n"
            "ربات فعال است."
        )

        with open(STATUS_FILE, "w") as f:
            f.write(str(now))


def main():

    try:

        new_hash = get_page_hash()

        old_hash = ""

        if os.path.exists(HASH_FILE):

            with open(HASH_FILE, "r") as f:
                old_hash = f.read().strip()


        if old_hash and old_hash != new_hash:

            send_message(
                "🚗 تغییر جدید در بخشنامه‌های ایران خودرو پیدا شد!\n\n"
                "لینک بررسی:\n"
                f"{URL}"
            )


        with open(HASH_FILE, "w") as f:
            f.write(new_hash)


        send_status_if_needed()


    except Exception as e:

        send_message(
            "⚠️ خطا در بررسی سایت ایران خودرو:\n\n"
            f"{e}"
        )


if __name__ == "__main__":
    main()
