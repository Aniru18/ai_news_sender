from fastmcp import FastMCP
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from mcp_servers.mail_server.auth import get_credentials

mcp = FastMCP("gmail-mcp")

def get_service():
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)

# =========================
# TOOL 1: List Emails
# =========================
def list_emails_logic(max_results: int = 10, query: str = ""):
    """
    List emails with basic info.
    
    Args:
        max_results: Number of emails to return (default: 10)
        query: Gmail search query (e.g., "is:unread", "from:user@example.com")
    """
    service = get_service()
    
    params = {
        "userId": "me",
        "maxResults": max_results
    }
    if query:
        params["q"] = query
    
    results = service.users().messages().list(**params).execute()
    messages = results.get("messages", [])
    
    # Get details for each message
    email_list = []
    for msg in messages:
        detail = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()
        
        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        
        email_list.append({
            "id": msg["id"],
            "threadId": msg["threadId"],
            "from": headers.get("From", "Unknown"),
            "subject": headers.get("Subject", "(No Subject)"),
            "date": headers.get("Date", "Unknown")
        })
    
    return email_list

@mcp.tool()
def list_emails(max_results: int = 10, query: str = ""):
    """
    List emails from Gmail inbox.
    
    Args:
        max_results: Number of emails to return (default: 10)
        query: Gmail search query (e.g., "is:unread", "from:user@example.com", "subject:meeting")
    
    Returns:
        List of emails with id, from, subject, and date
    """
    return list_emails_logic(max_results, query)

# =========================
# TOOL 2: Read Email
# =========================
def get_email_logic(message_id: str):
    """Get full email content including body"""
    service = get_service()
    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()
    
    # Extract headers
    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    
    # Extract body
    def get_body(payload):
        if "body" in payload and "data" in payload["body"]:
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    if "data" in part["body"]:
                        return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                # Recursively check nested parts
                body = get_body(part)
                if body:
                    return body
        return ""
    
    body = get_body(msg.get("payload", {}))
    
    return {
        "id": msg["id"],
        "threadId": msg["threadId"],
        "from": headers.get("From", "Unknown"),
        "to": headers.get("To", "Unknown"),
        "subject": headers.get("Subject", "(No Subject)"),
        "date": headers.get("Date", "Unknown"),
        "body": body,
        "snippet": msg.get("snippet", "")
    }

@mcp.tool()
def get_email(message_id: str):
    """
    Get full email content by message ID.
    
    Args:
        message_id: The Gmail message ID
    
    Returns:
        Email details including from, to, subject, date, and body
    """
    return get_email_logic(message_id)

# =========================
# TOOL 3: Send Email
# =========================
def send_email_logic(to: str, subject: str, body: str):
    """Send an email"""
    service = get_service()
    
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    
    sent = service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()
    
    return {
        "id": sent["id"],
        "threadId": sent["threadId"],
        "message": f"Email sent successfully to {to}"
    }

@mcp.tool()
def send_email(to: str, subject: str, body: str):
    """
    Send an email via Gmail.
    
    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body text
    
    Returns:
        Confirmation with message ID
    """
    return send_email_logic(to, subject, body)

# =========================
# TOOL 4: Search Emails
# =========================
@mcp.tool()
def search_emails(query: str, max_results: int = 10):
    """
    Search emails using Gmail search syntax.
    
    Args:
        query: Gmail search query (examples: "is:unread", "from:boss@company.com", 
               "subject:invoice", "has:attachment", "after:2024/01/01")
        max_results: Number of results to return
    
    Returns:
        List of matching emails
    """
    return list_emails_logic(max_results, query)

# =========================
# Testing & Server
# =========================
if __name__ == "__main__":
    # For testing:
    print("=== Testing list_emails ===")
    emails = list_emails_logic(3)
    for email in emails:
        print(f"\nFrom: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
    
    # To run MCP server, uncomment:
    # mcp.run()