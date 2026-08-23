import os
import time
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail permissions scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def execute_with_retry(request, max_attempts=3, delay=5):
    """Executes a Google API request with automatic retry logic for network timeouts."""
    for attempt in range(1, max_attempts + 1):
        try:
            return request.execute()
        except Exception as e:
            is_timeout = "10060" in str(e) or "timeout" in str(e).lower()
            if is_timeout and attempt < max_attempts:
                print(f"⚠️ Network timeout encountered (Attempt {attempt}/{max_attempts}). Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise e

def get_gmail_service(token_path='token_zia.json'):
    """Handles OAuth authentication for a specific user token with robust refresh retries."""
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Symmetrical token refresh retries to handle socket timeout drops
            for attempt in range(1, 4):
                try:
                    creds.refresh(Request())
                    break
                except Exception as e:
                    is_timeout = "10060" in str(e) or "timeout" in str(e).lower()
                    if is_timeout and attempt < 3:
                        print(f"⚠️ Gmail token refresh timeout (Attempt {attempt}/3). Retrying in 5s...")
                        time.sleep(5)
                    else:
                        # ONLY delete the token on permanent permission errors (e.g. revoked access)
                        # NEVER delete on temporary socket timeout drops!
                        is_permanent_error = "invalid_grant" in str(e).lower() or "unauthorized" in str(e).lower()
                        if is_permanent_error:
                            print(f"❌ Permanent OAuth token invalidation. Removing {token_path}.")
                            if os.path.exists(token_path):
                                os.remove(token_path)
                            creds = None
                        raise e
        
        if not creds:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "Error: credentials.json not found! Please place your Google OAuth "
                    "credentials.json file in the workspace directory."
                )
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            
            account_name = "Zia Khan (Boy)" if "zia" in token_path else "Wahiba Kiran (Girl)"
            print(f"\n========================================================")
            print(f"🔐 AUTHENTICATION REQUIRED FOR: {account_name}")
            print(f"Please sign in with the GMAIL account corresponding to this role.")
            print(f"========================================================\n")
            
            creds = flow.run_local_server(port=0)
            
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    return build('gmail', 'v1', credentials=creds)

def send_email(service, to, subject, body, thread_id=None, reply_to_msg_id=None):
    """Sends an email with automatic retries on network failures."""
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    
    if thread_id and reply_to_msg_id:
        message['In-Reply-To'] = reply_to_msg_id
        message['References'] = reply_to_msg_id

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    payload = {'raw': raw_message}
    
    if thread_id:
        payload['threadId'] = thread_id

    request = service.users().messages().send(userId='me', body=payload)
    try:
        sent_msg = execute_with_retry(request)
        return sent_msg
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

def fetch_thread_messages(service, thread_id):
    """Fetches all messages in a given thread with automatic retries."""
    request = service.users().threads().get(userId='me', id=thread_id)
    try:
        thread = execute_with_retry(request)
        return thread.get('messages', [])
    except Exception as e:
        if "404" in str(e):
            return []
        print(f"Error fetching thread {thread_id}: {e}")
        return []

def get_latest_reply(service, thread_id, my_email):
    """Checks for the latest email reply in the thread with retries."""
    messages = fetch_thread_messages(service, thread_id)
    if not messages:
        return None
    
    for msg in reversed(messages):
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        
        sender = ""
        msg_id_header = ""
        subject = ""
        for h in headers:
            if h['name'].lower() == 'from':
                sender = h['value']
            if h['name'].lower() == 'message-id':
                msg_id_header = h['value']
            if h['name'].lower() == 'subject':
                subject = h['value']
                
        if my_email.lower() not in sender.lower():
            body = ""
            parts = [payload]
            while parts:
                part = parts.pop()
                if 'parts' in part:
                    parts.extend(part['parts'])
                else:
                    mime_type = part.get('mimeType', '')
                    if mime_type == 'text/plain':
                        data = part.get('body', {}).get('data', '')
                        if data:
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                            break
            
            return {
                'id': msg['id'],
                'message_id_header': msg_id_header,
                'sender': sender,
                'subject': subject,
                'body': body.strip()
            }
            
    return None
