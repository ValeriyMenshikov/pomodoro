import smtplib
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
from app.settings import Settings

settings = Settings()

celery = Celery(__name__)

celery.conf.broker_url = settings.CELERY_REDIS_URL
celery.conf.result_backend = settings.CELERY_REDIS_URL


# app.conf.update(
#     result_backend='redis://localhost:6379/0',
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='Europe/London',
#     enable_utc=True,
# )

@celery.task(name='send_email_task')
def send_email_task(subject: str, text: str, to: str):
    msg = _build_message(subject, text, to)
    _send_email(msg)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    msg = MIMEMultipart()

    msg['From'] = settings.MAIL_FROM
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))
    return msg


def _send_email(msg: MIMEMultipart) -> None:
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context)
    server.login(settings.MAIL_FROM, settings.SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()