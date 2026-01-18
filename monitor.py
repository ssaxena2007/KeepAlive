import json
from datetime import datetime

# Configuration (In the future, these can be Environment Variables)
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
            print("ALERT: User is unresponsive. Triggering protocol...")
            return True # Trigger the switch
        else:
            print("STATUS: User is active. Standing by.")
            return False # Do nothing
            
    except FileNotFoundError:
        print("Error: Status file not found.")

if __name__ == "__main__":
    check_status()