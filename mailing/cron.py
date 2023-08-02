from datetime import timedelta

from django.utils.timezone import now

from mailing.models import Mail, Logs
from mailing.services import mail_send


def mail_send_by_time():
    """
    Проверяет необходимость отправки email у всех объектов модели Mail и отправляет его
    """
    mails = Mail.objects.all()
    for mail in mails:
        if mail.periodicity == 'daily':
            if now() - timedelta(days=1) >= mail.last_send:
                mail_send(mail)
        elif mail.periodicity == 'weekly':
            if now() - timedelta(days=7) >= mail.last_send:
                mail_send(mail)
        elif mail.periodicity == 'monthly':
            if now() - timedelta(days=30) >= mail.last_send:
                mail_send(mail)

        if mail.mail_time_to >= now():
            mail.mail_status = 'завершена'



