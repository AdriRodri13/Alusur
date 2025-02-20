from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


# Create your views here.
@login_required
def perfil(request):
    return render(request, "usuarios/perfil.html")

def login_vista(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form':form})

def logout_vista(request):
    logout(request)
    return redirect('Inicio')