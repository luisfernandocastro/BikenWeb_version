# Generated by Django 3.2.3 on 2021-06-22 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0012_auto_20210617_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mibicicleta',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='miBici', to=settings.AUTH_USER_MODEL),
        ),
    ]
