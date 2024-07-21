from django.contrib import admin

from inventario.models import CStateMovimiento, DetalleMovimiento, Movimiento, PagoMovimiento, SucursalProducto, TipoMovimiento

class CStateMovimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(CStateMovimiento, CStateMovimientoAdmin)

class PagoMovimientoAdmin(admin.ModelAdmin):
    list_display = ("id_pago", "metodo", "monto", )

admin.site.register(PagoMovimiento, PagoMovimientoAdmin)

class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(TipoMovimiento, TipoMovimientoAdmin)

class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("auxiliar", "tipo_movimiento", "coste_total", "precio_total", "fecha", )

admin.site.register(Movimiento, MovimientoAdmin)

class SucursalProductoAdmin(admin.ModelAdmin):
    list_display = ("id_sucursal", "id_producto", "cantidad", )

admin.site.register(SucursalProducto, SucursalProductoAdmin)

class DetalleMovimientoAdmin(admin.ModelAdmin):
    list_display = ("movimiento", "sucursal_producto", "cantidad", "precio_unitario", "coste_unitario")

admin.site.register(DetalleMovimiento, DetalleMovimientoAdmin)