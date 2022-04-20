from django.contrib import admin
from hello.models import Busqueda, ResultadoBusqueda

# Register your models here.
class BusquedaAdmin(admin.ModelAdmin):
    list_display= ('when', 'proyecto', 'busqueda', 'pais')

class ResultadoBusquedaAdmin(admin.ModelAdmin):
    list_display= ('when', 'fecha_modificacion', 'busqueda', 'url', 'evaluacion', 'puntaje', 'idstring')



admin.site.register(Busqueda, BusquedaAdmin)
admin.site.register(ResultadoBusqueda, ResultadoBusquedaAdmin)
