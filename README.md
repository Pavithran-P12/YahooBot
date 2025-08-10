# YahooBot
---

```markdown
# 📬 Email Attachment Forwarder to Telegram

This Python application connects to a Yahoo Mail inbox, downloads the latest email attachment from a specified folder, and forwards it to a Telegram chat using the Telegram Bot API. It is designed to run as a scheduled cron job on [Render.com](https://render.com).

---

## 🚀 Features

- ✅ Connects securely to Yahoo Mail via IMAP  
- 📂 Downloads the latest attachment from a specific folder (`B2b`)  
- 📤 Sends the attachment to a Telegram chat or group  
- 🧾 Logs each step for easy debugging  
- 🕒 Designed for automated execution via cron job  

---

## 🛠️ Technologies Used

- Python 3  
- `imaplib` for email access  
- `email` for parsing MIME messages  
- `requests` for Telegram API communication  
- `dotenv` for local environment variable management  

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/email-to-telegram.git
cd email-to-telegram
```

### 2. Create a `.env` File (for local testing)

```ini
EMAIL_USER=your_yahoo_email@example.com
EMAIL_PASS=your_yahoo_app_password
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id_or_group_id
```

> ⚠️ Use a Yahoo **App Password** instead of your regular password for IMAP access.

---

## 🧑‍💻 Local Testing

Run the script manually to verify functionality:

```bash
python script.py
```

You should see logs indicating connection to Yahoo Mail, attachment download, and Telegram API response.

---

## ☁️ Deploying on Render.com

### Step 1: Create a New Cron Job

- Go to [Render Cron Jobs](https://dashboard.render.com/new/cron)  
- Choose **Python** as the runtime  
- Set the schedule using cron syntax (e.g., `0 * * * *` for hourly)

### Step 2: Upload Your Code

- Upload your script (`script.py`)  
- Include a `requirements.txt` with:

  ```txt
  requests
  python-dotenv
  ```

### Step 3: Set Environment Variables

In the **Environment** section of the cron job setup:

- `EMAIL_USER`  
- `EMAIL_PASS`  
- `TELEGRAM_TOKEN`  
- `TELEGRAM_CHAT_ID`  

> These should match the values you used locally, but you don’t need the `.env` file on Render.

### Step 4: Confirm and Deploy

- Save and deploy the cron job  
- Check logs after the first scheduled run to confirm success

---

## 🧪 Troubleshooting

- **No logs?** Add `print()` statements to trace execution.  
- **No attachment sent?** Check folder name (`B2b`) and email structure.  
- **Telegram error?** Ensure the bot is not blocked and has permission to send messages.

---

Once you've saved it as `README.md`, you can upload it to GitHub or share it as needed. Want help creating a GitHub repo structure for this project too?
