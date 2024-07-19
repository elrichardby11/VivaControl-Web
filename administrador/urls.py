from django.urls import path
from . import views

urlpatterns = [
    path("metodos-pago", views.metodos_pago, name="metodos_pago"),
    path("metodos-pago/agregar_metodo/", views.agregar_metodo, name="agregar_metodo"),
    path("metodos-pago/editar_metodo/<int:id>", views.editar_metodo, name="editar_metodo"),
    path("metodos-pago/eliminar_metodo/<int:id>", views.eliminar_metodo, name="eliminar_metodo"),
    path("sucursales", views.sucursales, name="sucursales"),
    path("agregar_sucursal/", views.agregar_sucursal, name="agregar_sucursal"),
    path("eliminar_sucursal/<id>", views.eliminar_sucursal, name="eliminar_sucursal"),
    path("editar_sucursal/<id_sucursal>", views.editar_sucursal, name="editar_sucursal"),
]
