import smtplib
from email.message import EmailMessage
from typing import List

from celery import Celery

from src.api.schemas import ShowUser
from src.settings import settings

celery_app = Celery("tasks", broker=settings.REDIS_URL)


def get_email_template_dashboard(value: List[ShowUser]) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Value"
    email["From"] = settings.SMTP_USER
    email["To"] = settings.SMTP_USER  # сам себе отправляю
    email.set_content(f"<div><p>{value}</p></div>", subtype="html")
    return email


@celery_app.task
def send_email_report_dashboard(value: List[ShowUser]):
    email = get_email_template_dashboard(value)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
