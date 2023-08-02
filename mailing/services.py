from smtplib import SMTPException

from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.timezone import now

from config import settings
from mailing.models import Logs


def mail_send(item):
    """
    Отправляет рассылку списку клиентов и формирует отчет об отправки как объект модели Logs
    :param item: объект рассылки
    """
    try:
        send_mail(
            item.message.theme,
            item.message.body,
            settings.EMAIL_HOST_USER,
            [i.email for i in item.clients.all()],
        )
        item.last_send = now()
        Logs.objects.create_log(item, 'отправлена')
    except SMTPException as e:
        Logs.objects.create_log(item, 'не отправлена', now(), e.args[0])
        return SMTPException("Что то пошло не так, попробуем еще раз чуть позже")


def cache_lists(object_, model):
    """
    Кеширует список объектов
    :param object_: объект класса модели
    :param model: класс модели
    :return: список объектов
    """
    if settings.CACHE_ENABLED:
        key = f'{model}_list'
        object_list = cache.get(key)
        if object_list is None:
            object_list = model.objects.filter(owner=object_.request.user)
            cache.set(key, object_list)
    else:
        object_list = model.objects.filter(owner=object_.request.user)

    return object_list
