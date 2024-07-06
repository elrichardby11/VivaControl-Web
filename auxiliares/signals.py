from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def cargar_datos_por_defecto(sender, **kwargs):
    if sender.name == 'auxiliares':
        TipoAuxiliar = apps.get_model('auxiliares', 'TipoAuxiliar')
        Cargo = apps.get_model('auxiliares', 'Cargo')

        positions = [
            {'nombre': 'Administrador', 'descripcion': 'Persona encargado de administrar toda la empresa, tiene todos los permisos.'},
            {'nombre': 'Cajero', 'descripcion': 'Persona encargado de atender al publico con punto de venta.'},
            {'nombre': 'Supervisor', 'descripcion': 'Persona encargado de supervisar productos, auxiliares, etc.'},
            {'nombre': 'Inventario', 'descripcion': 'Persona encargado de realizar ventas, compras de reposicion y encargado de actualizar precios y proveedores.'},
            {'nombre': 'Atencion_Cliente', 'descripcion': 'Persona encargado de ateneder al cliente, pudiendo revisar sus datos generales y de contacto.'},
            {'nombre': 'Vendedor', 'descripcion': 'Persona encargado de vender productos o servicios.'},
        ]

        types = [
            {'nombre': 'Proveedor', 'descripcion': 'Entidad o empresa que suministra productos'},
            {'nombre': 'Cliente', 'descripcion': 'Individuos o empresas que adquieren productos'},
            {'nombre': 'Empleado', 'descripcion': 'Personas que trabajan para la empresa y desempeñan una variedad de roles y funciones'},
            {'nombre': 'Socio', 'descripcion': 'Individuos o empresas que colaboran estrechamente con el negocio para alcanzar objetivos mutuos'},
            {'nombre': 'Distribuidor', 'descripcion': 'Ayudan a llevar tus productos o servicios al mercado'},
            {'nombre': 'Otros', 'descripcion': 'Cualquier otro individuo o empresa que no esté desclarado'}
        ]

        for position in positions:
            Cargo.objects.get_or_create(nombre=position['nombre'], defaults={'descripcion': position['descripcion']})

        for type in types:
            TipoAuxiliar.objects.get_or_create(nombre=type['nombre'], defaults={'descripcion': type['descripcion']})

