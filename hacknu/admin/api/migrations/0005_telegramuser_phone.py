# Generated by Django 2.1.7 on 2019-03-16 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190316_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='phone',
            field=models.PositiveIntegerField(default=0, unique=True, verbose_name='Номер телефона'),
        ),
    ]
