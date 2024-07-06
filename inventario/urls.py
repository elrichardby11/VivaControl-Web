from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name="inventario"),
    path('movimiento/', views.movement_list, name="movimiento"),
    path('movimiento/detalle/<id>', views.detail_list),
]