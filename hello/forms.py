from django.forms import ModelForm
from hello.models import Busqueda
from django import forms

class BusquedaForm(forms.ModelForm):
    proyecto = forms.CharField(max_length=100, help_text='100 characters max.', required=False)
    busqueda = forms.CharField(max_length=100, help_text='100 characters max.', required=False)
    pais = forms.CharField(max_length=100, help_text='100 characters max.', required=False)
    evaluacion = forms.CharField(max_length=100, help_text='100 characters max.', required=False)
    class Meta:
        model = Busqueda
        exclude = ()