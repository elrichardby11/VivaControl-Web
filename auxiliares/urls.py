from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.auxiliares, name="auxiliares"),
    path('registrar_auxiliares/', views.registrar_auxiliar, name="registrar_auxiliar"),
    path('editar_auxiliar/<rut_auxiliar>', views.editar_auxiliar, name="editar_auxiliar"),
    path('eliminar_auxiliar/<rut_auxiliar>', views.eliminar_auxiliar, name="eliminar_auxiliar"),
    path('tipos/', views.list_types, name='tipos'),
    path('tipos/guardar_tipos/', views.guardar_tipo),
    path('tipos/editar_tipo/<id>', views.editar_tipos, name='editar_tipo'),
    path('tipos/eliminar_tipo/<id>', views.eliminar_tipos, name='eliminar_tipo'),
    path('comunas/', views.listar_comunas, name='comunas'),
    path('comunas/guardar_comuna/', views.guardar_comunas, name='guardar_comuna'),
    path('comunas/editar_comuna/<id>', views.editar_comunas, name='editar_comunas'),
    path('comunas/eliminar_comuna/<id>', views.eliminar_comunas, name='eliminar_comuna')
]
