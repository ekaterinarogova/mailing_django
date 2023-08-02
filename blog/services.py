from django.conf import settings
from django.core.cache import cache

from blog.models import Article


def cache_articles():
    """
    Кеширует список статей
    :return: список статей
    """
    if settings.CACHE_ENABLED:
        key = 'article_list'
        article_list = cache.get(key)
        if article_list is None:
            article_list = Article.objects.all()
            cache.set(key, article_list)
    else:
        article_list = Article.objects.all()

    return article_list
