from django.db import models

from auxiliares.models import Comuna

class MetodosPago(models.Model):
    nombre = models.CharField(max_length=225)
    descripcion = models.CharField(max_length=225)

    def __str__(self):
        return self.nombre
    
class Sucursal(models.Model):
    id_sucursal = models.IntegerField(primary_key=True)
    direccion = models.CharField(max_length=255)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return self.direccion
