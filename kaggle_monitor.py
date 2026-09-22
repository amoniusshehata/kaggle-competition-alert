import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# TEST MODE: send the newest Kaggle competition every time the workflow runs.
# Set to False after the Telegram test succeeds.
TEST_MODE = True


def get_competitions():
    cmd = [
        "kaggle", "competitions", "list",
        "--sort-by", "recentlyCreated",
        "--page-size", "100",
        "--format", "json",
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data if isinstance(data, list) else data.get("competitions", [])


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "disable_web_page_preview": True},
        timeout=30,
    )
    response.raise_for_status()


def main():
    competitions = get_competitions()

    if not competitions:
        print("No Kaggle competitions returned.")
        return

    if TEST_MODE:
        c = competitions[0]
        ref = c.get("ref", "unknown")
        title = c.get("title") or ref
        reward = c.get("reward") or "Not specified"
        deadline = c.get("deadline") or "Not specified"
        link = f"https://www.kaggle.com/competitions/{ref}"

        message = (
            "🧪 Kaggle Alert TEST\n\n"
            "🏆 Latest Competition\n"
            f"📌 {title}\n"
            f"💰 Prize: {reward}\n"
            f"📅 Deadline: {deadline}\n"
            f"🔗 {link}\n\n"
            f"🕐 Test time (UTC): {datetime.now(timezone.utc):%Y-%m-%d %H:%M}"
        )
        send_telegram(message)
        print(f"TEST: sent latest competition: {ref}")
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
