# Generated by Django 4.2.3 on 2023-07-31 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0013_alter_message_mail_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='mail_settings',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mailing.mail', verbose_name='рассылка'),
        ),
    ]
