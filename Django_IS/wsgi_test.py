"""
Vista de diagnóstico ultra-simple que bypassa Django completamente
"""

def simple_wsgi_app(environ, start_response):
    """Aplicación WSGI simple que bypassa Django completamente"""
    
    # Obtener información del request
    method = environ.get('REQUEST_METHOD', 'UNKNOWN')
    path = environ.get('PATH_INFO', '/')
    host = environ.get('HTTP_HOST', 'unknown')
    
    # Crear respuesta HTML simple
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test WSGI Directo</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>✅ WSGI Funciona!</h1>
        <p><strong>Método:</strong> {method}</p>
        <p><strong>Ruta:</strong> {path}</p>
        <p><strong>Host:</strong> {host}</p>
        <hr>
        <h2>Variables de entorno de Azure:</h2>
        <ul>
    """
    
    # Agregar variables de entorno importantes
    azure_vars = [
        'WEBSITE_HOSTNAME',
        'DJANGO_SETTINGS_MODULE', 
        'SECRET_KEY',
        'PORT',
        'WEBSITE_SITE_NAME'
    ]
    
    for var in azure_vars:
        value = environ.get(var, 'No configurado')
        html_content += f"<li><strong>{var}:</strong> {value}</li>"
    
    html_content += """
        </ul>
        <hr>
        <p>Si ves esto, el problema NO es WSGI/Gunicorn, sino Django.</p>
    </body>
    </html>
    """
    
    # Configurar respuesta
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html_content.encode('utf-8'))))
    ]
    
    start_response(status, headers)
    return [html_content.encode('utf-8')]