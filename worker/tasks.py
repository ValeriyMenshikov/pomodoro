from celery import shared_task
import smtplib
from email.mime.text import MIMEText

@shared_task
def send_email_task(email):
    msg = MIMEText('Welcome!')
    msg['Subject'] = 'Welcome'
    msg['From'] = 'your_email@example.com'
    msg['To'] = email

    with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
        server.login('your_email@example.com', 'your_password')
        server.sendmail('your_email@example.com', [email], msg.as_string())


