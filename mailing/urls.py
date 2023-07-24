from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import LetterCreateView, LetterListView, LetterUpdateView, LetterDetailView, LetterDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', LetterListView.as_view(), name='list_letter'),
    path('create/', LetterCreateView.as_view(), name='create_letter'),
    path('update/<int:pk>/', LetterUpdateView.as_view(), name='update_letter'),
    path('view_letter/<int:pk>/', LetterDetailView.as_view(), name='view_letter'),
    path('delete_letter/<int:pk>/', LetterDeleteView.as_view(), name='delete_letter'),

]