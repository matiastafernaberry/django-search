from django.db import models

# Create your models here.
class Busqueda(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    proyecto = models.CharField(max_length=100)
    busqueda = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    evaluacion = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
