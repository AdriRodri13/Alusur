from django.db import models
from django.utils.text import slugify

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


class EntradaBlog(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(help_text="Descripción breve que aparecerá en el listado del blog")
    imagen_portada = models.ImageField(
        storage=seleccionar_storage(),
        upload_to='EntradaBlog/',
        blank=True,
        null=True,
        help_text="Imagen principal de la entrada"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False, help_text="¿Está publicada la entrada?")
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="URL amigable (se genera automáticamente)")
    
    def save(self, *args, **kwargs):
        # Generar slug automáticamente si no existe
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            num = 1
            while EntradaBlog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("blog_detalle", args=[self.slug])
    
    class Meta:
        verbose_name = "Entrada de Blog"
        verbose_name_plural = "Entradas de Blog"
        ordering = ['-fecha_creacion']


class Parrafo(models.Model):
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="parrafos",
        blank=True,
        null=True,
    )
    proyecto = models.ForeignKey(
        ProyectoFinalizado,
        on_delete=models.CASCADE,
        related_name="parrafos",
        blank=True,
        null=True,
    )
    entrada_blog = models.ForeignKey(
        EntradaBlog,
        on_delete=models.CASCADE,
        related_name="parrafos",
        blank=True,
        null=True,
    )
    titulo = models.CharField(max_length=100, blank=True, null=True)
    contenido = models.TextField()
    imagen = models.ImageField(
        storage=seleccionar_storage(),
        upload_to="Parrafo/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.contenido[:50]



