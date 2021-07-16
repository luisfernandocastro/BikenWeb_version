# Generated by Django 3.2.3 on 2021-07-14 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0004_delete_observaciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContratoBicicleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechainicio', models.DateTimeField(db_column='fechainicio', default=None)),
                ('fechafin', models.DateTimeField(db_column='fechafin', default=None)),
                ('tiempo', models.TimeField(db_column='Tiempo')),
                ('bicicleta', models.ForeignKey(db_column='Bicicleta', on_delete=django.db.models.deletion.DO_NOTHING, to='principal.mibicicleta')),
                ('tipocontrato', models.ForeignKey(db_column='Tipocontrato', on_delete=django.db.models.deletion.DO_NOTHING, to='principal.tipocontrato')),
                ('usuario', models.ForeignKey(db_column='usuario', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Contratos',
            },
        ),
    ]
