
from django.views.generic import ListView, DetailView

from blog.models import Article
from blog.services import cache_articles


class ArticleListView(ListView):
    """
        Представления просмотра списка статей в блоге
    """
    model = Article

    def get_queryset(self):
        return cache_articles()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список статей'

        return context_data


class ArticleDetailView(DetailView):
    """
        Представления просмотра одной статьи
    """
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1  # счетчик просмотра статьи
        self.object.save()

        return self.object

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = self.object.title

        return context_data

