from django.shortcuts import render

# Create your views here.
def nosotros(request):
    template_name = "nosotros/nosotros.html"
    return render(request, template_name)