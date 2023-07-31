from django import forms

from mailing.models import Mail, Client, Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('theme', 'body',)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'


class MailForm(forms.ModelForm):

    class Meta:
        model = Mail
        exclude = ('mail_status', )
        clients = forms.ModelMultipleChoiceField(queryset=Client.objects.all())
