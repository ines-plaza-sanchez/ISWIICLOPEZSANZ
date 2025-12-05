"""
Vistas de diagnóstico temporal para Azure
"""
import os
from django.http import JsonResponse
from django.conf import settings


def debug_info(request):
    """Vista para mostrar información de diagnóstico"""
    
    debug_data = {
        'request_info': {
            'method': request.method,
            'path': request.path,
            'host': request.get_host(),
            'is_secure': request.is_secure(),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'No disponible'),
        },
        'django_settings': {
            'DEBUG': settings.DEBUG,
            'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
            'SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE', 'No configurado'),
        },
        'azure_info': {
            'WEBSITE_HOSTNAME': os.environ.get('WEBSITE_HOSTNAME', 'No es Azure'),
            'PORT': os.environ.get('PORT', 'No configurado'),
            'WEBSITE_SITE_NAME': os.environ.get('WEBSITE_SITE_NAME', 'No configurado'),
        },
        'static_settings': {
            'STATIC_URL': settings.STATIC_URL,
            'STATIC_ROOT': str(getattr(settings, 'STATIC_ROOT', 'No configurado')),
            'STATICFILES_DIRS': [str(d) for d in getattr(settings, 'STATICFILES_DIRS', [])],
        },
        'middleware': settings.MIDDLEWARE,
        'installed_apps': settings.INSTALLED_APPS,
    }
    
    return JsonResponse(debug_data, indent=2)