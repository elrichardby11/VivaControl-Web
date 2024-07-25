import glob
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from administrador.models import Sucursal, MetodosPago
from inventario.utils import save_ticket
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
    

    paginator = Paginator(movimientos.order_by('-id'), 10)  # Mostrar 10 elementos por página
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

    return render(request, 'detalle.html', context={"detalles": detalles,
                                                    "id": id})

@login_required
def ticket_view(request, id):
    # Usar glob para encontrar el archivo que coincide con el patrón
    file_pattern = f"inventario/boletas/{id}__*.txt"
    file_list = glob.glob(file_pattern)

    # Verificar si se encontró algún archivo
    if not file_list:
        return render(request, "boleta.html", {"error": "Boleta no encontrada", "id": id})

    # Asumir que se encontró el primer archivo que coincide con el patrón
    file_path = file_list[0]

    try:
        with open(file_path, "r") as file:
            boleta_content = file.read()
    except IOError:
        return render(request, "boleta.html", {"error": "No se pudo leer la boleta", "id": id})

    return render(request, "boleta.html", {"boleta_content": boleta_content, "id": id})


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

    paginator = Paginator(inventarios.order_by('-id'), 10)  # Mostrar 10 elementos por página
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

def edit_inventory(request, id_sucursal, id_producto):

    if request.method == "POST":
        cantidad = request.POST["txtCantidad"]
        precio = request.POST["txtPrecio"]

        try:
            inventario = SucursalProducto.objects.get(id_producto=id_producto, id_sucursal=id_sucursal)
            inventario.cantidad = cantidad
            inventario.precio = precio
            
            inventario.save()

        except Exception as e:
            messages.error(request, e, "No se ha podido actualizar el inventario")
        
        else:
            messages.success(request, "El inventario se ha actualizado correctamente! ")

        finally:
            return redirect("inventario")

    inventario = SucursalProducto.objects.get(id_producto=id_producto, id_sucursal=id_sucursal)

    return render(request,
                  "editar_inventario.html",
                  context={"inventario": inventario,
                           })

def delete_inventory(request, id_producto, id_sucursal):
    inventario = SucursalProducto.objects.get(id_producto=id_producto, id_sucursal=id_sucursal)
    inventario.delete()
    messages.success(request, "Inventario eliminado correctamente! ")

    return redirect('inventario')

@login_required
def puntos(request):
    return render(request, 'puntos.html')

@login_required
def punto_venta(request):

    locales = Sucursal.objects.all()
    metodos = MetodosPago.objects.all()
    
    # Inicializar variables si no existen
    if 'cart' not in request.session:
        request.session['cart'] = {} 

    if ('local_query' not in request.session) or (request.session['cart'] == {}):
        request.session['local_query'] = ''

    if 'total_price' not in request.session:
        request.session['total_price'] = 0

    cart = request.session['cart']
    local_query = request.session['local_query']
    total_price = request.session['total_price']

    context = {
        "locales": locales,
        "metodos": metodos,
        "cart": cart,
        "local_query": local_query,
        "codigo_barras": request.GET.get('codigo_barras', ''),
        "total_price": total_price
    }

    if request.method == "GET":
        # Capturando los parámetros de la petición
        code_query = request.GET.get('codigo_barras', '')

        if 'codigo_barras' in request.GET or 'local' in request.GET:

            new_local_query = request.GET.get('local', '')

            if not new_local_query:
                messages.error(request, "Debe seleccionar un local primero.")
                return redirect('punto_venta')
            if cart and local_query and new_local_query != local_query:
                messages.error(request, "No se puede cambiar de local con productos en el carrito.")
                return redirect('punto_venta')
            if not code_query:
                messages.error(request, "Debe de añadir el código de barras.")
                return redirect('punto_venta')
            if not code_query.isdigit() or len(code_query) > 15:
                messages.error(request, "Debe de añadir un código de barras válido.")
                return redirect('punto_venta')

            # Actualizar local query de la sesion
            request.session['local_query'] = new_local_query

            products = SucursalProducto.objects.filter(id_sucursal=new_local_query)
            product = products.filter(id_producto=code_query).first()

            if not product:
                messages.error(request, "Producto no encontrado.")
                return render(request, 'punto_venta.html', context)

            quantity = product.cantidad
            if code_query in cart and cart[code_query]["quantity"] >= quantity:
                messages.error(request, "Producto fuera de stock.")
                return render(request, 'punto_venta.html', context)

            # Añadir o actualizar el producto en el carrito
            if code_query in cart:
                cart[code_query]["quantity"] += 1
                cart[code_query]["total"] = product.precio * cart[code_query]['quantity']
                cart[code_query]["max_quantity"] = product.cantidad

            else:
                cart[code_query] = {
                    "name": product.id_producto.nombre,
                    "price": product.precio,
                    "quantity": 1,
                    "total": product.precio,
                    "max_quantity": product.cantidad
                }
            
            total_price = 0
            for code in cart:
                total_price += int(cart[code]['total'])

            request.session['cart'] = cart
            request.session['local_query'] = new_local_query
            request.session['total_price'] = total_price
            
            context.update({
                "local_query": new_local_query,
                "codigo_barras": code_query,
                "total_price": total_price
            })

            messages.success(request, f"Producto encontrado: {product.id_producto.nombre}. Cantidad disponible: {quantity}.")
            return redirect('punto_venta')

    return render(request, 'punto_venta.html', context)

