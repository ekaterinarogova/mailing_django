# Generated by Django 4.2.3 on 2023-08-01 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0017_alter_mail_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='last_try',
            field=models.DateTimeField(verbose_name='последняя отправка'),
        ),
    ]
