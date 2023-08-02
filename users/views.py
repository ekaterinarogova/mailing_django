from django.conf import settings
from django.contrib.auth.models import Group

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserForm
from users.models import User


class UserLoginView(LoginView):
    """Представление входа пользователя """
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    """Представление выхода пользователя """
    pass


class UserRegisterView(CreateView):
    """
    Представление регистрации пользователя
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()

        if form.is_valid():
            send_mail(
                'Поздравляем с регистрацией',
                f'Вы зарегистрированы на нашем сайте.',
                settings.EMAIL_HOST_USER,
                [self.object.email],
                fail_silently=False,
            )
            # наделяем пользователя правами группы обычных пользователей
            group = Group.objects.get(name='ordinary')
            self.object.groups.add(group)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Регистрация на сайте'

        return context_data

