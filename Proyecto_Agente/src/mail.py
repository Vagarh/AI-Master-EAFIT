import os
import smtplib
from email.message import EmailMessage

def send_email(to_addr, subject, body):
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    pwd  = os.getenv("SMTP_PASS")
    port = int(os.getenv("SMTP_PORT", "587"))
    if not all([host,user,pwd,to_addr]): return False
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(host, port) as s:
        s.starttls()
        s.login(user, pwd)
        s.send_message(msg)
    return True
