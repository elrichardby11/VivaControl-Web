from django.urls import path
from . import views

urlpatterns = [
    path("metodos-pago", views.metodos_pago, name="metodos_pago"),
    path("sucursales", views.sucursales, name="sucursales"),
    path("agregar_sucursal/", views.agregar_sucursal, name="agregar_sucursal"),
    path("eliminar_sucursal/<id>", views.eliminar_sucursal, name="eliminar_sucursal"),
    path("editar_sucursal/<id_sucursal>", views.editar_sucursal, name="editar_sucursal"),
]
