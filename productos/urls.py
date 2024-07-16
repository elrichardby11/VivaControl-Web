from django.urls import path
from . import views

urlpatterns = [
    path('estados/', views.cstate_producto_list, name='cstate_producto'),
    path('estados/editar/<int:pk>/', views.cstate_edit, name='cstate_edit'),
    path('estados/eliminar/<int:pk>/', views.cstate_delete, name='cstate_delete'),

    path('categorias/', views.categoria_list, name='categorias'),
    path('categoria/editar/<int:pk>/', views.categoria_edit, name='categoria_edit'),
    path('categoria/eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),
    
    path('', views.producto_list, name='productos'),
    path('editar/<int:pk>/', views.producto_edit, name='producto_edit'),
    path('eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
]
