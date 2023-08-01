# Generated by Django 4.2.3 on 2023-07-29 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_remove_mail_message_message_mail_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logs',
            name='message',
        ),
        migrations.AddField(
            model_name='logs',
            name='mail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mail', verbose_name='рассылка'),
        ),
    ]
