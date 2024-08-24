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
        precio = request.POST["txtPrecio"]

        try:
            inventario = SucursalProducto.objects.get(id_producto=id_producto, id_sucursal=id_sucursal)
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

@login_required
def puntos(request):
    return render(request, 'puntos.html')

@login_required
def punto_venta(request):
    locales = Sucursal.objects.all()
    metodos = MetodosPago.objects.all()
    
    # Inicializar variables si no existen
    if 'venta_cart' not in request.session:
        request.session['venta_cart'] = {} 

    if ('venta_local_query' not in request.session) or (request.session['venta_cart'] == {}):
        request.session['venta_local_query'] = ''

    if 'venta_total_price' not in request.session:
        request.session['venta_total_price'] = 0

    cart = request.session['venta_cart']
    local_query = request.session['venta_local_query']
    total_price = request.session['venta_total_price']

    context = {
        "locales": locales,
        "metodos": metodos,
        "cart": cart,
        "local_query": local_query,
        "codigo_barras": request.GET.get('codigo_barras', ''),
        "total_price": total_price
    }

    if request.method == "GET":
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
            request.session['venta_local_query'] = new_local_query

            products = SucursalProducto.objects.filter(id_sucursal=new_local_query)
            product = products.filter(id_producto=code_query).first()

            if not product:
                messages.error(request, "Producto no encontrado.")
                return render(request, 'punto_venta.html', context)

            quantity = product.cantidad
            print(product)
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
            
            total_price = sum(int(cart[code]['total']) for code in cart)

            request.session['venta_cart'] = cart
            request.session['venta_local_query'] = new_local_query
            request.session['venta_total_price'] = total_price
            
            context.update({
                "local_query": new_local_query,
                "codigo_barras": code_query,
                "total_price": total_price
            })

            messages.success(request, f"Producto encontrado: {product.id_producto.nombre}. Cantidad disponible: {quantity}.")
            return redirect('punto_venta')

    return render(request, 'punto_venta.html', context)

@login_required
def punto_compra(request):
    return render(request, 'punto_compra.html')

@login_required
def punto_otros(request):
    locales = Sucursal.objects.all()
    metodos = MetodosPago.objects.all()
    tipos = TipoMovimiento.objects.exclude(nombre__in=["Compra", "Venta"])
    
    # Inicializar variables si no existen
    if 'otros_cart' not in request.session:
        request.session['otros_cart'] = {} 

    if ('otros_local_query' not in request.session) or (request.session['otros_cart'] == {}):
        request.session['otros_local_query'] = ''

    if ('otros_tipo_query' not in request.session) or (request.session['otros_cart'] == {}):
        request.session['otros_tipo_query'] = ''

    if 'otros_total_price' not in request.session:
        request.session['otros_total_price'] = 0

    cart = request.session['otros_cart']
    local_query = request.session['otros_local_query']
    tipo_query = request.session['otros_tipo_query']
    total_price = request.session['otros_total_price']

    context = {
        "locales": locales,
        "metodos": metodos,
        "tipos": tipos,
        "cart": cart,
        "local_query": local_query,
        "tipo_query": tipo_query,
        "codigo_barras": request.GET.get('codigo_barras', ''),
        "total_price": total_price
    }

    if request.method == "GET":
        code_query = request.GET.get('codigo_barras', '')

        if 'codigo_barras' in request.GET or 'local' in request.GET or 'tipo' in request.GET:
            new_local_query = request.GET.get('local', '')
            new_tipo_query = request.GET.get('tipo', '')

            if not new_local_query:
                messages.error(request, "Debe seleccionar un local primero.")
                return redirect('punto_otros')
            
            if not new_tipo_query:
                messages.error(request, "Debe seleccionar un tipo de movimiento.")
                return redirect('punto_otros')
            
            if cart and local_query and new_local_query != local_query:
                messages.error(request, "No se puede cambiar de local con productos en el carrito.")
                return redirect('punto_otros')
            
            if cart and tipo_query and new_tipo_query != tipo_query:
                messages.error(request, "No se puede cambiar de tipo de movimiento con productos en el carrito.")
                return redirect('punto_otros')
            
            if not code_query:
                messages.error(request, "Debe de añadir el código de barras.")
                return redirect('punto_otros')
            
            if not code_query.isdigit() or len(code_query) > 15:
                messages.error(request, "Debe de añadir un código de barras válido.")
                return redirect('punto_otros')

            # Actualizar local y tipo query de la sesión
            request.session['otros_local_query'] = new_local_query
            request.session['otros_tipo_query'] = new_tipo_query

            products = SucursalProducto.objects.filter(id_sucursal=new_local_query)
            product = products.filter(id_producto=code_query).first()

            if not product:
                messages.error(request, "Producto no encontrado.")
                return render(request, 'punto_otros.html', context)

            quantity = product.cantidad
            if (code_query in cart) and (cart[code_query]["quantity"] >= quantity) or (quantity < 0):
                messages.error(request, "Producto fuera de stock.")
                return render(request, 'punto_otros.html', context)

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
            
            total_price = sum(int(cart[code]['total']) for code in cart)

            request.session['otros_cart'] = cart
            request.session['otros_local_query'] = new_local_query
            request.session['otros_tipo_query'] = new_tipo_query
            request.session['otros_total_price'] = total_price
            
            context.update({
                "local_query": new_local_query,
                "tipo_query": new_tipo_query,
                "codigo_barras": code_query,
                "total_price": total_price
            })

            messages.success(request, f"Producto encontrado: {product.id_producto.nombre}. Cantidad disponible: {quantity}.")
            return redirect('punto_otros')

    return render(request, 'punto_otros.html', context)

