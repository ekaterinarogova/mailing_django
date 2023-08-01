from django.utils.timezone import now

from mailing.models import Mail
from mailing.services import mail_send


def mail_send_by_time():
    mails = Mail.objects.all()
    for mail in mails:
            mail_send(mail)
