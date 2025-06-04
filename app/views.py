from django.shortcuts import render
from .models import *


# Create your views here.
def inicio(request):

    template_name = "app/index.html"

    texto_presentacion = TextoPresentacion.objects.all()
    servicios = Servicio.objects.all()
    empresas_trabajadas = EmpresaTrabajada.objects.all()
    proyecto_finalizado = ProyectoFinalizado.objects.all()


    context = {"texto_presentacion":texto_presentacion,"servicios": servicios,"empresas_trabajadas": empresas_trabajadas,"proyecto_finalizado": proyecto_finalizado}

    return render(request, template_name, context)

# views.py para el panel de administración - CORREGIDO

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.http import HttpResponse

# Create your views here.
def inicio(request):
    template_name = "app/index.html"

    texto_presentacion = TextoPresentacion.objects.all()
    servicios = Servicio.objects.all()
    empresas_trabajadas = EmpresaTrabajada.objects.all()
    proyecto_finalizado = ProyectoFinalizado.objects.all()

    context = {
        "texto_presentacion": texto_presentacion,
        "servicios": servicios,
        "empresas_trabajadas": empresas_trabajadas,
        "proyecto_finalizado": proyecto_finalizado
    }

    return render(request, template_name, context)

# Importar los modelos
from .models import TextoPresentacion, Servicio, EmpresaTrabajada, ProyectoFinalizado

