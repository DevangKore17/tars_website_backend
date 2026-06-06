from email.mime.text import MIMEText
import smtplib

from app.core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    RECEIVER_EMAIL
)


def send_contact_email(
    name: str,
    email: str,
    message: str
):

    body = f"""
New TARS Contact Form Submission

Name: {name}

Email: {email}

Message:
{message}
"""

    msg = MIMEText(body)

    msg["Subject"] = "TARS Website Contact Form"
    msg["From"] = EMAIL_USER
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL(
    SMTP_SERVER,
    SMTP_PORT
) as server:

        server.login(
        EMAIL_USER,
        EMAIL_PASSWORD
        )

        server.send_message(msg)