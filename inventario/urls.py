from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario_list, name="inventario"),
    path('detalle/<id>', views.detalle_list),
]