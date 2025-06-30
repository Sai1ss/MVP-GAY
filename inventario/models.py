from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

class ElementoInventario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    numero_serie = models.CharField(max_length=50, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    ubicacion = models.CharField(max_length=100)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"

class RecepcionCompra(models.Model):
    elemento = models.ForeignKey(ElementoInventario, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.elemento.stock_actual += self.cantidad
        self.elemento.save()
        super().save(*args, **kwargs)
