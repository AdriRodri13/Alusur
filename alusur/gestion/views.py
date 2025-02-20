from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ArchivoForm
from .utils.manejador import Manejador 

# Create your views here.
def gestion(request):
    form = ArchivoForm()
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']

            #guardamos el archivo en la carpeta media
            fs = FileSystemStorage()
            filename = fs.save(archivo.name, archivo)

            manejador = Manejador(archivo)
            mensaje = manejador.manejar()

            return render(request, 'gestion/archivo_subido.html', {'mensaje': mensaje})
        else:
            form = ArchivoForm()

    return render(request, 'gestion/gestion.html', {'form': form})