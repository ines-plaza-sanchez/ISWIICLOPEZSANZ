"""
Vista de emergencia para diagnosticar problemas de Azure
Esta vista bypassa el sistema completo de Django
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os


@csrf_exempt
@require_http_methods(["GET", "POST"])
def emergency_debug(request):
    """Vista de emergencia que bypassa todo el middleware"""
    
    try:
        # Información básica
        info = {
            "status": "Django funciona!",
            "method": request.method,
            "path": request.path,
            "host": request.get_host(),
            "is_secure": request.is_secure(),
            "settings_module": os.environ.get('DJANGO_SETTINGS_MODULE', 'No configurado'),
            "website_hostname": os.environ.get('WEBSITE_HOSTNAME', 'No es Azure'),
            "port": os.environ.get('PORT', 'No configurado'),
            "headers": dict(request.headers),
        }
        
        # Convertir a JSON con indentación
        json_response = json.dumps(info, indent=2, ensure_ascii=False)
        
        return HttpResponse(
            json_response,
            content_type='application/json; charset=utf-8',
            status=200
        )
        
    except Exception as e:
        return HttpResponse(
            f"Error en emergency_debug: {str(e)}",
            content_type='text/plain; charset=utf-8',
            status=500
        )