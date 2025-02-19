from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactoForm


# Create your views here.
def contacto(request):
    template_name='contacto/contacto.html'
    form = ContactoForm()

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            #enviar mail
            send_mail(
                f'Contacto de {nombre}',
                mensaje,
                email,
                ['daniadri963@gmail.com']
            )

        return render(request,template_name,{'form':form,'success':True})
        
    return render(request,template_name,{'form':form})