# Generated by Django 5.1.6 on 2025-02-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Servicio",
            fields=[
                ("iden", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=100)),
                ("descripcion", models.TextField()),
                ("imagen", models.ImageField(upload_to="servicios")),
            ],
            options={
                "verbose_name": "servicio",
                "verbose_name_plural": "servicios",
            },
        ),
    ]