@login_required
def actualizar_cantidad_carrito(request, contexto, codigo_barras):

    if (contexto != "punto_compra") and (contexto != "punto_venta") and (contexto != "punto_otros"):
        messages.error(request, "Error al actualizar el carrito.")
        return redirect("puntos")

    if request.method != "POST":
        return redirect(contexto)

    if not request.POST.get("cantidad").isdigit():
        messages.error(request, "Ingrese una cantidad válida.")
        return redirect(contexto)

    if contexto == 'punto_venta':
        cart_key = 'venta_cart'
        local_query_key = 'venta_local_query'
        total_price_key = 'venta_total_price'
    else:  # 'otros'
        cart_key = 'otros_cart'
        local_query_key = 'otros_local_query'
        total_price_key = 'otros_total_price'


    if not request.session.get(local_query_key):
        messages.error(request, "Error al obtener local.")
        return redirect(contexto)

    local_query = request.session[local_query_key]
    nueva_cantidad = int(request.POST.get("cantidad"))
    cart = request.session.get(cart_key, {})

    if codigo_barras not in cart:
        messages.error(request, "Producto no encontrado en el carrito.")
        return redirect(contexto)

    producto = SucursalProducto.objects.filter(id_producto=codigo_barras, id_sucursal=local_query).first()
    if not producto or nueva_cantidad > producto.cantidad:
        messages.error(request, f"Cantidad fuera de stock. Cantidad disponible: {cart[codigo_barras]['max_quantity']}")
        return redirect(contexto)
  
    cart[codigo_barras]["quantity"] = nueva_cantidad
    cart[codigo_barras]["total"] = cart[codigo_barras]["price"] * nueva_cantidad

    # Recalcular el total del precio
    total_price = sum(item["total"] for item in cart.values())
    request.session[total_price_key] = total_price
    request.session[cart_key] = cart

    messages.success(request, "Cantidad actualizada correctamente.")
    return redirect(contexto)

