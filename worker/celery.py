import smtplib
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
from app.settings import Settings

settings = Settings()

celery = Celery(
    __name__,
    broker=settings.CELERY_RABBIT_URL,
    backend="rpc://",
)


@celery.task(name='send_email_task')
def send_email_task(subject: str, text: str, to: str):
    msg = _build_message(subject, text, to)
    _send_email_mailhog(msg)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    msg = MIMEMultipart()

    msg['From'] = settings.MAIL_FROM
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))
    return msg


def _send_email_mailhog(msg: MIMEMultipart) -> None:
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.send_message(msg)
