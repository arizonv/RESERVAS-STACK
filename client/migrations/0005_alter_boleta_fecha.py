# Generated by Django 4.2.2 on 2023-06-11 01:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0004_alter_boleta_fecha_alter_reserva_dia"),
    ]

    operations = [
        migrations.AlterField(
            model_name="boleta",
            name="fecha",
            field=models.DateTimeField(default="2023-06-11 01:42:28"),
        ),
    ]
