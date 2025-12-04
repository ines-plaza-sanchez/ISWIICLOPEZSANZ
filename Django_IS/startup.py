#!/usr/bin/env python3
"""
Script de inicio para Azure App Service
Este script se ejecuta cuando se inicia la aplicación en Azure
"""

import os
import subprocess
import sys

def main():
    """Función principal de inicio"""
    
    print("=== INICIO DEL SCRIPT DE AZURE ===")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Establecer el módulo de configuración (detección automática en settings.py)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    print(f"DJANGO_SETTINGS_MODULE configurado a: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Mostrar variables de entorno importantes
    print(f"WEBSITE_HOSTNAME: {os.environ.get('WEBSITE_HOSTNAME', 'No configurado')}")
    print(f"PORT: {os.environ.get('PORT', 'No configurado')}")
    
    # Ejecutar migraciones automáticamente - TEMPORAL: COMENTADO
    print("SALTANDO migraciones temporalmente...")
    # try:
    #     subprocess.run([
    #         sys.executable, 'manage.py', 'migrate', '--noinput'
    #     ], check=True)
    #     print("Migraciones completadas exitosamente.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error en migraciones: {e}")
    
    # Recopilar archivos estáticos - SOLO SI NO EXISTEN
    staticfiles_dir = os.path.join(os.getcwd(), 'staticfiles')
    if not os.path.exists(staticfiles_dir) or len(os.listdir(staticfiles_dir)) < 10:
        print("Recopilando archivos estáticos...")
        try:
            subprocess.run([
                sys.executable, 'manage.py', 'collectstatic', '--noinput'
            ], check=True)
            print("Archivos estáticos recopilados exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error recopilando archivos estáticos: {e}")
    else:
        print("Archivos estáticos ya existen, saltando collectstatic.")
    
    print("Configuración de inicio completada.")
    
    # Iniciar el servidor Django con Gunicorn
    print("Iniciando servidor Django...")
    port = os.environ.get('PORT', '8000')
    print(f"Iniciando en puerto: {port}")
    
    subprocess.run([
        'gunicorn', 
        '--bind', f'0.0.0.0:{port}',
        '--workers', '3',
        '--timeout', '600',
        'project.wsgi:application'
    ], check=False)  # check=False porque queremos que el proceso continue corriendo

if __name__ == '__main__':
    main()