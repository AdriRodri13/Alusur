from django.urls import include, path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.nosotros, name="Nosotros")
]