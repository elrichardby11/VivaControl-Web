from django.contrib import admin

from inventario.models import CStateMovimiento, DetalleMovimiento, Movimiento, PagoMovimiento, TipoMovimiento

class CStateMovimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(CStateMovimiento, CStateMovimientoAdmin)

class PagoMovimientoAdmin(admin.ModelAdmin):
    list_display = ("id_pago", "monto", )

admin.site.register(PagoMovimiento, PagoMovimientoAdmin)

class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(TipoMovimiento, TipoMovimientoAdmin)

class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("auxiliar", "tipo_movimiento", "coste_total", "precio_total", "fecha", )

admin.site.register(Movimiento, MovimientoAdmin)

class DetalleMovimientoAdmin(admin.ModelAdmin):
    list_display = ("movimiento", "id_producto", "id_sucursal", "cantidad", )

admin.site.register(DetalleMovimiento, DetalleMovimientoAdmin)