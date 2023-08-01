# Generated by Django 4.2.3 on 2023-07-24 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_remove_client_mail_client_email_client_letter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='letter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to='mailing.letter'),
        ),
    ]