@login_required
def eliminar_producto_carrito(request, contexto, code):
        
    if (contexto != "punto_compra") and (contexto != "punto_venta") and (contexto != "punto_otros"):
        messages.error(request, "Error al actualizar el carrito.")
        return redirect("puntos")
    
    if contexto == 'punto_venta':
        cart_key = 'venta_cart'
        total_price_key = 'venta_total_price'
    else:  # 'otros'
        cart_key = 'otros_cart'
        total_price_key = 'otros_total_price'

    cart = request.session.get(cart_key, {})
    total_price = request.session.get(total_price_key, 0)
    
    if code not in cart:
        messages.success(request, "El producto no se encuentra en el carrito.")
        return redirect(contexto)

    total_price -= int(cart[code]['total'])
    del cart[code]
    request.session[cart_key] = cart
    request.session[total_price_key] = total_price
    messages.success(request, "Producto eliminado del carrito.")
    return redirect(contexto)

@login_required
def confirmar(request, contexto):

    if request.method != "POST":
        return redirect(contexto)

    if (contexto != "punto_compra") and (contexto != "punto_venta") and (contexto != "punto_otros"):
        messages.error(request, "Error al procesar la confirmación.")
        return redirect("puntos")

    if contexto == 'punto_venta':
        cart_key = 'venta_cart'
        local_query_key = 'venta_local_query'
        total_price_key = 'venta_total_price'
    else:  # 'otros'
        cart_key = 'otros_cart'
        local_query_key = 'otros_local_query'
        total_price_key = 'otros_total_price'
        type_query_key = 'otros_tipo_query'

    total_amount = request.session.get(total_price_key, 0)
    local_query = request.session.get(local_query_key, '')

    if not local_query_key:
        messages.error(request, "Por favor, selecciona una sucursal.")
        return redirect(contexto)

    if total_amount == 0:
        messages.error(request, "Por favor, agrega un producto.")
        return redirect(contexto)

    if contexto == 'punto_venta':

        # Lógica para Punto de Venta

        # Obtener el método de pago seleccionado
        payment_method_id = request.POST.get('metodo_pago')
        if not payment_method_id:
            messages.error(request, "Por favor, selecciona un método de pago.")
            return redirect(contexto)

        # Obtener el método de pago de la base de datos
        payment_method = MetodosPago.objects.filter(id=payment_method_id).first()

        if not payment_method:
            messages.error(request, "Método de pago no válido.")
            return redirect(contexto)

        # Procesar pago en efectivo
        if payment_method.nombre == "Efectivo":
            cash = request.POST.get('efectivo')

            if not cash or not cash.isdigit() or int(cash) < total_amount:
                messages.error(request, "Por favor, verifica el monto en efectivo.")
                return redirect(contexto)

            vuelto = int(cash) - total_amount
            print("vuelto", vuelto) # Todo mostrar vuelto en frond

            # Guardar detalles de pago en la base de datos
            current_cart = request.session.get(cart_key, {})
            save_ticket(request, contexto, current_cart, total_amount, local_query, 2, payment_method=payment_method, cash=cash)
        else:
            current_cart = request.session.get(cart_key, {})
            save_ticket(request, contexto, current_cart, total_amount, local_query, 2, payment_method=payment_method)

    elif contexto == 'punto_otros':
        # Lógica para Punto de Salida
        tipo_query = request.session.get(type_query_key, "")
        
        if not tipo_query:
            messages.error(request, "Por favor, selecciona un tipo de salida.")
            return redirect(contexto)
        
        current_cart = request.session.get(cart_key, {})
        save_ticket(request, contexto, current_cart, total_amount, local_query, tipo_query)

    clear_cart(request, contexto)

    messages.success(request, "Transacción realizada con éxito.")
    return redirect(contexto)

@login_required
def clear_cart(request, contexto):
    # Vacía el carrito de compras y restablece la sesión
    
    if contexto == 'punto_venta':
        cart_key = 'venta_cart'
        local_query_key = 'venta_local_query'
        total_price_key = 'venta_total_price'
    else:  # 'otros'
        cart_key = 'otros_cart'
        local_query_key = 'otros_local_query'
        total_price_key = 'otros_total_price'

    # Eliminar el carrito de la sesión
    request.session[cart_key] = {}
    request.session[total_price_key] = 0
    request.session[local_query_key] = ''

    messages.success(request, "Carrito vacío exitosamente.")
    return redirect(contexto)
