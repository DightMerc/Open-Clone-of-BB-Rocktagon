# Generated by Django 2.1.7 on 2019-03-16 07:53

import api.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190316_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=api.fields.IntegerRangeField(verbose_name='Рейтинг'),
        ),
    ]
