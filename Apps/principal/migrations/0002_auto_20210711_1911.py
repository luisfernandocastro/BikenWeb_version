# Generated by Django 3.2.3 on 2021-07-12 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='image_portada',
            field=models.ImageField(blank=True, null=True, upload_to='custom_upload_to_banner', verbose_name='Imagen de portada'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='image_user',
            field=models.ImageField(blank=True, null=True, upload_to='custom_upload_to_profile', verbose_name='Imagen de perfil'),
        ),
    ]
