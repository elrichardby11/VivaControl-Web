from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name="inventario"),
    path('editar_inventario/<str:id_producto>/<str:id_sucursal>', views.edit_inventory, name="editar_inventario"),
    path('punto/', views.puntos, name='puntos'),
    path('punto/venta/', views.punto_venta, name='punto_venta'),
    path('punto/<str:contexto>/editar/<str:codigo_barras>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('punto/<str:contexto>/eliminar/<str:code>/', views.eliminar_producto_carrito, name='eliminar_p_carrito'),
    path('punto/<str:contexto>/confirmar', views.confirmar, name='punto_confirmacion'),
    path('punto/compra/', views.punto_compra, name='punto_compra'),
    path('punto/compra/actualizar/<str:code>/', views.update_button, name='update_button'),
    path('punto/otros/', views.punto_otros, name='punto_otros'),
    path('movimiento/', views.movement_list, name="movimiento"),
    path('movimiento/detalle/<id>', views.detail_list, name="ver_detalle"),
    path('movimiento/detalle/boleta/<id>', views.ticket_view, name="ver_boleta"),
]