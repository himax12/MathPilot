import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_delete_session():
    print("Testing Session Deletion...")
    
    # 1. Create a new session to ensure we have something to delete
    try:
        print("Creating new session...")
        resp = requests.post(f"{BASE_URL}/api/sessions/new")
        if resp.status_code != 200:
            print(f"FAILED to create session: {resp.text}")
            return
        
        session_id = resp.json().get("session_id")
        print(f"Created session: {session_id}")
        
    except Exception as e:
        print(f"FAILED to connect to server: {e}")
        return

    # 2. Delete the session
    try:
        print(f"Deleting session {session_id}...")
        resp = requests.delete(f"{BASE_URL}/api/sessions/{session_id}")
        
        if resp.status_code == 200:
            print("Successfully deleted session.")
        else:
            print(f"FAILED to delete session. Status: {resp.status_code}, Response: {resp.text}")
            return
            
    except Exception as e:
        print(f"Error during deletion: {e}")
        return

    # 3. Verify it's gone from list (optional, but good practice)
    try:
        print("Verifying session is gone from list...")
        resp = requests.get(f"{BASE_URL}/api/sessions")
        sessions = resp.json()
        
        found = any(s['session_id'] == session_id for s in sessions)
        if not found:
            print("VERIFIED: Session no longer exists in list.")
        else:
            print("FAILED: Session still exists in list!")
            
    except Exception as e:
        print(f"Error checking list: {e}")

if __name__ == "__main__":
    test_delete_session()
