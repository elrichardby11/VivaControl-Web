from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def cargar_datos_por_defecto(sender, **kwargs):
    if sender.name == 'administrador':
        MetodosPago = apps.get_model('administrador', 'MetodosPago')

        methods = [
            {'nombre': 'Debito', 'descripcion': 'Tarjeta Debito Uso General'},
            {'nombre': 'Credito', 'descripcion': 'Tarjeta Credito Uso General'},
            {'nombre': 'Efectivo', 'descripcion': 'Efectivo, dinero en mano'},
            {'nombre': 'Junaeb - Edenred', 'descripcion': 'La Tarjeta Junaeb establece Edenred como único proveedor'},
        ]

        for method in methods:
            MetodosPago.objects.get_or_create(nombre=method['nombre'], defaults={'descripcion': method['descripcion']})

