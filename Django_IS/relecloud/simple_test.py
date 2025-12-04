"""
Vista de prueba minimalista para diagnosticar el error 400
"""
from django.http import HttpResponse

def simple_test(request):
    """Vista más simple posible para probar si Django funciona"""
    return HttpResponse("¡Django funciona! Esta es una prueba simple.")