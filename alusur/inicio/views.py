from django.shortcuts import render

# Create your views here.
def inicio(request):
    template_name = "inicio/inicio.html"
    return render(request, template_name)