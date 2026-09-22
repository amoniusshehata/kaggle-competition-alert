import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

LOOKBACK_HOURS = 25


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


def parse_date(value):
    if not value:
        return None
    value = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(value)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "disable_web_page_preview": True},
        timeout=30,
    )
    response.raise_for_status()


def main():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=LOOKBACK_HOURS)

    competitions = get_competitions()
    new_items = []

    for c in competitions:
        created = parse_date(c.get("dateCreated") or c.get("created"))
        if created and cutoff <= created <= now:
            new_items.append(c)

    # Remove duplicate refs while preserving order.
    seen = set()
    new_items = [c for c in new_items if not (c.get("ref") in seen or seen.add(c.get("ref")))]

    if not new_items:
        print("No new Kaggle competitions found.")
        return

    lines = ["🚨 New Kaggle Competition(s)", ""]
    for c in new_items:
        ref = c.get("ref", "unknown")
        title = c.get("title") or ref
        reward = c.get("reward") or "Not specified"
        deadline = c.get("deadline") or "Not specified"
        link = f"https://www.kaggle.com/competitions/{ref}"

        lines.extend([
            f"🏆 {title}",
            f"💰 Prize: {reward}",
            f"📅 Deadline: {deadline}",
            f"🔗 {link}",
            "",
        ])

    send_telegram("\n".join(lines))
    print(f"Sent {len(new_items)} competition alert(s).")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
