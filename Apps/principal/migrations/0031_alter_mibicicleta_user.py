# Generated by Django 3.2.3 on 2021-07-10 01:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0030_mibicicleta_disponible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mibicicleta',
            name='user',
            field=models.ForeignKey(db_column='Propietario', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='miBici', to=settings.AUTH_USER_MODEL),
        ),
    ]
