from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailCreateView, MailListView, MailUpdateView, MailDetailView, \
    MailDeleteView, ClientCreateView, ClientListView, ClientDetailView, ClientDeleteView, \
    ClientUpdateView, index, LogsListView

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(index), name='index'),
    path('list_letter', MailListView.as_view(), name='list_letter'),
    path('create/', MailCreateView.as_view(), name='create_letter'),
    path('<int:pk>/update/', MailUpdateView.as_view(), name='update_letter'),
    path('<int:pk>/view_letter/', MailDetailView.as_view(), name='view_letter'),
    path('<int:pk>/delete_letter/', MailDeleteView.as_view(), name='delete_letter'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('list_clients/', ClientListView.as_view(), name='list_clients'),
    path('<int:pk>/view_client/', ClientDetailView.as_view(), name='view_client'),
    path('<int:pk>/delete_client/', ClientDeleteView.as_view(), name='delete_client'),
    path('<int:pk>/update_client/', ClientUpdateView.as_view(), name='update_client'),
    path('<int:pk>/list_logs/', LogsListView.as_view(), name='list_logs'),

]