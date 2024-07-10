from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from administrador.models import Sucursal, MetodosPago
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
    detalles = DetalleMovimiento.objects.filter(movimiento=id)

    return render(request, 'detalle.html', context={"detalles": detalles})

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

    paginator = Paginator(inventarios, 10)  # Mostrar 10 elementos por página
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

def puntos(request):
    return render(request, 'puntos.html')

def punto_venta(request):

    locales = Sucursal.objects.all()
    metodos = MetodosPago.objects.all()
    
    # Inicializar el carrito si no existe
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    local_query = request.GET.get('local', '')
    code_query = request.GET.get('codigo_barras', '')

    context = {
        "locales": locales,
        "metodos": metodos,
        "cart": cart,
        "local_query": local_query,
        "codigo_barras": code_query
    }

    if request.method == "GET":
        # Capturando los parámetros de la petición
        # code_query = request.GET.get('codigo_barras', '')
        # local_query = request.GET.get('local', '')

        if 'codigo_barras' in request.GET or 'local' in request.GET:

            # context.update({
            #     "local_query": local_query,
            #     "codigo_barras": code_query
            # })

            if not local_query:
                messages.error(request, "Debe seleccionar un local primero.")
                return render(request, 'punto_venta.html', context)
            if not code_query:
                messages.error(request, "Debe de añadir el código de barras.")
                return render(request, 'punto_venta.html', context)
            if not code_query.isdigit() or len(code_query) > 15:
                messages.error(request, "Debe de añadir un código de barras válido.")
                return render(request, 'punto_venta.html', context)

            products = SucursalProducto.objects.filter(id_sucursal=local_query)
            product = products.filter(id_producto=code_query).first()

            if not product:
                messages.error(request, "Producto no encontrado.")
                return render(request, 'punto_venta.html', context)

            quantity = product.cantidad
            if quantity < 1:
                messages.error(request, "Producto fuera de stock.")
                return render(request, 'punto_venta.html', context)

            # Añadir o actualizar el producto en el carrito
            if code_query in cart:
                cart[code_query]["quantity"] += 1
            else:
                cart[code_query] = {
                    "name": product.id_producto.nombre,
                    "price": product.precio,
                    "quantity": 1
                }

            request.session['cart'] = cart
            messages.success(request, f"Producto encontrado: {product.id_producto.nombre}. Cantidad disponible: {quantity}.")

    return render(request, 'punto_venta.html', context)

def punto_compra(request):
    return render(request, 'punto_compra.html')

def punto_otros(request):
    return render(request, 'punto_otros.html')

def eliminar_producto_carrito(request, code, local_query):
    cart = request.session.get('cart', {})
    if code in cart:
        del cart[code]
        request.session['cart'] = cart
        messages.success(request, "Producto eliminado del carrito.")
        
    else:
        messages.success(request, "el producto no se encuentra en el carrito.")

    # Pasar los datos necesarios al contexto
    locales = Sucursal.objects.all()
    metodos = MetodosPago.objects.all()
    context = {
        "locales": locales,
        "metodos": metodos,
        "cart": cart,
        "local_query": local_query,
        "codigo_barras": request.GET.get('codigo_barras', '')
    }

    return render(request, 'punto_venta.html', context)
