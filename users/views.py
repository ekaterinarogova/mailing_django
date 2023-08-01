from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserForm, CodeForm
from users.models import User
from users.services import create_code


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            send_mail(
                    'Регистрация',
                    f'Поздравляем с регистрацией на нашем сайте',
                    settings.EMAIL_HOST_USER,
                    [self.object.email]
                )

            group = Group.objects.get(name='ordinary')
            self.object.groups.add(group)
        return super().form_valid(form)


# def registration_confirm(request):
#     if request.method == 'POST':
#         form = CodeForm
#         code = request.session['key']
#         code_user = form.cleaned_data.get('code')
#
#         if str(code_user) == code:
#             return redirect('users/login')
#         else:
#             messages.error(request, 'Неверный код')
#
#     return render(request, 'users/confirm_registration.html')


