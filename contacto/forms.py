from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Tu Nombre'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Tu Email'})
    )

    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tu Mensaje'})
    )