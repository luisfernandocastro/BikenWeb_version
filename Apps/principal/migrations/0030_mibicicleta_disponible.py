# Generated by Django 3.2.3 on 2021-07-10 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0029_alter_perfil_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='mibicicleta',
            name='disponible',
            field=models.BooleanField(db_column='Disponible', default=True),
        ),
    ]
