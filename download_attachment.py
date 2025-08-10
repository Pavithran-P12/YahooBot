import os
import imaplib
import email
import requests
from dotenv import load_dotenv

# Load .env file if running locally
load_dotenv()

# Environment variables
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.mail.yahoo.com")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(file_path):
    """Send the downloaded attachment to Telegram."""
    print(f"Sending file to Telegram: {file_path}")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as file:
            response = requests.post(
                url,
                data={"chat_id": TELEGRAM_CHAT_ID},
                files={"document": file}
            )
        print(f"Telegram Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def download_latest_unread_attachment():
    """Connect to Yahoo Mail and process the latest unread email with attachment."""
    print("Cron job started.")

    # Check environment variables
    if not all([EMAIL_USER, EMAIL_PASS, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        print("Missing one or more required environment variables.")
        return

    try:
        print("Connecting to IMAP server...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)

        status, _ = mail.select("B2b")
        print(f"Select folder status: {status}")
        if status != "OK":
            print("Failed to select folder 'B2b'")
            return

        result, data = mail.search(None, "UNSEEN")
        if result != "OK":
            print("Failed to search for unread emails.")
            return

        mail_ids = data[0].split()
        print(f"Found {len(mail_ids)} unread emails.")
        if not mail_ids:
            print("No unread emails found.")
            return

        latest_email_id = mail_ids[-1]
        print(f"Fetching unread email ID: {latest_email_id.decode()}")

        result, data = mail.fetch(latest_email_id, "(RFC822)")
        if result != "OK":
            print("Failed to fetch email.")
            return

        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        for part in email_message.walk():
            content_type = part.get_content_type()
            disposition = part.get_content_disposition()
            print(f"Checking part: {content_type}, disposition: {disposition}")

            if disposition == "attachment":
                filename = part.get_filename()
                if filename:
                    file_path = os.path.join("/tmp", filename)
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Downloaded attachment: {filename}")

                    if os.path.exists(file_path):
                        print(f"File saved at: {file_path}")
                        send_to_telegram(file_path)

                        # Mark email as read
                        mail.store(latest_email_id, '+FLAGS', '\\Seen')
                        print("Email marked as read.")
                    else:
                        print("File not saved!")
                    break
        else:
            print("No attachment found in the unread email.")

        mail.logout()
        print("IMAP session closed.")
    except Exception as e:
        print(f"Error during email processing: {e}")

if __name__ == "__main__":
    download_latest_unread_attachment()
