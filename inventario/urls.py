from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name="inventario"),
    path('punto/', views.puntos, name='puntos'),
    path('punto/venta/', views.punto_venta, name='punto_venta'),
    path('punto/venta/editar/<str:code>/', views.editar_producto_carrito, name='editar_p_carrito'),
    path('punto/venta/eliminar/<str:code>/', views.eliminar_producto_carrito, name='eliminar_p_carrito'),
    path('punto/compra/', views.punto_compra, name='punto_compra'),
    path('punto/otros/', views.punto_otros, name='punto_otros'),
    path('movimiento/', views.movement_list, name="movimiento"),
    path('movimiento/detalle/<id>', views.detail_list),
]