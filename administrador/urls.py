from django.urls import path
from . import views

urlpatterns = [
    path('metodos-pago', views.metodos_pago, name="metodos_pago"),
]