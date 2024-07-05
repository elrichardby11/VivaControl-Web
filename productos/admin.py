from django.contrib import admin

from productos.models import CStateProducto, Categoria, Producto, SucursalProducto

class CStateProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(CStateProducto, CStateProductoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(Categoria, CategoriaAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id_producto", "nombre", "categoria", )

admin.site.register(Producto, ProductoAdmin)

class SucursalProductoAdmin(admin.ModelAdmin):
    list_display = ("id_sucursal", "id_producto", "cantidad", )

admin.site.register(SucursalProducto, SucursalProductoAdmin)

