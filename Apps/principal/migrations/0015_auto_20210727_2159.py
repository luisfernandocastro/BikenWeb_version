# Generated by Django 3.2.3 on 2021-07-28 02:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0014_auto_20210726_0950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalogo',
            options={},
        ),
        migrations.AlterField(
            model_name='contratobicicleta',
            name='fechafin',
            field=models.DateTimeField(db_column='fechafin', default=datetime.datetime(2021, 7, 29, 21, 59, 2, 263527)),
        ),
        migrations.AlterField(
            model_name='contratobicicleta',
            name='fechainicio',
            field=models.DateTimeField(db_column='Fecha Inicio Contrato', default=datetime.datetime(2021, 7, 27, 21, 59, 2, 263527)),
        ),
    ]
