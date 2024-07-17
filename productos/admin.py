from django.contrib import admin

from productos.models import CStateProducto, Categoria, Producto

class CStateProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(CStateProducto, CStateProductoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(Categoria, CategoriaAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id_producto", "nombre", "cstate_producto", "categoria", )

admin.site.register(Producto, ProductoAdmin)
