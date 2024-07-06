from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from administrador.models import Sucursal
from .models import CStateMovimiento, DetalleMovimiento, Movimiento, SucursalProducto, TipoMovimiento
from django.core.paginator import Paginator             

@login_required
def movement_list(request):

    # Capturando los parámetros de busqueda
    search_query = request.GET.get('search', '')
    tipo_query = request.GET.get('tipo', '')
    estado_query = request.GET.get('estado', '')

    movimientos = Movimiento.objects.all()

    if search_query:
        movimientos = movimientos.filter(auxiliar__rut_auxiliar__contains = search_query)

    if tipo_query:
        movimientos = movimientos.filter(tipo_movimiento = tipo_query)

    if estado_query:
        movimientos = movimientos.filter(cstate_movimiento = estado_query)
    
    paginator = Paginator(movimientos, 10)  # Mostrar 5 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tipos = TipoMovimiento.objects.all()
    estados = CStateMovimiento.objects.all()

    context = {
        'page_obj': page_obj,
        'tipos': tipos,
        'estados': estados,
        'search_query': search_query,
        'tipo_query': tipo_query,
        'estado_query': estado_query,
    }

    return render(request, 'movimientos.html', context)

@login_required
def detail_list(request, id):
    detalle = DetalleMovimiento.objects.get(movimiento=id)

    return render(request, 'detalle.html', context={"detalle": detalle})

@login_required
def inventory_list(request):

    # Capturando los parámetros de busqueda
    search_query = request.GET.get('search', '')
    local_query = request.GET.get('local', '')

    inventarios = SucursalProducto.objects.all()

    if search_query:
        inventarios = inventarios.filter(id_producto__id_producto__contains = search_query)

    if local_query:
        inventarios = inventarios.filter(id_sucursal = local_query)

    paginator = Paginator(inventarios, 10)  # Mostrar 5 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    locales = Sucursal.objects.all()

    context = {
        'page_obj': page_obj,
        'locales': locales,
        'search_query': search_query,
        'local_query': local_query,
    }

    return render(request, 'inventario.html', context)