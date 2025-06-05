from django.contrib.sitemaps import Sitemap
from .models import Servicio, ProyectoFinalizado

class ServicioSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Servicio.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()




class ProyectoFinalizadoSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ProyectoFinalizado.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
