from django.shortcuts import render
from .models import *


# Create your views here.
def inicio(request):

    template_name = "app/index.html"

    texto_presentacion = TextoPresentacion.objects.all()
    servicios = Servicio.objects.all()
    empresas_trabajadas = EmpresaTrabajada.objects.all()
    proyecto_finalizado = ProyectoFinalizado.objects.all()


    context = {"texto_presentacion":texto_presentacion,"servicios": servicios,"empresas_trabajadas": empresas_trabajadas,"proyecto_finalizado": proyecto_finalizado}

    return render(request, template_name, context)