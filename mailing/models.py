
from django.conf import settings
from django.db import models

from django.utils.timezone import now


class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(verbose_name='email', null=True)
    comments = models.TextField(verbose_name='комментарии', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='владелец', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mail(models.Model):
    PERIODS = [
        ('daily', 'раз в день',),
        ('weekly', 'раз в неделю',),
        ('monthly', 'раз в месяц',),
    ]

    mail_time_from = models.DateTimeField(verbose_name='рассылка с ', default=now)
    mail_time_to = models.DateTimeField(verbose_name='рассылка по', default=now)
    periodicity = models.CharField(max_length=20, verbose_name='периодичность', choices=PERIODS)
    mail_status = models.CharField(max_length=50, verbose_name='статус отправки')
    clients = models.ManyToManyField(Client, verbose_name='получатели')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='владелец', on_delete=models.SET_NULL, null=True)
    last_send = models.DateTimeField(verbose_name='последняя отправка', auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.message} - {self.mail_status}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = [
            ('set_status', 'Can set mail status')
        ]


class Message(models.Model):
    theme = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    mail_settings = models.OneToOneField(Mail, verbose_name='рассылка', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.theme}"

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class LogsManager(models.Manager):
    def create_log(self, mail, status, last_try=now(), server_answer=None):
        log = self.create(mail=mail, status=status, last_try=last_try, server_answer=server_answer)

        return log


class Logs(models.Model):
    mail = models.ForeignKey(Mail, verbose_name='сообщение', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, verbose_name='статус попытки')
    last_try = models.DateTimeField(verbose_name='последняя отправка')
    server_answer = models.SmallIntegerField(verbose_name='ответ сервера', blank=True, null=True)

    objects = LogsManager()

    def __str__(self):
        return f"{self.message} - {self.status}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'



