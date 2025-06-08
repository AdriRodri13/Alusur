from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Servicio, ProyectoFinalizado, TextoPresentacion

class StaticViewSitemap(Sitemap):
    """Sitemap para páginas estáticas del sitio"""
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return [
            'inicio',
            'aviso_privacidad', 
            'terminos_servicio',
            'politica_cookies'
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        # Retorna la fecha actual para páginas estáticas
        return timezone.now()

class ServicioSitemap(Sitemap):
    """Sitemap para servicios"""
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Servicio.objects.all().order_by('-id')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        # Si tienes un campo de fecha de modificación, úsalo
        # return obj.updated_at
        # Si no, usa la fecha actual
        return timezone.now()

    def priority(self, obj):
        # Prioridad dinámica basada en si tiene párrafos
        if hasattr(obj, 'parrafos') and obj.parrafos.exists():
            return 0.9
        return 0.8

class ProyectoFinalizadoSitemap(Sitemap):
    """Sitemap para proyectos finalizados"""
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ProyectoFinalizado.objects.all().order_by('-id')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        # Si tienes un campo de fecha de modificación, úsalo
        # return obj.updated_at
        # Si no, usa la fecha actual
        return timezone.now()

    def priority(self, obj):
        # Prioridad dinámica basada en si tiene párrafos
        if hasattr(obj, 'parrafos') and obj.parrafos.exists():
            return 0.8
        return 0.7

class TextoPresentacionSitemap(Sitemap):
    """Sitemap para textos de presentación (si tienen URLs individuales)"""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        # Solo incluir si los textos de presentación tienen URLs propias
        # Si no, puedes comentar esta clase completa
        return TextoPresentacion.objects.all()

    def location(self, obj):
        # Asume que tienes URLs para textos individuales
        # Si no las tienes, comenta esta clase
        return f'/presentacion/{obj.id}/'

    def lastmod(self, obj):
        return timezone.now()

