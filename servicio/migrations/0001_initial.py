# Generated by Django 4.2 on 2023-07-16 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.CharField(choices=[('09', '09:00 - 10:00'), ('10', '10:00 - 11:00'), ('11', '11:00 - 12:00'), ('12', '12:00 - 01:00'), ('16', '04:00 - 05:00'), ('17', '05:00 - 06:00'), ('18', '06:00 - 07:00'), ('19', '07:00 - 08:00'), ('20', '08:00 - 09:00'), ('21', '09:00 - 10:00')], max_length=10, unique=True)),
                ('meridiem', models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], default='PM', max_length=2)),
            ],
            options={
                'verbose_name': 'Horario',
                'verbose_name_plural': 'Horarios',
            },
        ),
        migrations.CreateModel(
            name='TipoCancha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=0, max_digits=8)),
                ('descripcion', models.TextField()),
            ],
            options={
                'verbose_name': 'Tipo de Cancha',
                'verbose_name_plural': 'Tipos de Canchas',
            },
        ),
        migrations.CreateModel(
            name='Cancha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeracion', models.CharField(choices=[('1', 'Cancha 1'), ('2', 'Cancha 2'), ('3', 'Cancha 3'), ('4', 'Cancha 4'), ('5', 'Cancha 5'), ('6', 'Cancha 6'), ('7', 'Cancha 7'), ('8', 'Cancha 8')], max_length=10)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='canchas', to='servicio.tipocancha')),
            ],
            options={
                'verbose_name': 'Cancha',
                'verbose_name_plural': 'Canchas',
            },
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponible', models.BooleanField(default=True)),
                ('cancha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicio.cancha')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicio.horario')),
            ],
            options={
                'verbose_name': 'Agenda',
                'verbose_name_plural': 'Agendas',
                'unique_together': {('cancha', 'horario')},
            },
        ),
    ]
