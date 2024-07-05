from django.contrib import admin

from auxiliares.models import Auxiliar, AuxiliarGiro, Cargo, Comuna, ContactoAuxiliar, Giro, TipoAuxiliar

class TipoAuxiliarAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(TipoAuxiliar, TipoAuxiliarAdmin)

class CargoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(Cargo, CargoAdmin)

class GiroAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(Giro, GiroAdmin)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", )

admin.site.register(Comuna, ComunaAdmin)

class AuxiliarAdmin(admin.ModelAdmin):
    list_display = ("rut_auxiliar", "dv", "razon_social", "tipo_auxiliar", "telefono", )

admin.site.register(Auxiliar, AuxiliarAdmin)

class ContactoAuxiliarAdmin(admin.ModelAdmin):
    list_display = ("rut_auxiliar", "dv", "nombres", "apellidos", "telefono", "tipo_auxiliar", )

admin.site.register(ContactoAuxiliar, ContactoAuxiliarAdmin)

class AuxiliarGiroAdmin(admin.ModelAdmin):
    list_display = ("rut_auxiliar", "giro", )

admin.site.register(AuxiliarGiro, AuxiliarGiroAdmin)

