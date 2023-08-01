from django.core.cache import cache
from django.core.mail import send_mail
from config import settings


def mail_send(item):
    send_mail(
        item.message.theme,
        item.message.body,
        settings.EMAIL_HOST_USER,
        [i.email for i in item.clients.all()],
    )


def cache_lists(object_, model):
    if settings.CACHE_ENABLED:
        key = f'{model}_list'
        object_list = cache.get(key)
        if object_list is None:
            object_list = model.objects.filter(owner=object_.request.user)
            cache.set(key, object_list)
    else:
        object_list = model.objects.filter(owner=object_.request.user)

    return object_list
