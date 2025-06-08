from django.shortcuts import render
from .models import TextoPresentacion, Servicio, ProyectoFinalizado, Parrafo
import requests
from django.conf import settings

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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from bs4 import BeautifulSoup
import json

import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from bs4 import BeautifulSoup
import json


# Create your views here.
def inicio(request):

    template_name = "app/index.html"

    texto_presentacion = TextoPresentacion.objects.all()
    servicios = Servicio.objects.all()
    proyecto_finalizado = ProyectoFinalizado.objects.all()


    context = {"texto_presentacion": texto_presentacion, "servicios": servicios, "proyecto_finalizado": proyecto_finalizado}

    return render(request, template_name, context)

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
    
    
    context = {
        'total_presentaciones': total_presentaciones,
        'total_servicios': total_servicios,
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
def admin_proyectos(request):
    """
    Vista para gestionar proyectos finalizados
    """
    proyectos = ProyectoFinalizado.objects.all().order_by('-id')  # Cambiado a -id
    
    context = {
        'proyectos': proyectos,
    }
    
    return render(request, 'app/admin/proyectos.html', context)

# Vista para gestionar párrafos de un servicio específico
@login_required(login_url='admin_login')
def admin_servicio_parrafos(request, servicio_id):
    """
    Vista para gestionar párrafos de un servicio específico
    """
    try:
        servicio = Servicio.objects.get(id=servicio_id)
    except Servicio.DoesNotExist:
        messages.error(request, 'Servicio no encontrado')
        return redirect('admin_servicios')
    
    parrafos = Parrafo.objects.filter(servicio=servicio).order_by('id')
    
    context = {
        'servicio': servicio,
        'parrafos': parrafos,
        'tipo_contenido': 'servicio'
    }
    
    return render(request, 'app/admin/parrafos.html', context)

# Vista para gestionar párrafos de un proyecto específico
@login_required(login_url='admin_login')
def admin_proyecto_parrafos(request, proyecto_id):
    """
    Vista para gestionar párrafos de un proyecto específico
    """
    try:
        proyecto = ProyectoFinalizado.objects.get(id=proyecto_id)
    except ProyectoFinalizado.DoesNotExist:
        messages.error(request, 'Proyecto no encontrado')
        return redirect('admin_proyectos')
    
    parrafos = Parrafo.objects.filter(proyecto=proyecto).order_by('id')
    
    context = {
        'proyecto': proyecto,
        'parrafos': parrafos,
        'tipo_contenido': 'proyecto'
    }
    
    return render(request, 'app/admin/parrafos.html', context)



# Mapping de modelos
MODEL_MAPPING = {
    'presentacion': TextoPresentacion,
    'servicio': Servicio,
    'proyecto': ProyectoFinalizado,
    'parrafo': Parrafo,
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
            if hasattr(field, 'upload_to'):  # ImageField/FileField
                # Verificar si el campo tiene valor antes de acceder a .url
                if field_value and hasattr(field_value, 'url'):
                    data[field.name + '_url'] = field_value.url
                    data[field.name] = str(field_value)  # Nombre del archivo
                else:
                    data[field.name + '_url'] = ''
                    data[field.name] = ''
            elif field.__class__.__name__ == 'ForeignKey':  # ForeignKey específico
                # Para relaciones, guardar solo el ID
                if field_value is not None:
                    data[field.name] = field_value.id
                    data[field.name + '_name'] = str(field_value)  # Nombre para display
                else:
                    data[field.name] = None
                    data[field.name + '_name'] = ''
            elif hasattr(field_value, 'isoformat'):  # DateField/DateTimeField
                data[field.name] = field_value.isoformat() if field_value else ''
            else:
                data[field.name] = field_value if field_value is not None else ''
        
        return JsonResponse({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def ajax_save_item(request, model_name):
    """
    Guardar/actualizar un elemento vía AJAX (actualizado para párrafos)
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
        
        # Manejar párrafos especialmente
        if model_name == 'parrafo':
            # Obtener el servicio o proyecto padre
            servicio_id = request.POST.get('servicio_id')
            proyecto_id = request.POST.get('proyecto_id')
            
            if servicio_id:
                try:
                    servicio = Servicio.objects.get(id=servicio_id)
                    obj.servicio = servicio
                    obj.proyecto = None
                except Servicio.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Servicio no encontrado'
                    }, status=404)
            elif proyecto_id:
                try:
                    proyecto = ProyectoFinalizado.objects.get(id=proyecto_id)
                    obj.proyecto = proyecto
                    obj.servicio = None
                except ProyectoFinalizado.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Proyecto no encontrado'
                    }, status=404)
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Debe especificar un servicio o proyecto'
                }, status=400)
        
        # Actualizar campos normales
        for field in model_class._meta.fields:
            if field.name in ['id', 'servicio', 'proyecto']:
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


# Actualizar get_model_display_name
def get_model_display_name(model_name):
    """Helper para obtener nombres legibles de los modelos"""
    display_names = {
        'servicio': 'Servicio',
        'presentacion': 'Texto de Presentación',
        'proyecto': 'Proyecto',
        'parrafo': 'Párrafo'
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
    parrafos = servicio.parrafos.all().order_by('id')
    
    context = {
        'item': servicio,  # Objeto unificado
        'parrafos': parrafos,
        'tipo_contenido': 'servicio',  # Para breadcrumb y títulos
        'seccion_id': 'servicios',  # Para el botón de regreso
    }
    
    return render(request, "app/detalle.html", context)

def proyecto_detalle(request, pk):
    proyecto = get_object_or_404(ProyectoFinalizado, pk=pk)
    parrafos = proyecto.parrafos.all().order_by('id')
    
    context = {
        'item': proyecto,  # Objeto unificado
        'parrafos': parrafos,
        'tipo_contenido': 'proyecto',  # Para breadcrumb y títulos
        'seccion_id': 'proyectos',  # Para el botón de regreso
    }
    
    return render(request, "app/detalle.html", context)

def aviso_privacidad(request):
    """Página de aviso de privacidad"""
    return render(request, "app/aviso_privacidad.html")

def politica_cookies(request):
    """Página de política de cookies"""
    return render(request, "app/politica_cookies.html")

def terminos_servicio(request):
    """Página de términos de servicio"""
    return render(request, "app/terminos_servicio.html")


def obtener_parrafos_existentes(item_id, tipo_contenido):
    """
    Obtiene todos los párrafos existentes de un servicio o proyecto.
    Extrae solo el texto limpio para proporcionar contexto a la IA.
    """
    try:
        from .models import Parrafo
        
        # Filtrar párrafos según el tipo de contenido
        if tipo_contenido == 'servicio':
            parrafos = Parrafo.objects.filter(
                servicio_id=item_id,
                servicio__isnull=False
            ).order_by('id')  # Ordenar por ID ya que no hay campo 'orden'
        else:  # proyecto
            parrafos = Parrafo.objects.filter(
                proyecto_id=item_id,
                proyecto__isnull=False
            ).order_by('id')
        
        contexto_parrafos = []
        for parrafo in parrafos:
            # Limpiar HTML del contenido para extraer solo texto
            if parrafo.contenido:
                soup = BeautifulSoup(parrafo.contenido, 'html.parser')
                texto_limpio = soup.get_text().strip()
                
                # Evitar párrafos vacíos después de limpiar HTML
                if texto_limpio:
                    parrafo_info = {
                        'titulo': parrafo.titulo or '',
                        'contenido': texto_limpio[:200] + '...' if len(texto_limpio) > 200 else texto_limpio,
                        'tiene_imagen': bool(parrafo.imagen)
                    }
                    contexto_parrafos.append(parrafo_info)
        
        return contexto_parrafos
        
    except Exception as e:
        print(f"Error obteniendo párrafos existentes: {str(e)}")
        return []


def obtener_titulo_item(item_id, tipo_contenido):
    """
    Obtiene el título del servicio o proyecto para contexto.
    Actualizada para usar los modelos correctos.
    """
    try:
        if tipo_contenido == 'servicio':
            from .models import Servicio
            item = Servicio.objects.get(id=item_id)
        else:  # proyecto
            from .models import ProyectoFinalizado
            item = ProyectoFinalizado.objects.get(id=item_id)
        
        return item.titulo
        
    except Exception as e:
        print(f"Error obteniendo título del item: {str(e)}")
        return ""

def construir_prompt_ia(especificaciones, incluir_titulo=False, contexto_parrafos=None, item_titulo=""):
    """
    Construye el prompt completo para la IA de manera modular.
    """
    
    # Palabras clave específicas del negocio
    palabras_clave = [
        "aluminio", "ventanas", "puertas", "cerramientos", "persianas",
        "barandillas", "mamparas", "rejas", "mosquiteras", "carpinteria",
        "aluminio de alta calidad", "instalación profesional", "diseño personalizado",
        "eficiencia energética", "durabilidad", "estética moderna", "seguridad mejorada",
        "sostenibilidad", "aislamiento térmico y acústico", "carpinteria de aluminio en alicante",
        "ALUSUR", "Aluminios del Sureste", "Alicante", "profesionalismo", "garantía"
    ]
    
    # Prompt base con identidad de la IA
    prompt_base = (
        "Eres un redactor SEO profesional especializado en carpintería de aluminio. "
        "Tu tarea es generar contenido optimizado para la web de Aluminios del Sureste (ALUSUR). "
        "NO uses emojis. Tu estilo es directo, profesional y técnico."
        "Estamos buscando posicionarnos en la provicia de Alicante, concretamente en la zona de Elche, Aspe, Novelda y demás localidades cercanas. Por lo tanto inclute alguna si encaja bien con el texto, no es obligatorio.\n\n"
    )
    
    # Instrucciones para HTML enriquecido
    prompt_html = (
        "\nIMPORTANTE - FORMATO HTML:\n"
        "- Usa <p> para párrafos normales\n"
        "- <span class=\"importante\">texto clave</span> SOLO para 1-2 conceptos críticos\n"
        "- <span class=\"destacado\">información relevante</span> SOLO ocasionalmente\n"
        "- <span class=\"enfasis\">términos técnicos</span> para especialización\n"
        "- Mantén el contenido CONCISO (máximo 4 líneas por párrafo)\n"
        "- NO uses listas a menos que sea estrictamente necesario\n"
    )
    
    # Contexto de párrafos existentes
    prompt_contexto = ""
    if contexto_parrafos and len(contexto_parrafos) > 0:
        prompt_contexto = f"\nCONTEXTO - Párrafos ya existentes en '{item_titulo}':\n"
        for i, parrafo in enumerate(contexto_parrafos, 1):
            prompt_contexto += f"{i}. "
            if parrafo['titulo']:
                prompt_contexto += f"Título: '{parrafo['titulo']}' - "
            prompt_contexto += f"Contenido: {parrafo['contenido']}\n"
        
        prompt_contexto += (
            "\nIMPORTANTE: NO repitas información ya cubierta en estos párrafos. "
            "Genera contenido COMPLEMENTARIO y único que añada valor.\n"
        )
    
    # Palabras clave SEO
    prompt_seo = (
        f"\nSEO - Incluye naturalmente algunas palabras clave: "
        f"{', '.join(palabras_clave[:10])}.\n"  # Limitamos para no saturar
    )
    
    # Instrucciones específicas según si incluye título
    if incluir_titulo:
        prompt_output = (
            "\nOUTPUT REQUERIDO:\n"
            "1. Genera UN PÁRRAFO CORTO (máximo 4 líneas)\n"
            "2. Al final añade: TITULO_SUGERIDO: [título descriptivo máximo 50 caracteres]\n"
            "3. El título debe ser específico y diferente a los existentes\n"
        )
    else:
        prompt_output = (
            "\nOUTPUT REQUERIDO:\n"
            "Genera UN PÁRRAFO CORTO (máximo 4 líneas) sin título.\n"
        )
    
    # Ejemplo de formato esperado
    prompt_ejemplo = (
        "\nFORMATO EJEMPLO:\n"
        "<p>Nuestras <span class=\"importante\">ventanas de aluminio</span> destacan por su "
        "<span class=\"destacado\">excelente aislamiento térmico</span>. La instalación profesional "
        "garantiza un rendimiento óptimo durante décadas.</p>"
    )
    
    # Prompt completo
    prompt_completo = (
        f"{prompt_base}"
        f"{prompt_html}"
        f"{prompt_contexto}"
        f"{prompt_seo}"
        f"{prompt_output}"
        f"{prompt_ejemplo}\n\n"
        f"ESPECIFICACIONES DEL NUEVO CONTENIDO: {especificaciones}"
    )
    
    return prompt_completo

def obtener_titulo_item(item_id, tipo_contenido):
    """
    Obtiene el título del servicio o proyecto para contexto.
    """
    try:
        if tipo_contenido == 'servicio':
            from .models import Servicio
            item = Servicio.objects.get(id=item_id)
        else:
            from .models import Proyecto
            item = Proyecto.objects.get(id=item_id)
        
        return item.titulo
    except Exception as e:
        print(f"Error obteniendo título del item: {str(e)}")
        return ""

@csrf_exempt
@require_http_methods(["POST"])
def generacion_texto_ia(request):
    """
    Genera un texto utilizando IA (DeepSeek) basado en las especificaciones proporcionadas.
    Ahora incluye contexto de párrafos existentes para evitar repeticiones.
    """
    
    try:
        # Obtener datos del POST
        especificaciones = request.POST.get("especificaciones", "").strip()
        incluir_titulo = request.POST.get("incluir_titulo", "false").lower() == "true"
        item_id = request.POST.get("item_id")  # ID del servicio/proyecto
        tipo_contenido = request.POST.get("tipo_contenido", "servicio")  # 'servicio' o 'proyecto'
        
        # Validaciones
        if not especificaciones:
            return JsonResponse({"error": "Debes proporcionar especificaciones."}, status=400)
        
        # Obtener contexto de párrafos existentes
        contexto_parrafos = []
        item_titulo = ""
        
        if item_id:
            try:
                item_id = int(item_id)
                contexto_parrafos = obtener_parrafos_existentes(item_id, tipo_contenido)
                item_titulo = obtener_titulo_item(item_id, tipo_contenido)
            except (ValueError, TypeError):
                print(f"ID inválido: {item_id}")
        
        # Construir prompt modular
        prompt_completo = construir_prompt_ia(
            especificaciones=especificaciones,
            incluir_titulo=incluir_titulo,
            contexto_parrafos=contexto_parrafos,
            item_titulo=item_titulo
        )
        
        # Mensaje del sistema optimizado
        system_message = (
            "Eres un redactor SEO especializado en carpintería de aluminio. "
            "Escribes párrafos CORTOS y CONCISOS. Usas HTML mínimo para destacar conceptos clave. "
            "Tu estilo es directo, profesional y técnico. NUNCA repites información ya existente."
        )
        # Llamada a la API de DeepSeek
        response = requests.post(
            settings.DEEPSEEK_API_URL,
            headers={
                "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt_completo}
                ],
                "temperature": 0.7,
                "max_tokens": 450,  # Aumentado ligeramente para manejar contexto
                "top_p": 0.9,
                "frequency_penalty": 0.5,  # Reduce repeticiones
                "presence_penalty": 0.3    # Fomenta nuevos temas
            },
            timeout=100  # Aumentado para manejar contexto más largo
        )
        
        if response.status_code != 200:
            error_detail = ""
            try:
                error_data = response.json()
                error_detail = error_data.get('error', {}).get('message', 'Error desconocido')
            except:
                error_detail = f"Status code: {response.status_code}"
            
            return JsonResponse({
                "error": f"Error al comunicarse con la IA: {error_detail}"
            }, status=500)
        
        # Procesar respuesta
        data = response.json()
        contenido_generado = data["choices"][0]["message"]["content"].strip()
        
        # Separar contenido y título si es necesario
        resultado = {"texto": contenido_generado}
        
        if incluir_titulo and "TITULO_SUGERIDO:" in contenido_generado:
            partes = contenido_generado.split("TITULO_SUGERIDO:")
            if len(partes) == 2:
                resultado["texto"] = partes[0].strip()
                resultado["titulo"] = partes[1].strip()
        
        # Añadir información de contexto para debugging (opcional)
        if settings.DEBUG:
            resultado["debug_info"] = {
                "contexto_parrafos": len(contexto_parrafos),
                "item_titulo": item_titulo,
                "prompt_length": len(prompt_completo)
            }
        
        return JsonResponse(resultado)
    
    except requests.Timeout:
        return JsonResponse({
            "error": "Timeout: La IA tardó demasiado en responder. Intenta con especificaciones más breves."
        }, status=500)
    
    except requests.RequestException as e:
        
        return JsonResponse({
            "error": f"Error de conexión con la IA: {str(e)}"
        }, status=500)
    
    except KeyError as e:
        return JsonResponse({
            "error": f"Respuesta inesperada de la IA. Clave faltante: {str(e)}"
        }, status=500)
    
    except Exception as e:
        return JsonResponse({
            "error": f"Error interno del servidor: {str(e)}"
        }, status=500)
    