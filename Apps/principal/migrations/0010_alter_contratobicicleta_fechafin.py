# Generated by Django 3.2.4 on 2021-08-17 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0009_auto_20210817_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratobicicleta',
            name='fechafin',
            field=models.DateTimeField(db_column='fechafin', default=datetime.datetime(2021, 8, 19, 9, 42, 47, 565886)),
        ),
    ]
