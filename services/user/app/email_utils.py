import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM

logger = logging.getLogger(__name__)


async def send_password_reset_email(to_email: str, reset_link: str):
    subject = "Reset your Luxe Garments password"
    body = f"""Hi,

We received a request to reset your Luxe Garments password.

Click the link below to set a new password (expires in 1 hour):

{reset_link}

If you didn't request this, you can safely ignore this email.

— Luxe Garments
"""
    if not SMTP_HOST:
        logger.warning("SMTP not configured. Password reset link: %s", reset_link)
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.attach(MIMEText(body, "plain"))

    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASS,
        start_tls=True,
    )
