from django import forms

from mailing.models import Letter, Client


class LetterForm(forms.ModelForm):

    class Meta:
        model = Letter
        fields = ('theme', 'body',)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

