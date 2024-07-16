from django import forms
from .models import Producto, Categoria, CStateProducto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cstate_producto', 'categoria']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class CStateProductoForm(forms.ModelForm):
    class Meta:
        model = CStateProducto
        fields = ['nombre']
