from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('list_article', ArticleListView.as_view(), name='list_article'),
    path('view_article/<int:pk>/', ArticleDetailView.as_view(), name='view_article'),

]