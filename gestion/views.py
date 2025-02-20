from django.shortcuts import render
from django.http import FileResponse
from .forms import ArchivoForm
from .utils.manejador import Manejador 

def gestion(request):
    form = ArchivoForm()

    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']

            try:
                manejador = Manejador(archivo)
                zip_path = manejador.manejar()  # Ahora retorna el ZIP en lugar de un mensaje

                # Forzar la descarga del archivo ZIP
                return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename="facturas_procesadas.zip")

            except Exception as e:
                mensaje = f"Error al procesar el archivo: {str(e)}"
                return render(request, 'gestion/gestion.html', {'form': form, 'mensaje': mensaje})

    return render(request, 'gestion/gestion.html', {'form': form})
