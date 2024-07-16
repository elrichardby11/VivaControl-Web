from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from .models import CStateProducto, Categoria, Producto
from .forms import CStateProductoForm, CategoriaForm, ProductoForm
from django.urls import reverse_lazy

# Vista para la página de estado de producto
def cstate_producto_list(request):
    estados = CStateProducto.objects.all()
    if request.method == 'POST':
        form = CStateProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cstate_producto')
    else:
        form = CStateProductoForm()
    return render(request, 'cstate_producto.html', {'estados': estados, 'form': form})

class EstadoProductoCreateView(FormView):
    template_name = 'cstate_producto.html'
    form_class = CStateProductoForm
    success_url = reverse_lazy('cstate_producto')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def cstate_edit(request, pk):
    estado_producto = get_object_or_404(CStateProducto, pk=pk)
    if request.method == 'POST':
        form = CStateProductoForm(request.POST, instance=estado_producto)
        if form.is_valid():
            form.save()
            return redirect('cstate_producto') # Redirigir a la lista de estados
    else:
        form = CStateProductoForm(instance=estado_producto)
    return render(request, 'cstate_edit.html', {'form': form})

def cstate_delete(request, pk):
    estado_producto = get_object_or_404(CStateProducto, pk=pk)
    if request.method == 'POST':
        estado_producto.delete()
        return redirect('cstate_producto') # Redirigir a la lista de estados
    return render(request, 'cstate_delete.html', {'estado': estado_producto})

# Vista para la página de categoría
def categoria_list(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categoria.html', {'categorias': categorias, 'form': form})

def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')  # Redirige a la lista de categorías
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria_edit.html', {'form': form, 'categoria': categoria})

def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')  # Redirige a la lista de categorías
    return render(request, 'categoria_delete.html', {'categoria': categoria})

# Vista para la página de producto
def producto_list(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'producto.html', {'productos': productos, 'form': form})

def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')  # Redirige a la lista de productos
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto_edit.html', {'form': form, 'producto': producto})

def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')  # Redirige a la lista de productos
    return render(request, 'producto_delete.html', {'producto': producto})
