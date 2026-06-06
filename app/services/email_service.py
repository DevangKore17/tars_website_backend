import logging
import smtplib
from email.message import EmailMessage
from app.core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    RECEIVER_EMAIL
)

logger = logging.getLogger(__name__)

def send_contact_email(name: str, email: str, message: str):
    try:
        msg = EmailMessage()
        msg["Subject"] = "New Contact Form Submission"
        msg["From"] = EMAIL_USER
        msg["To"] = RECEIVER_EMAIL

        msg.set_content(
            f"""
Name: {name}
Email: {email}

Message:
{message}
"""
        )

        with smtplib.SMTP_SSL(
            SMTP_SERVER,
            SMTP_PORT
        ) as server:
            server.login(
                EMAIL_USER,
                EMAIL_PASSWORD
            )

            server.send_message(msg)

        logger.info(
            f"Contact email sent successfully from {email}"
        )

    except Exception as e:
        logger.error(
            f"Failed to send contact email from {email}: {e}"
        )