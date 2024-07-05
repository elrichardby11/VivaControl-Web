from django.contrib import admin

from administrador.models import MetodosPago, Sucursal

class MetodosPagoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(MetodosPago, MetodosPagoAdmin)

class SucursalAdmin(admin.ModelAdmin):
    list_display = ("id_sucursal", "direccion", )

admin.site.register(Sucursal, SucursalAdmin)
