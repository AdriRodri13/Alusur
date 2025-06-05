from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from app.models import Servicio, ProyectoFinalizado, TextoPresentacion




urlpatterns = [
    # ========== SITIO WEB PÚBLICO ==========
    path('', views.inicio, name='inicio'),

    path("robots.txt", views.robots_txt),
    
    # ========== PANEL DE ADMINISTRACIÓN ==========
    # Autenticación
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    
    # Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Gestión de contenido
    path('admin/presentacion/', views.admin_presentacion, name='admin_presentacion'),
    path('admin/servicios/', views.admin_servicios, name='admin_servicios'),
    path('admin/proyectos/', views.admin_proyectos, name='admin_proyectos'),
    
    # Vistas AJAX para modales
    # Vistas AJAX para modales
    path('admin/ajax/get/<str:model_name>/<int:item_id>/', views.ajax_get_item, name='admin_ajax_get_item'),
    path('admin/ajax/save/<str:model_name>/', views.ajax_save_item, name='admin_ajax_save_item'),
    path('admin/ajax/delete/<str:model_name>/<int:item_id>/', views.ajax_delete_item, name='admin_ajax_delete_item'),  # ← Cambiar aquí

    
    path('servicio/<int:pk>/', views.servicio_detalle, name='servicio_detalle'),
    path('proyecto/<int:pk>/', views.proyecto_detalle, name='proyecto_detalle'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)