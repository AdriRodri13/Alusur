from django.db import models

from .utils import seleccionar_storage
from django.urls import reverse
# Create your models here.

class TextoPresentacion(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(
        storage=seleccionar_storage(),
        upload_to='TextoPresentacion/',
        blank=True,
        null=True
    )


class Servicio(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(
        storage=seleccionar_storage(), #si estamos en debug, se sube al media local, si no se sube a clodynary
        upload_to='Servicio/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("servicio_detalle", args=[self.id])


class ProyectoFinalizado(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(
        storage=seleccionar_storage(),
        upload_to='ProyectoFinalizado/',
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse("proyecto_detalle", args=[self.id])



