from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ServicioSitemap, ProyectoFinalizadoSitemap, EntradaBlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'servicios': ServicioSitemap,
    'proyectos': ProyectoFinalizadoSitemap,
    'blog': EntradaBlogSitemap,
}


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
    path('admin/blog/', views.admin_blog, name='admin_blog'),
    path('aviso-privacidad/', views.aviso_privacidad, name='aviso_privacidad'),
    path('politica-cookies/', views.politica_cookies, name='politica_cookies'),
    path('terminos-servicio/', views.terminos_servicio, name='terminos_servicio'),
    
    # Vistas AJAX para modales
    path('admin/ajax/get/<str:model_name>/<int:item_id>/', views.ajax_get_item, name='admin_ajax_get_item'),
    path('admin/ajax/save/<str:model_name>/', views.ajax_save_item, name='admin_ajax_save_item'),
    path('admin/ajax/delete/<str:model_name>/<int:item_id>/', views.ajax_delete_item, name='admin_ajax_delete_item'),  
    path('admin/servicios/<int:servicio_id>/parrafos/', views.admin_servicio_parrafos, name='admin_servicio_parrafos'),
    path('admin/proyectos/<int:proyecto_id>/parrafos/', views.admin_proyecto_parrafos, name='admin_proyecto_parrafos'),
    path('admin/blog/<int:entrada_id>/parrafos/', views.admin_entrada_blog_parrafos, name='admin_entrada_blog_parrafos'),
    path('admin/generar-texto-ia/', views.generacion_texto_ia, name='generacion_texto_ia'),
    
    path('servicio/<int:pk>/', views.servicio_detalle, name='servicio_detalle'),
    path('proyecto/<int:pk>/', views.proyecto_detalle, name='proyecto_detalle'),
    
    # ========== BLOG PÚBLICO ==========
    path('blog/', views.blog_lista, name='blog_lista'),
    path('blog/<slug:slug>/', views.blog_detalle, name='blog_detalle'),

    # ========== SEO ==========
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    #Asistente IA
    path('asistente-chat/', views.asistente_chat, name='asistente_chat'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)