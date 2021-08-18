# Generated by Django 3.2.3 on 2021-08-17 13:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_auto_20210816_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='tipo',
            field=models.IntegerField(choices=[[0, 'Petición'], [1, 'Queja'], [2, 'Reclamo'], [3, 'Denuncias'], [4, 'Sugerencias'], [5, 'Felicitación']], null=True),
        ),
        migrations.AlterField(
            model_name='contratobicicleta',
            name='fechafin',
            field=models.DateTimeField(db_column='fechafin', default=datetime.datetime(2021, 8, 19, 8, 49, 58, 716876)),
        ),
    ]