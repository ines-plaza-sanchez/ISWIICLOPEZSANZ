# APP (relecloud)

from django.urls import path
from . import views
from . import debug_views
from . import simple_test
from . import emergency_views

urlpatterns = [
    # Vista de emergencia (debe ir PRIMERA)
    path('emergency/', emergency_views.emergency_debug, name='emergency_debug'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('destination/add/', views.DestinationCreateView.as_view(), name='destination_form'),
    path('destination/<int:pk>/update/', views.DestinationUpdateView.as_view(), name='destination_form'),
    path('destination/<int:pk>/delete/', views.DestinationDeleteView.as_view(), name='destination_confirm_delete'),
    path('destination/<int:pk>/review/', views.DestinationReviewCreateView.as_view(), name='destination_review'),
    path('cruise/<int:pk>/', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('cruise/<int:pk>/review/', views.CruiseReviewCreateView.as_view(), name='cruise_review'),
    path('info_request/', views.InfoRequestCreate.as_view(), name='info_request'),
    # Vistas de diagnóstico temporal
    path('debug/', debug_views.debug_info, name='debug_info'),
    path('simple/', simple_test.simple_test, name='simple_test'),
]