@csrf_protect
@never_cache
def admin_login(request):
    """
    Vista para el login del panel de administración
    """
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        

        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    # Configurar duración de sesión
                    if not remember_me:
                        request.session.set_expiry(0)  # Se cierra al cerrar navegador
                    else:
                        request.session.set_expiry(1209600)  # 2 semanas
                    
                    messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}!')
                    
                    # Redirigir a la página solicitada o dashboard
                    next_url = request.GET.get('next', 'admin_dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Tu cuenta está desactivada.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
    
    return render(request, 'app/admin/login.html')

@login_required(login_url='admin_login')
def admin_logout(request):
    """
    Vista para cerrar sesión
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('admin_login')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    """
    Vista principal del dashboard
    """
    # Obtener estadísticas reales de los modelos
    total_presentaciones = TextoPresentacion.objects.count()
    total_servicios = Servicio.objects.count()
    total_empresas = EmpresaTrabajada.objects.count()
    total_proyectos = ProyectoFinalizado.objects.count()
    
    # Actividad reciente (últimos elementos creados por ID - ya que no hay created_at)
    recent_activities = []
    
    # Últimos servicios (por ID descendente)
    latest_servicios = Servicio.objects.order_by('-id')[:2]
    for servicio in latest_servicios:
        recent_activities.append({
            'icon': 'cogs',
            'description': f'Servicio "{servicio.titulo}" en el sistema',
            'created_at': timezone.now(),  # Usamos fecha actual como placeholder
        })
    
    # Últimos proyectos
    latest_proyectos = ProyectoFinalizado.objects.order_by('-id')[:2]
    for proyecto in latest_proyectos:
        recent_activities.append({
            'icon': 'project-diagram',
            'description': f'Proyecto "{proyecto.titulo}" en el sistema',
            'created_at': timezone.now(),
        })
    
    # Últimas empresas
    latest_empresas = EmpresaTrabajada.objects.order_by('-id')[:1]
    for empresa in latest_empresas:
        recent_activities.append({
            'icon': 'building',
            'description': f'Empresa "{empresa.nombre_empresa}" en el sistema',
            'created_at': timezone.now(),
        })
    
    context = {
        'total_presentaciones': total_presentaciones,
        'total_servicios': total_servicios,
        'total_empresas': total_empresas,
        'total_proyectos': total_proyectos,
        'recent_activities': recent_activities,
        'last_update': timezone.now(),
    }
    
    return render(request, 'app/admin/dashboard.html', context)

@login_required(login_url='admin_login')
def admin_presentacion(request):
    """
    Vista para gestionar textos de presentación
    """
    presentaciones = TextoPresentacion.objects.all().order_by('-id')  # Cambiado a -id
    
    context = {
        'presentaciones': presentaciones,
    }
    
    return render(request, 'app/admin/presentacion.html', context)

@login_required(login_url='admin_login')
def admin_servicios(request):
    """
    Vista para gestionar servicios
    """
    servicios = Servicio.objects.all().order_by('-id')  # Cambiado a -id
    
    context = {
        'servicios': servicios,
    }
    
    return render(request, 'app/admin/servicios.html', context)

@login_required(login_url='admin_login')
def admin_empresas(request):
    """
    Vista para gestionar empresas trabajadas
    """
    empresas = EmpresaTrabajada.objects.all().order_by('-id')  # Cambiado a -id
    
    context = {
        'empresas': empresas,
    }
    
    return render(request, 'app/admin/empresas.html', context)

@login_required(login_url='admin_login')
def admin_proyectos(request):
    """
    Vista para gestionar proyectos finalizados
    """
    proyectos = ProyectoFinalizado.objects.all().order_by('-id')  # Cambiado a -id
    
    context = {
        'proyectos': proyectos,
    }
    
    return render(request, 'app/admin/proyectos.html', context)

# ========== VISTAS AJAX PARA MODALES ==========

# En tu views.py del admin

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

# Mapping de modelos
MODEL_MAPPING = {
    'presentacion': TextoPresentacion,
    'servicio': Servicio,
    'empresa': EmpresaTrabajada,
    'proyecto': ProyectoFinalizado,
}

@login_required(login_url='admin_login')
@require_http_methods(["GET"])
def ajax_get_item(request, model_name, item_id):
    """
    Obtener un elemento específico vía AJAX
    """
    try:
        # Validar modelo
        if model_name not in MODEL_MAPPING:
            return JsonResponse({
                'success': False,
                'error': 'Modelo no válido'
            }, status=400)
        
        model_class = MODEL_MAPPING[model_name]
        
        # Obtener el objeto
        try:
            obj = model_class.objects.get(id=item_id)
        except model_class.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Elemento no encontrado'
            }, status=404)
        
        # Serializar datos
        data = {}
        for field in obj._meta.fields:
            field_value = getattr(obj, field.name)
            
            # Manejar diferentes tipos de campos
            if hasattr(field_value, 'url'):  # ImageField/FileField
                data[field.name] = field_value.url if field_value else ''
            elif hasattr(field_value, 'isoformat'):  # DateField/DateTimeField
                data[field.name] = field_value.isoformat() if field_value else ''
            else:
                data[field.name] = field_value
        
        return JsonResponse({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def ajax_save_item(request, model_name):
    """
    Guardar/actualizar un elemento vía AJAX
    """
    try:
        # Validar modelo
        if model_name not in MODEL_MAPPING:
            return JsonResponse({
                'success': False,
                'error': 'Modelo no válido'
            }, status=400)
        
        model_class = MODEL_MAPPING[model_name]
        
        # Obtener datos del formulario
        item_id = request.POST.get('id')
        
        # Crear o actualizar
        if item_id and item_id.strip():
            try:
                obj = model_class.objects.get(id=item_id)
                action = 'actualizado'
            except model_class.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Elemento no encontrado'
                }, status=404)
        else:
            obj = model_class()
            action = 'creado'
        
        # Actualizar campos
        for field in model_class._meta.fields:
            if field.name == 'id':
                continue
                
            field_value = None
            
            if field.name in request.POST:
                field_value = request.POST.get(field.name)
            elif field.name in request.FILES:
                field_value = request.FILES.get(field.name)
            else:
                continue
            
            # Solo actualizar si hay valor o es una actualización
            if field_value or (item_id and item_id.strip()):
                setattr(obj, field.name, field_value)
        
        # Guardar
        obj.save()
        
        model_display_name = get_model_display_name(model_name)
        
        return JsonResponse({
            'success': True,
            'message': f'{model_display_name} {action} correctamente',
            'reload': True,
            'data': {'id': obj.id}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required(login_url='admin_login')
@require_http_methods(["DELETE"])
def ajax_delete_item(request, model_name, item_id):
    """
    Eliminar un elemento vía AJAX
    """
    try:
        # Validar modelo
        if model_name not in MODEL_MAPPING:
            return JsonResponse({
                'success': False,
                'error': 'Modelo no válido'
            }, status=400)
        
        model_class = MODEL_MAPPING[model_name]
        
        # Obtener el objeto
        try:
            obj = model_class.objects.get(id=item_id)
        except model_class.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Elemento no encontrado'
            }, status=404)
        
        # Eliminar
        obj.delete()
        
        model_display_name = get_model_display_name(model_name)
        
        return JsonResponse({
            'success': True,
            'message': f'{model_display_name} eliminado correctamente',
            'reload': True
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_model_display_name(model_name):
    """Helper para obtener nombres legibles de los modelos"""
    display_names = {
        'servicio': 'Servicio',
        'presentacion': 'Texto de Presentación',
        'empresa': 'Empresa',
        'proyecto': 'Proyecto'
    }
    return display_names.get(model_name, model_name.title())


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://aluminiosalusur.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

from django.shortcuts import get_object_or_404

def servicio_detalle(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    return render(request, "app/servicio_detalle.html", {"servicio": servicio})

def empresa_detalle(request, pk):
    empresa = get_object_or_404(EmpresaTrabajada, pk=pk)
    return render(request, "app/empresa_detalle.html", {"empresa": empresa})

def proyecto_detalle(request, pk):
    proyecto = get_object_or_404(ProyectoFinalizado, pk=pk)
    return render(request, "app/proyecto_detalle.html", {"proyecto": proyecto})