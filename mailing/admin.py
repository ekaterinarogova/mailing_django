from django.contrib import admin

from mailing.models import Mail, Client, Message


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    list_filter = ('first_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'body', 'mail_settings',)
    list_filter = ('theme',)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('mail_time_from', 'mail_time_to', 'mail_status')
    list_filter = ('mail_time_from', 'mail_time_to',)

