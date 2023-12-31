from smtplib import SMTPException

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from blog.models import Article

from mailing.forms import MessageForm, ClientForm, MailForm
from mailing.models import Client, Mail, Message, Logs
from mailing.services import mail_send, cache_lists


class MailCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление создания рассылки"""
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.add_mail'
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
        self.object.owner = self.request.user

        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        if form.is_valid():
            # отправляет email если текущее время больше времени начала и меньше времени окончания
            if self.object.mail_time_from <= now() <= self.object.mail_time_to:
                mail_send(self.object)
                self.object.mail_status = 'запущена'

            if self.object.mail_time_to <= now():
                self.object.mail_status = 'завершена'

        self.object.save()
        return super().form_valid(form)


class MailListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Представление списка рассылок
    """
    model = Mail
    permission_required = 'mailing.view_mail'

    def get_queryset(self):
        return cache_lists(self, Mail)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список рассылок'

        return context_data


class MailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Представление редактирования рассылки
    """
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.change_mail'
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

        return super().form_valid(form)


class MailDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Представление просмотра одной рассылки
    """
    model = Mail
    permission_required = 'mailing.view_mail'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр рассылки'

        return context_data


class MailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление удаления рассылки
    """
    model = Mail
    success_url = reverse_lazy('mailing:list_letter')
    permission_required = 'mailing.delete_mail'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление рассылки'

        return context_data


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление создания клиента
    """
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.create_client'
    success_url = reverse_lazy('mailing:list_clients')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание клиента'

        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Представления просмотра списка клиентов для каждого пользователя
    """
    model = Client
    permission_required = 'mailing.view_client'

    def get_queryset(self):
        return cache_lists(self, Client)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список клиентов'

        return context_data


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
        Представления просмотра одного клиента
    """
    model = Client
    permission_required = 'mailing.view_client'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр клиента'

        return context_data


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
        Представления удаления клиента
    """
    model = Client
    permission_required = 'mailing.delete_client'
    success_url = reverse_lazy('mailing:list_clients')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление клиента'

        return context_data


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
        Представления редактирования клиента
    """
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.change_client'
    success_url = reverse_lazy('mailing:list_clients')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Редактирование клиента'

        return context_data


def index(request):
    """
    Функция отображения главной страницы
    """
    context = {
        'all_mail': Mail.objects.all().count(),
        'active_mail': Mail.objects.filter(mail_status='запущена').count(),
        'all_clients': Client.objects.all().count(),
        'article_object_list': Article.objects.all().order_by('?')[:3],
        'title': 'Главная'
    }
    return render(request, 'mailing/index.html', context)


class LogsListView(ListView):
    """
        Представления просмотра списка отчетов об отправке для каждой рассылки
    """
    model = Logs

    def get_queryset(self):
        return super().get_queryset().filter(mail_id=self.kwargs.get('pk'))

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Отчеты проведенных рассылок'

        return context_data





