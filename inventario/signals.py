from django.db.models.signals import post_save, pre_delete, post_migrate
from django.dispatch import receiver
from django.apps import apps

from inventario.models import DetalleMovimiento

@receiver(post_save, sender=DetalleMovimiento)
def actualizar_stock(sender, instance, created, **kwargs):
    if created:
        id_tipo_movimiento = instance.movimiento.tipo_movimiento.id
        
        sucursal_producto = instance.sucursal_producto
        
        if id_tipo_movimiento == 1:  # Compra
            sucursal_producto.cantidad += instance.cantidad
        elif id_tipo_movimiento in [2, 3, 4, 5]:  # Venta
            sucursal_producto.cantidad -= instance.cantidad
        
        sucursal_producto.save()

""" @receiver(pre_delete, sender=DetalleMovimiento)
def revertir_stock(sender, instance, **kwargs):
    id_tipo_movimiento = instance.movimiento.tipo_movimiento.id

    sucursal_producto = instance.sucursal_producto
    
    if id_tipo_movimiento == 1:  # Compra
        sucursal_producto.cantidad -= instance.cantidad
    elif id_tipo_movimiento in [2, 3, 4, 5]:  # Venta
        sucursal_producto.cantidad += instance.cantidad
    
    sucursal_producto.save() """


@receiver(post_migrate)
def cargar_datos_por_defecto(sender, **kwargs):
    if sender.name == 'inventario':
        CStateMovimiento = apps.get_model('inventario', 'CStateMovimiento')
        TipoMovimiento = apps.get_model('inventario', 'TipoMovimiento')

        states = [
            {'nombre': 'Activo'},
            {'nombre': 'Anulado'}
        ]

        types = [
            {'nombre': 'Compra', 'descripcion': 'Compra Satisfactoria.'},
            {'nombre': 'Venta', 'descripcion': 'Venta Satisfactoria.'},
            {'nombre': 'Extravio', 'descripcion': 'Extravio de Producto.'},
            {'nombre': 'Merma', 'descripcion': 'Producto en mal estado o vencido.'},
            {'nombre': 'Consumo_intrerno', 'descripcion': 'Producto en consumo para personal.'}
        ]

        for state in states:
            CStateMovimiento.objects.get_or_create(nombre=state['nombre'])

        for type in types:
            TipoMovimiento.objects.get_or_create(nombre=type['nombre'], defaults={'descripcion': type['descripcion']})

