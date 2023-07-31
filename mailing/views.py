from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import request
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from config import settings
from config.settings import EMAIL_HOST_USER
from mailing.forms import MessageForm, ClientForm, MailForm
from mailing.models import Client, Mail, Message
from mailing.services import mail_send


class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:list_letter')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mail, Message, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        context_data['title'] = 'Создание рассылки'

        return context_data
    
    def form_valid(self, form):
        self.object = form.save()
        self.object.mail_status = 'создана'
        self.object.save()

        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        if form.is_valid():
            mail_send(self.object)

        return super().form_valid(form)


class MailListView(ListView):
    model = Mail

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список рассылок'

        return context_data


class MailUpdateView(UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:list_letter')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mail, Message, form=MessageForm)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        context_data['title'] = 'Редактирование рассылки'

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        if form.is_valid():
            mail_send(self.object)

        return super().form_valid(form)


class MailDetailView(DetailView):
    model = Mail

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр рассылки'

        return context_data


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('mailing:list_letter')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление рассылки'

        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_clients')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание клиента'

        return context_data


class ClientListView(ListView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список клиентов'

        return context_data


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр клиента'

        return context_data


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_clients')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление клиента'

        return context_data


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_clients')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Редактирование клиента'

        return context_data



