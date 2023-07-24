
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing.forms import LetterForm, ClientForm
from mailing.models import Client, Letter


class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy('mailing:list_letter')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ClientFormset = inlineformset_factory(Letter, Client, form=ClientForm, extra=1)
        context_data['formset'] = ClientFormset()

        context_data['title'] = 'Создание рассылки'

        return context_data


class LetterListView(ListView):
    model = Letter

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список рассылок'

        return context_data


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy('mailing:list_letter')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ClientFormset = inlineformset_factory(Letter, Client, form=ClientForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ClientFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ClientFormset(instance=self.object)

        context_data['title'] = 'Редактирование рассылки'

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)



class LetterDetailView(DetailView):
    model = Letter

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр рассылки'

        return context_data


class LetterDeleteView(DeleteView):
    model = Letter
    success_url = reverse_lazy('mailing:list_letter')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление рассылки'

        return context_data






