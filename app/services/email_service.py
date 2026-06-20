"""
TARS Contact Form Backend — Email Service

Sends contact form submissions via SMTP (Gmail).
Runs in a background task after the endpoint returns 202.
All exceptions are caught and logged — never fails silently.
"""

import smtplib
from email.mime.text import MIMEText

from app.config import settings
from app.utils.logging import get_logger

logger = get_logger("email_service")


def send_contact_email(name: str, email: str, message: str) -> None:
    """
    Send a contact form submission via SMTP.

    Called as a background task — errors are caught and logged,
    they never bubble up or crash the worker.
    """

    logger.info(
        "[SEND] Sending contact email from %s (%s)",
        name, email,
    )

    try:
        # ── Build the email body ──────────────────────────────
        body = f"""New TARS Contact Form Submission

Name: {name}

Email: {email}

Message:
{message}
"""

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = f"TARS Contact Form — {name}"
        msg["From"] = settings.smtp_sender
        msg["To"] = settings.receiver
        msg["Reply-To"] = email  # so you can reply directly to the sender

        # ── Send via SMTP ─────────────────────────────────────
        _send_smtp(msg)

        logger.info(
            "[OK] Contact email sent successfully (from: %s, to: %s)",
            email, settings.receiver,
        )

    except Exception as exc:
        logger.exception(
            "[FAIL] Failed to send contact email from %s: %s",
            email, exc,
        )


def _send_smtp(msg: MIMEText) -> None:
    """
    Send an email via SMTP using the settings from config.

    Supports STARTTLS (port 587) and direct SSL (port 465).
    Raises on failure so the caller can log the error.
    """
    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    username = settings.SMTP_USERNAME
    password = settings.SMTP_PASSWORD

    if not username or not password:
        raise RuntimeError(
            "SMTP credentials not configured. "
            "Set SMTP_USERNAME and SMTP_PASSWORD in your .env file."
        )

    logger.debug("Connecting to SMTP %s:%d ...", host, port)

    if port == 465:
        # Direct SSL connection
        with smtplib.SMTP_SSL(host, port, timeout=30) as server:
            server.login(username, password)
            server.send_message(msg)
    else:
        # STARTTLS (typically port 587)
        with smtplib.SMTP(host, port, timeout=30) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            server.login(username, password)
            server.send_message(msg)

    logger.debug("SMTP send complete")
