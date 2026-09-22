import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Keep True for the current test. Set to False after confirming the test.
TEST_MODE = True
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


def competition_url(ref):
    if not ref:
        return ""
    if ref.startswith("http://") or ref.startswith("https://"):
        return ref
    return f"https://www.kaggle.com/competitions/{ref}"


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
        ref = c.get("ref", "")
        title = c.get("title") or ref
        reward = c.get("reward") or "Not specified"
        deadline = c.get("deadline") or "Not specified"

        message = (
            " Kaggle Alert TEST\n\n"
            " Latest Competition\n"
            f" {title}\n"
            f" Prize: {reward}\n"
            f" Deadline: {deadline}\n"
            f" {competition_url(ref)}\n\n"
            f" Test time (UTC): {datetime.now(timezone.utc):%Y-%m-%d %H:%M}"
        )
        send_telegram(message)
        print(f"TEST: sent latest competition: {ref}")
        return

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=LOOKBACK_HOURS)
    new_items = []

    for c in competitions:
        raw_date = c.get("dateCreated") or c.get("created")
        if not raw_date:
            continue
        try:
            created = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

        if cutoff <= created <= now:
            new_items.append(c)

    if not new_items:
        print("No new Kaggle competitions found.")
        return

    lines = [" New Kaggle Competition(s)", ""]
    for c in new_items:
        ref = c.get("ref", "")
        lines.extend([
            f" {c.get('title') or ref}",
            f" Prize: {c.get('reward') or 'Not specified'}",
            f" Deadline: {c.get('deadline') or 'Not specified'}",
            f" {competition_url(ref)}",
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
