from django.contrib import admin
from .models import Servicio, ProyectoFinalizado, TextoPresentacion, Parrafo


class ParrafoServicioInline(admin.TabularInline):
    model = Parrafo
    fk_name = "servicio"
    extra = 1
    fields = ("contenido", "imagen")


class ParrafoProyectoInline(admin.TabularInline):
    model = Parrafo
    fk_name = "proyecto"
    extra = 1
    fields = ("contenido", "imagen")

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("titulo",)
    search_fields = ("titulo",)
    list_per_page = 25
    inlines = [ParrafoServicioInline]


@admin.register(ProyectoFinalizado)
class ProyectoFinalizadoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descripcion")
    search_fields = ("titulo", "descripcion")
    list_per_page = 25
    inlines = [ParrafoProyectoInline]

@admin.register(TextoPresentacion)
class TextoPresentacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descripcion")
    search_fields = ("titulo", "descripcion")
    list_per_page = 25


@admin.register(Parrafo)
class ParrafoAdmin(admin.ModelAdmin):
    list_display = ("id", "servicio", "proyecto", "contenido")
    list_filter = ("servicio", "proyecto")
    search_fields = ("contenido",)
    list_per_page = 25
