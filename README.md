# 🏆 Kaggle Competition Alert

A simple GitHub Actions bot that checks Kaggle competitions once a day and sends new competition alerts to Telegram.

Your computer does **not** need to stay on.

## ✨ Features

- 🔎 Checks Kaggle competitions automatically.
- ⏰ Runs every day at **7:00 AM Egypt time**.
- 📱 Sends notifications to Telegram.
- 🔐 Uses GitHub Secrets for credentials.
- ☁️ Runs completely in GitHub Actions.

## 🚀 How it works

```text
Kaggle → GitHub Actions → Python → Telegram Bot → 📱 Telegram
```

# 🛠️ Setup

## 1. Fork the repository

Open:

https://github.com/amoniusshehata/kaggle-competition-alert

Click **Fork → Create fork**.

Now you have your own copy.

## 2. Create a Kaggle API token

Go to:

https://www.kaggle.com/settings

Open the **API** section and create an API token.

You will use it as:

`KAGGLE_API_TOKEN`

Never put the token inside the Python code.

## 3. Create a Telegram bot

In Telegram, open **@BotFather**.

Send:

`/start`

Then:

`/newbot`

Follow the instructions.

BotFather will give you a **Bot Token**.

You will use it as:

`TELEGRAM_BOT_TOKEN`

Never publish this token.

## 4. Get your Telegram Chat ID

Open your new bot and send:

`/start`

Then obtain your Telegram Chat ID using your preferred Telegram bot/API method.

It will normally be a numeric value such as:

```text
123456789
```

You will use it as:

`TELEGRAM_CHAT_ID`

## 🔐 5. Add the 3 GitHub Secrets

In **your forked repository** go to:

**Settings → Secrets and variables → Actions → New repository secret**

Create exactly these three secrets:

| Secret | Value |
|---|---|
| `KAGGLE_API_TOKEN` | Your Kaggle API token |
| `TELEGRAM_BOT_TOKEN` | Token from BotFather |
| `TELEGRAM_CHAT_ID` | Your Telegram Chat ID |

The workflow reads them securely:

```yaml
${{ secrets.KAGGLE_API_TOKEN }}
${{ secrets.TELEGRAM_BOT_TOKEN }}
${{ secrets.TELEGRAM_CHAT_ID }}
```

### ⚠️ Never commit secrets

Do not put tokens in:

- `kaggle_monitor.py`
- workflow files
- `README.md`
- public GitHub issues
- commits

## ▶️ 6. Test the workflow

Go to:

**Actions → Daily Kaggle Competition Alert**

Click:

**Run workflow**

If the setup is correct, the workflow should finish successfully and Telegram should receive a message.

## 🧪 Test mode

The project currently has:

```python
TEST_MODE = True
```

In test mode, a manual workflow run sends the **latest Kaggle competition**.

This lets you verify the complete pipeline:

```text
Kaggle API
   ↓
GitHub Actions
   ↓
Python script
   ↓
Telegram
```

After confirming that the Telegram message is correct, change:

```python
TEST_MODE = False
```

and commit the change.

## ⏰ Daily schedule

The workflow runs every day at:

**07:00 AM Egypt time (UTC+3)**

GitHub Actions uses UTC, so the current cron expression is:

```yaml
cron: "0 4 * * *"
```

That means:

```text
04:00 UTC
07:00 Egypt time
```

> GitHub Actions cron is UTC. If Egypt's UTC offset changes, the local execution time can change accordingly.

To change the schedule, edit:

`.github/workflows/kaggle-alert.yml`

## 📁 Project structure

```text
kaggle-competition-alert/
│
├── .github/
│   └── workflows/
│       └── kaggle-alert.yml
│
├── kaggle_monitor.py
├── requirements.txt
└── README.md
```

### kaggle_monitor.py

The main Python program. It gets competitions from Kaggle and sends Telegram notifications.

### kaggle-alert.yml

Defines when GitHub Actions runs the monitor.

### requirements.txt

Contains the required Python packages.

## 🔒 Security

If your Telegram bot token is accidentally exposed, revoke/regenerate it through BotFather immediately.

Never reuse a leaked token.

## 🐛 Troubleshooting

### Telegram does not receive a message

Check:

1. The bot token is correct.
2. The chat ID is correct.
3. You sent `/start` to the bot.
4. All three GitHub Secrets were created in the correct repository.
5. The workflow completed successfully.

### Kaggle authentication error

Check that `KAGGLE_API_TOKEN` contains a valid Kaggle API token.

### Automatic schedule does not run

Check:

**Actions → Daily Kaggle Competition Alert**

and make sure GitHub Actions is enabled.

You can always use **Run workflow** for a manual test.

## ⭐ Customize it

You can modify the project to:

- change the notification time;
- filter competitions;
- change the Telegram message;
- send to a Telegram group;
- add additional notification channels;
- run the checker more frequently.

---

Made with **Python + Kaggle API + GitHub Actions + Telegram Bot API**.
