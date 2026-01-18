import json
import sys # <--- Add this
from datetime import datetime

STATUS_FILE = 'status.json'
MAX_DAYS = 7

def check_status():
    try:
        with open(STATUS_FILE, 'r') as f:
            data = json.load(f)
            
        last_checkin = datetime.strptime(data['last_checkin'], "%Y-%m-%d")
        delta = datetime.now() - last_checkin
        
        print(f"Days since last check-in: {delta.days}")
        
        if delta.days > MAX_DAYS:
            print("🚨 ALERT: User is unresponsive. Triggering protocol...")
            # This exit code tells GitHub Actions that the job FAILED (Red X)
            sys.exit(1) 
        else:
            print("✅ STATUS: User is active. Standing by.")
            sys.exit(0)
            
    except FileNotFoundError:
        print("Error: Status file not found.")
        sys.exit(1)

if __name__ == "__main__":
    check_status()