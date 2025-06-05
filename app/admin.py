from django.contrib import admin
from .models import Servicio, ProyectoFinalizado, TextoPresentacion

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("titulo",)
    search_fields = ("titulo",)
    list_per_page = 25


@admin.register(ProyectoFinalizado)
class ProyectoFinalizadoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descripcion")
    search_fields = ("titulo", "descripcion")
    list_per_page = 25

@admin.register(TextoPresentacion)
class TextoPresentacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descripcion")
    search_fields = ("titulo", "descripcion")
    list_per_page = 25
