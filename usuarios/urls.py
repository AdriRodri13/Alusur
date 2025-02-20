from django.urls import include, path
from . import views

urlpatterns = [
    path('perfil/', views.perfil, name='Perfil'),  
    path('login/', views.login_vista, name='Login'),  
    path('logout/', views.logout_vista, name='Logout'),     
]