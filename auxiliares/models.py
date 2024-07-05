from django.db import models

class TipoAuxiliar(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=225)

    def __str__(self):
        return self.nombre

class Giro(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Auxiliar(models.Model):
    rut_auxiliar = models.IntegerField(primary_key=True)
    dv = models.IntegerField()
    razon_social = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50)
    sitio_web = models.URLField(max_length=50, blank=True)
    fecha_inicio_acuerdo = models.DateField()
    telefono = models.IntegerField(blank=True)
    activo = models.BooleanField()
    tipo_auxiliar = models.ForeignKey(TipoAuxiliar, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return self.razon_social or self.rut_auxiliar

class ContactoAuxiliar(models.Model):
    rut_auxiliar = models.ForeignKey(Auxiliar, on_delete=models.CASCADE)
    dv = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50, blank=True)
    telefono = models.IntegerField()
    tipo_auxiliar = models.ForeignKey(TipoAuxiliar, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class AuxiliarGiro(models.Model):
    rut_auxiliar = models.ForeignKey(Auxiliar, on_delete=models.CASCADE)
    giro = models.ForeignKey(Giro, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('rut_auxiliar', 'giro'),)

    def __str__(self):
        return f"{self.rut_auxiliar} - {self.giro.nombre}"