@login_required
def punto_venta_pagar(request):
    if request.method == "POST":
        # Obtener el total del carrito y el local seleccionado
        total_amount = request.session.get('total_price', 0)
        local_query = request.session.get('local_query', '')

        if not local_query:
            messages.error(request, "Por favor, selecciona una sucursal.")
            return redirect('punto_venta')

        if total_amount == 0:
            messages.error(request, "Por favor, agrega un producto.")
            return redirect('punto_venta')

        # Obtener el método de pago seleccionado
        payment_method_id = request.POST.get('metodo_pago')
        if not payment_method_id:
            messages.error(request, "Por favor, selecciona un método de pago.")
            return redirect('punto_venta')

        # Obtener el método de pago de la base de datos
        payment_method = MetodosPago.objects.filter(id=payment_method_id).first()

        if not payment_method:
            messages.error(request, "Método de pago no válido.")
            return redirect('punto_venta')

        # Procesar pago en efectivo
        if payment_method.nombre == "Efectivo":
            efectivo = request.POST.get('efectivo')

            if not efectivo or not efectivo.isdigit() or int(efectivo) < total_amount:
                messages.error(request, "Por favor, verifica el monto en efectivo.")
                return redirect('punto_venta')

            vuelto = int(efectivo) - total_amount

            print("vuelto", vuelto)

            # Guardar detalles de pago en la base de datos
            current_cart = request.session.get('cart', {})
            save_ticket(request, current_cart, total_amount, payment_method, local_query, efectivo)

            # Vaciar carrito después del pago
            clear_cart(request)

            messages.success(request, "Pago realizado con éxito.")
            return redirect('punto_venta')  

        current_cart = request.session.get('cart', {})
        # Actualizar siguiente funcion
        save_ticket(request, current_cart, total_amount, payment_method, local_query)

        clear_cart(request)

        messages.success(request, "Pago realizado con éxito.")
        return redirect('punto_venta')

    return redirect('punto_venta')

@login_required
def actualizar_cantidad_carrito(request, codigo_barras):
    if request.method != "POST":
        return redirect('punto_venta')

    if not request.POST.get("cantidad").isdigit():
        messages.error(request, "Ingrese una cantidad válida.")
        return redirect('punto_venta')

    if not request.session['local_query']:
        messages.error(request, "Error al obtener local.")
        return redirect('punto_venta')

    local_query = request.session['local_query']
    nueva_cantidad = int(request.POST.get("cantidad"))
    cart = request.session.get('cart', {})

    if codigo_barras not in cart:
        messages.error(request, "Producto no encontrado en el carrito.")
        return redirect('punto_venta')

    producto = SucursalProducto.objects.filter(id_producto=codigo_barras, id_sucursal=local_query).first()
    if not producto or nueva_cantidad > producto.cantidad:
        messages.error(request, f"Cantidad fuera de stock. Cantidad disponible: {cart[codigo_barras]['max_quantity']}")
        return redirect('punto_venta')
  
    cart[codigo_barras]["quantity"] = nueva_cantidad
    cart[codigo_barras]["total"] = cart[codigo_barras]["price"] * nueva_cantidad

    # Recalcular el total del precio
    total_price = sum(item["total"] for item in cart.values())
    request.session['total_price'] = total_price
    request.session['cart'] = cart

    messages.success(request, "Cantidad actualizada correctamente.")
    return redirect('punto_venta')

@login_required
def punto_compra(request):
    return render(request, 'punto_compra.html')

@login_required
def punto_otros(request):
    return render(request, 'punto_otros.html')

@login_required
def eliminar_producto_carrito(request, code):
    cart = request.session.get('cart', {})
    total_price = request.session.get('total_price', 0)
    
    if code not in cart:
        messages.success(request, "El producto no se encuentra en el carrito.")
        return redirect('punto_venta')

    total_price -= int(cart[code]['total'])
    del cart[code]
    request.session['cart'] = cart
    request.session['total_price'] = total_price
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('punto_venta')

@login_required
def clear_cart(request):
    # Vacía el carrito de compras y restablece la sesión
    
    # Eliminar el carrito de la sesión
    request.session['cart'] = {}
    request.session['total_price'] = 0
    request.session['local_query'] = ''

    messages.success(request, "Carrito vacío exitosamente.")
    return redirect('punto_venta')
