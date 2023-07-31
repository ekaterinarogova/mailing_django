import datetime

from django.db import models

from django.utils.timezone import now

# now = datetime.datetime.now()


class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(verbose_name='email', null=True)
    comments = models.TextField(verbose_name='комментарии', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mail(models.Model):
    PERIODS = [
        ('@daily', 'раз в день',),
        ('@weekly', 'раз в неделю',),
        ('@monthly', 'раз в месяц',),
    ]

    mail_time_from = models.DateTimeField(verbose_name='рассылка с ', default=now)
    mail_time_to = models.DateTimeField(verbose_name='рассылка по', default=now)
    periodicity = models.CharField(max_length=20, verbose_name='периодичность', choices=PERIODS)
    mail_status = models.CharField(max_length=50, verbose_name='статус отправки')
    clients = models.ManyToManyField(Client, verbose_name='получатели')

    def __str__(self):
        return f"{self.message} - {self.mail_status}"

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'


class Message(models.Model):
    theme = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    mail_settings = models.OneToOneField(Mail, verbose_name='рассылка', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.theme}"

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Logs(models.Model):
    mail = models.ForeignKey(Mail, verbose_name='сообщение', on_delete=models.CASCADE)
    last_try = models.DateTimeField(verbose_name='последняя отправка', auto_now=True)
    status = models.CharField(max_length=50, verbose_name='статус попытки')
    server_answer = models.SmallIntegerField(verbose_name='ответ сервера', blank=True, null=True)

    def __str__(self):
        return f"{self.message} - {self.status}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
