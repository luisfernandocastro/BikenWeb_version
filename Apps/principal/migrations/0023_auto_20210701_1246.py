# Generated by Django 3.2.3 on 2021-07-01 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0022_rename_valotiempoalquiler_mibicicleta_valortiempoalquiler'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mibicicleta',
            name='valortiempoalquiler',
        ),
        migrations.AddField(
            model_name='mibicicleta',
            name='valortiempohoras',
            field=models.IntegerField(blank=True, db_column='Horas de alquiler', default=23, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='mibicicleta',
            name='valortiempomin',
            field=models.IntegerField(blank=True, db_column='Minutos de alquiler', default=0, max_length=2, null=True),
        ),
    ]