# Generated by Django 5.2.1 on 2025-06-07 15:07

import django.core.files.storage
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_delete_empresatrabajada"),
    ]

    operations = [
        migrations.CreateModel(
            name="Parrafo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("contenido", models.TextField()),
                (
                    "imagen",
                    models.ImageField(
                        blank=True,
                        null=True,
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="Parrafo/",
                    ),
                ),
                (
                    "proyecto",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parrafos",
                        to="app.proyectofinalizado",
                    ),
                ),
                (
                    "servicio",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parrafos",
                        to="app.servicio",
                    ),
                ),
            ],
        ),
    ]
