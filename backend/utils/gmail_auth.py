from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import threading
import time

# Minimal scopes for AI email assistant
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",  # Read emails
    "https://www.googleapis.com/auth/gmail.send",     # Send emails
]

# Global lock for OAuth flow
oauth_lock = threading.Lock()
oauth_in_progress = False
oauth_completed = False

def get_gmail_service():
    global oauth_in_progress, oauth_completed
    
    creds = None
    
    # Check for existing token file
    token_path = "token.json"
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            if creds and creds.valid:
                return build("gmail", "v1", credentials=creds)
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(token_path, "w") as token:
                        token.write(creds.to_json())
                    return build("gmail", "v1", credentials=creds)
                except Exception:
                    creds = None
        except Exception:
            creds = None
    
    # Need to re-authorize
    with oauth_lock:
        # Check again after acquiring lock
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
                if creds and creds.valid:
                    return build("gmail", "v1", credentials=creds)
            except Exception:
                pass
        
        if oauth_in_progress:
            # Wait for OAuth to complete
            for _ in range(60):  # Wait up to 60 seconds
                time.sleep(1)
                if os.path.exists(token_path):
                    try:
                        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
                        if creds and creds.valid:
                            return build("gmail", "v1", credentials=creds)
                    except Exception:
                        continue
            raise Exception("OAuth timeout")
        
        oauth_in_progress = True
        try:
            # Remove old token if corrupted
            if os.path.exists(token_path):
                os.remove(token_path)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(
                port=9000,
                prompt="consent",
                access_type="offline",
            )
            
            if creds:
                with open(token_path, "w") as token:
                    token.write(creds.to_json())
                oauth_completed = True
        finally:
            oauth_in_progress = False
    
    if not creds:
        raise Exception("Failed to get Gmail credentials")
    
    service = build("gmail", "v1", credentials=creds)
    return service
