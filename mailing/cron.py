from datetime import timedelta
from smtplib import SMTPException

from django.utils.timezone import now

from mailing.models import Mail, Logs
from mailing.services import mail_send


def mail_send_by_time():
    mails = Mail.objects.all()
    for mail in mails:
        try:
            if mail.periodicity == 'daily':
                if now() - timedelta(days=1) >= mail.last_send:
                    mail_send(mail)
                    mail.last_send = now()
                    Logs.objects.create_log(mail, 'отправлена')
            elif mail.periodicity == 'weekly':
                if now() - timedelta(days=7) >= mail.last_send:
                    mail_send(mail)
                    mail.last_send = now()
                    Logs.objects.create_log(mail, 'отправлена')
            elif mail.periodicity == 'monthly':
                if now() - timedelta(days=30) >= mail.last_send:
                    mail_send(mail)
                    mail.last_send = now()
                    Logs.objects.create_log(mail, 'отправлена')
        except SMTPException as e:
            Logs.objects.create_log(mail, 'не отправлена', now(), e.args[0])
            return SMTPException("Сообщение не отправлено, попробуем еще раз")

