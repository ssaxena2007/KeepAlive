import json
import sys
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

STATUS_FILE = 'status.json'
MAX_DAYS = 7

def send_alert():
    sender = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')
    receiver = os.environ.get('TARGET_EMAIL')
    secret = os.environ.get('SECRET_PAYLOAD')

    if not all([sender, password, receiver, secret]):
        print("Error: Missing environment variables for email.")
        return

    subject = "🚨 ALERT: Dead Man's Switch Triggered"
    body = f"This is an automated message.\n\nThe user has been inactive for over {MAX_DAYS} days.\n\nHERE IS THE ATTACHED PAYLOAD:\n----------------\n{secret}\n----------------"

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
    try:
        with open(STATUS_FILE, 'r') as f:
            data = json.load(f)
            
        last_checkin = datetime.strptime(data['last_checkin'], "%Y-%m-%d")
        delta = datetime.now() - last_checkin
        
        print(f"Days since last check-in: {delta.days}")
        
        if delta.days > MAX_DAYS:
            print("🚨 ALERT: User is unresponsive. Sending protocol...")
            send_alert()
            sys.exit(1) 
        else:
            print("✅ STATUS: User is active. Standing by.")
            sys.exit(0)
            
    except FileNotFoundError:
        print("Error: Status file not found.")
        sys.exit(1)

if __name__ == "__main__":
    check_status()