import os
import requests
import json
from time import sleep
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH_URL = "https://mockapi.obligo.io/auth/token"
SESSION_URL = "https://mockapi.obligo.io/renters/session"
STATUS_URL_TEMPLATE = "https://mockapi.obligo.io/renters/session/{}"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def authenticate():
    print("🔐 Authenticating...")
    response = requests.post(AUTH_URL, json={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })

    if response.status_code == 200:
        token = response.json().get("userSessionToken")
        print("✅ Auth successful.")
        return token
    else:
        raise Exception(f"Auth failed: {response.status_code} → {response.text}")

def start_renter_session(token):
    print("📦 Creating renter session...")
    headers = {"Authorization": f"Bearer {token}"}
    body = {
        "renter_id": "r_789",
        "property_id": "p_456",
        "amount": 2100,
        "currency": "USD"
    }

    response = requests.post(SESSION_URL, headers=headers, json=body)

    if response.status_code == 201:
        session_id = response.json().get("session_id")
        print(f"✅ Session created: {session_id}")
        return session_id
    else:
        raise Exception(f"Session creation failed: {response.status_code} → {response.text}")

def get_session_status(token, session_id):
    print("📡 Polling session status...")
    headers = {"Authorization": f"Bearer {token}"}
    url = STATUS_URL_TEMPLATE.format(session_id)

    for attempt in range(5):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"➡️  Attempt {attempt+1}: {data['status']}")
            if data["status"] == "approved":
                with open("session_status.json", "w") as f:
                    json.dump(data, f, indent=2)
                print("🎉 Session approved and saved to file.")
                return
        sleep(2)

    print("⚠️  Session not approved after 5 attempts.")

if __name__ == "__main__":
    try:
        token = authenticate()
        session_id = start_renter_session(token)
        get_session_status(token, session_id)
    except Exception as e:
        print(f"❌ Error: {e}")
# This script handles the authentication, session creation, and polling for session status