from django.core.mail import send_mail
from django.utils.timezone import now

from config import settings


def mail_send(item):
    if item.mail_time_from <= now() <= item.mail_time_to:
        send_mail(
            item.message.theme,
            item.message.body,
            settings.EMAIL_HOST_USER,
            [i.email for i in item.clients.all()],
        )