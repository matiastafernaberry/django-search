from django.db import models

# Create your models here.
class Busqueda(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    proyecto = models.CharField(max_length=100)
    busqueda = models.CharField(max_length=100)
    tipobusqueda = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)


class ResultadoBusqueda(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    fecha_modificacion = models.DateTimeField("fecha modificacion")
    busqueda = models.ForeignKey(Busqueda, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    evaluacion = models.CharField(max_length=100)
    puntaje = models.FloatField(null=True, blank=True, default=None)
    posicion = models.IntegerField(blank=True, null=True)
    idstring = models.CharField(max_length=500)
    titulo = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=500)