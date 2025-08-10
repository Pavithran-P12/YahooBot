import os
import imaplib
import email
import requests
from dotenv import load_dotenv

# Load .env file if running locally (ignored on Render if ENV vars are set)
load_dotenv()

# Environment variables
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.mail.yahoo.com")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(file_path):
    """Send the downloaded attachment to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID}, files={"document": file})
    print(f"Telegram Response: {response.text}")

def download_latest_attachment():
    """Connect to Yahoo Mail and download the latest attachment."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        if result != "OK":
            print("No messages found!")
            return

        mail_ids = data[0].split()
        latest_email_id = mail_ids[-1]

        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        for part in email_message.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                if filename:
                    file_path = os.path.join("/tmp", filename)  # /tmp works on Render
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Downloaded attachment: {filename}")
                    send_to_telegram(file_path)
                    break

        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_latest_attachment()
