# Generated by Django 4.2.2 on 2023-06-11 02:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0006_alter_boleta_fecha"),
    ]

    operations = [
        migrations.AlterField(
            model_name="boleta",
            name="fecha",
            field=models.DateTimeField(default="2023-06-11 02:23:28"),
        ),
    ]