import os
import sys
import smtplib
import subprocess
from email.mime.text import MIMEText
from datetime import datetime, timezone

# Configuration
MAX_DAYS = 7

def get_last_commit_time():
    """
    Asks Git: 'What is the timestamp of the last commit?'
    Returns a datetime object in UTC.
    """
    try:
        # git show -s --format=%ct HEAD gives the unix timestamp of the last commit
        commit_ts = subprocess.check_output(
            ['git', 'show', '-s', '--format=%ct', 'HEAD']
        ).decode('utf-8').strip()
        
        # Convert unix timestamp to datetime object
        return datetime.fromtimestamp(int(commit_ts), timezone.utc)
    except Exception as e:
        print(f"Error getting git history: {e}")
        sys.exit(1)

def send_alert(days_inactive):
    sender = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')
    receiver = os.environ.get('TARGET_EMAIL')
    secret = os.environ.get('SECRET_PAYLOAD')

    if not all([sender, password, receiver, secret]):
        print("Error: Missing environment variables for email.")
        return

    subject = "🚨 ALERT: Dead Man's Switch Triggered"
    body = (f"This is an automated message.\n\n"
            f"The user has been inactive for {days_inactive} days (Threshold: {MAX_DAYS}).\n\n"
            f"HERE IS THE ATTACHED PAYLOAD:\n----------------\n{secret}\n----------------")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Alert email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def check_status():
    last_commit = get_last_commit_time()
    current_time = datetime.now(timezone.utc)
    
    delta = current_time - last_commit
    days_inactive = delta.days
    
    print(f"🕒 Last Commit: {last_commit}")
    print(f"🕒 Current Time: {current_time}")
    print(f"⏳ Days Inactive: {days_inactive}")

    if days_inactive > MAX_DAYS:
        print("🚨 ALERT: Threshold exceeded. Triggering protocol...")
        send_alert(days_inactive)
        sys.exit(1) # Fail the action so it turns RED
    else:
        print("✅ STATUS: User is active. Standing by.")
        sys.exit(0)

if __name__ == "__main__":
    check_status()