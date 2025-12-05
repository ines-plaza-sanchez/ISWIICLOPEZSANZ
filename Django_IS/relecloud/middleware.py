"""
Middleware de debug temporal para Azure
"""

import logging

logger = logging.getLogger(__name__)

class AzureDebugMiddleware:
    """Middleware para debuggear peticiones en Azure"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log información de la petición entrante
        print(f"🔍 PETICIÓN ENTRANTE: {request.method} {request.path}")
        print(f"🔍 HOST: {request.get_host()}")
        print(f"🔍 SECURE: {request.is_secure()}")
        print(f"🔍 HEADERS importantes:")
        for header in ['HTTP_HOST', 'HTTP_X_FORWARDED_HOST', 'HTTP_X_FORWARDED_PROTO']:
            if header in request.META:
                print(f"🔍   {header}: {request.META[header]}")
        
        # Procesar la petición
        try:
            response = self.get_response(request)
            print(f"🔍 RESPUESTA: {response.status_code}")
            return response
        except Exception as e:
            print(f"🔍 ERROR EN MIDDLEWARE: {str(e)}")
            raise