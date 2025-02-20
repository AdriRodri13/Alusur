from django import forms

class ArchivoForm(forms.Form):
    archivo = forms.FileField(
        label = "Subir archivo ZIP o RAR",
        required=True
    )

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            extension = archivo.name.split('.')[-1].lower()
            if extension not in ['zip', 'rar']:
                raise forms.ValidationError("Solo se permiten archivos .zip o .rar ")
            
        return archivo