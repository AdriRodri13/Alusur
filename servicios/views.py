from django.shortcuts import render
from .models import Servicio

# Create your views here.
def servicios(request):
    servicios = Servicio.objects.all
    template_name = "servicios/servicios.html"
    return render(request, template_name, {'servicios':servicios})