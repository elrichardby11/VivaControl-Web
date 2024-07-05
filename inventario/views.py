from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CStateMovimiento, Movimiento, TipoMovimiento
from django.core.paginator import Paginator             

@login_required
def inventario_list(request):

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
    
    paginator = Paginator(movimientos, 5)  # Mostrar 5 elementos por página
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

    return render(request, 'inventario.html', context)
