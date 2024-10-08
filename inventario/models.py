from django.db import models

from administrador.models import MetodosPago, Sucursal
from auxiliares.models import Auxiliar
from productos.models import Producto

class CStateMovimiento(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class PagoMovimiento(models.Model):
    id_pago = models.IntegerField()
    metodo = models.ForeignKey(MetodosPago, on_delete=models.CASCADE, default=None)
    monto = models.IntegerField()

    class Meta:
        unique_together = (('id_pago', 'metodo'),)

    def __str__(self):
        return f"Pago {self.id_pago} - {self.metodo.nombre}"

class TipoMovimiento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    fecha = models.DateField()
    periodo = models.IntegerField()
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)
    cstate_movimiento = models.ForeignKey(CStateMovimiento, on_delete=models.CASCADE)
    auxiliar = models.ForeignKey(Auxiliar, on_delete=models.CASCADE)  # Usando el modelo Auxiliar
    precio_total = models.IntegerField(blank=True, null=True)
    coste_total = models.IntegerField()
    pago = models.ForeignKey(PagoMovimiento, null=True, blank=True, on_delete=models.SET_NULL)  # Usando el modelo PagoMovimiento

    def __str__(self):
        return f"Movimiento: {self.id}"

class SucursalProducto(models.Model):
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    class Meta:
        unique_together = (('id_sucursal', 'id_producto'),)

    def __str__(self):
        return f"Producto: {self.id_producto} en Sucursal {self.id_sucursal}"

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    sucursal_producto = models.ForeignKey(SucursalProducto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    coste_unitario = models.IntegerField()

    class Meta:
        unique_together = (('movimiento', 'sucursal_producto'),)

    def __str__(self):
        return f"Detalle de Movimiento {self.movimiento.id} - Producto {self.sucursal_producto.id_producto}"
