from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name="inventario"),
    path('editar_inventario/<str:id_producto>/<str:id_sucursal>', views.edit_inventory, name="editar_inventario"),
    path('eliminar_inventario/<str:id_producto>/<str:id_sucursal>', views.delete_inventory, name="eliminar_inventario"),
    path('punto/', views.puntos, name='puntos'),
    path('punto/venta/', views.punto_venta, name='punto_venta'),
    path('punto/venta/editar/<str:codigo_barras>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('punto/venta/eliminar/<str:code>/', views.eliminar_producto_carrito, name='eliminar_p_carrito'),
    path('punto/venta/pagar/', views.punto_venta_pagar, name='punto_venta_pagar'),
    path('punto/compra/', views.punto_compra, name='punto_compra'),
    path('punto/otros/', views.punto_otros, name='punto_otros'),
    path('movimiento/', views.movement_list, name="movimiento"),
    path('movimiento/detalle/<id>', views.detail_list),
]