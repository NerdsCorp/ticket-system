import secrets
import base64

def generate_ticket_code(length=12):
    raw = secrets.token_bytes(length)
    code = base64.urlsafe_b64encode(raw).decode('utf-8').rstrip('=')
    return code[:16]