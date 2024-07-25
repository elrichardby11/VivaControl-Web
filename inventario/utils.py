from datetime import datetime
import os
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Max, Sum
from administrador.models import Sucursal
from auxiliares.models import Auxiliar
from productos.models import Producto
from .models import PagoMovimiento, Movimiento, DetalleMovimiento, SucursalProducto, TipoMovimiento, CStateMovimiento

def save_payment_details(request, cart, total_amount, payment_method, local_query):
    try:
        # Obtener la sucursal
        sucursal = Sucursal.objects.get(id_sucursal=local_query)

        # Obtener el estado y el tipo de movimiento
        tipo_movimiento = TipoMovimiento.objects.get(nombre="Venta")
        cstate_movimiento = CStateMovimiento.objects.get(nombre="Activo")

        # Crear PagoMovimiento
        with transaction.atomic():  # Usar transacción atómica para asegurar consistencia
            max_id_pago = PagoMovimiento.objects.aggregate(Max('id_pago'))['id_pago__max'] or 0
            new_id_pago = max_id_pago + 1
            pago_movimiento = PagoMovimiento.objects.create(
                id_pago=new_id_pago,
                metodo=payment_method,
                monto=total_amount
            )

            # Obtener el auxiliar genérico para el cliente
            auxiliar = Auxiliar.objects.get(rut_auxiliar=1)

            # Crear Movimiento
            movimiento = Movimiento.objects.create(
                fecha=datetime.now(),
                periodo=datetime.now().year,
                tipo_movimiento=tipo_movimiento,
                cstate_movimiento=cstate_movimiento,
                auxiliar=auxiliar,
                precio_total=total_amount,
                coste_total=0,  # Lo calcularemos a continuación
                pago=pago_movimiento
            )

            coste_total = 0  # Inicializar coste total

            # Iterar sobre el carrito y crear DetalleMovimiento
            for product_id, item in cart.items():
                cantidad = item['quantity']
                producto = Producto.objects.get(id_producto=product_id)

                # Obtener el SucursalProducto
                sucursal_producto = SucursalProducto.objects.get(id_sucursal=sucursal, id_producto=producto)

                # Obtener compras previas y ventas
                compras = DetalleMovimiento.objects.filter(
                    sucursal_producto=sucursal_producto,
                    movimiento__tipo_movimiento__nombre="Compra"  # Suponiendo que el tipo de movimiento para compras es "Compra"
                ).order_by('movimiento__fecha')

                ventas = DetalleMovimiento.objects.filter(
                    sucursal_producto=sucursal_producto,
                    movimiento__tipo_movimiento__nombre="Venta"
                ).aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0

                contador = 0
                cantidad_restante = cantidad
                precio_coste = 0

                for compra in compras:
                    if (compra.cantidad + contador) >= ventas:
                        cantidad_disponible = (compra.cantidad + contador) - ventas
                        if cantidad_restante <= cantidad_disponible:
                            precio_coste = compra.coste_unitario
                            coste_total += cantidad_restante * precio_coste
                            DetalleMovimiento.objects.create(
                                movimiento=movimiento,
                                sucursal_producto=sucursal_producto,
                                cantidad=cantidad_restante,
                                precio_unitario=sucursal_producto.precio,
                                coste_unitario=precio_coste
                            )
                            cantidad_restante = 0
                            break
                        else:
                            coste_total += cantidad_disponible * compra.coste_unitario
                            cantidad_restante -= cantidad_disponible
                            DetalleMovimiento.objects.create(
                                movimiento=movimiento,
                                sucursal_producto=sucursal_producto,
                                cantidad=cantidad_disponible,
                                precio_unitario=sucursal_producto.precio,
                                coste_unitario=compra.coste_unitario
                            )
                            ventas += cantidad_disponible
                    contador += compra.cantidad

            # Actualizar el coste total en el movimiento
            movimiento.coste_total = coste_total
            movimiento.save()
            return movimiento.id

    except Exception as e:
        messages.error(request, f"Error al procesar el pago: {str(e)}")
        return redirect('punto_venta')

def save_ticket(request, cart, total_amount, payment_method, local_query, efectivo=None):
    try:

        id_movimiento = save_payment_details(request, cart, total_amount, payment_method, local_query)
        now, fecha, hora = get_date()

        with open_file(now, id_movimiento) as file:
            write_header(file, fecha, hora)
            write_detail(file, cart, total_amount)
            write_payments(file, total_amount, payment_method, efectivo)

    except Exception as e:
        messages.error(request, f"Error al procesar el pago: {str(e)}")
        return redirect('punto_venta')

def get_date():
    now = datetime.now()
    fecha = now.strftime("Fecha: %d-%m-%Y")
    hora = now.strftime("Hora: %H:%M:%S")
    return now, fecha, hora

def open_file(now, id_movimiento):
    directory = f"inventario/boletas"
    id_movimiento = str(id_movimiento) if id_movimiento else 0
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filename = now.strftime(f"{directory}/{id_movimiento}__%Y-%m-%d_%H-%M-%S.txt")
        print(f"Registro guardado en {filename}")
        return open(filename, "w")
    except OSError as e:
        print(f"Error creating file: {e}")
        return None

def write_header(file, fecha, hora):
    file.write(" _____________________________________________________ \n")
    file.write("|                                                     |\n")
    file.write("|RUT: 11.111.111-1                                    |\n")
    file.write("|RAZON SOCIAL: FANTASIA S.A                           |\n")
    file.write("|BLABLA NRO 999 - PISO 1234B                          |\n")
    file.write("|LAS CONDES - SANTIAGO F. -256784321                  |\n")
    file.write("|GIRO: VENTAS AL POR MENOR DE MERCADERIA              |\n")
    file.write("|_____________________________________________________|\n")
    file.write(f" {fecha}          {hora}\n")
    file.write(" Boleta Electronica:        123.456.789\n")
    file.write(" CAJA: 1 CAJERO: RICHARD MAZUELOS\n")
    file.write("  D E T A L L E  \n")
    file.write(" --------------- \n")

def write_detail(file, cart, total_amount):

    neto = round(total_amount / 1.19)
    iva = round(total_amount - neto)

    for product_code, item in cart.items():
        product_name = item["name"]
        price = item["price"]
        quantity = item["quantity"]
        total_price = quantity * price
        formatted_quantity = format_number(quantity)
        formatted_price = format_number(price)
        formatted_total_price = format_number(total_price)

        if quantity > 1:
            cantidad = (40 - (len(formatted_quantity) + len(formatted_price) + len(product_name)))
            file.write(f" Codigo: {product_code}\n")
            file.write(f" {formatted_quantity}X{formatted_price} {product_name}{' ' * cantidad}{'$'}{formatted_total_price:>11}\n")
        else:
            cantidad = 28 - len(product_name)
            file.write(f" {product_code:>13} {product_name}{' ' * cantidad}{'$'}{formatted_total_price:>11}\n")
    file.write(" ----------------------------------------------------- \n")
    file.write(f"                                SUBTOTAL      $ {format_number(total_amount):>7}\n")
    file.write(f"                        TOTAL AFECTO       $ {format_number(neto):>10}\n")
    file.write(f"                        TOTAL EXCENTO      $          0\n")
    file.write(f"                        TOTAL IVA 19%      $ {format_number(iva):>10}\n")
    file.write(f"                                TOTAL         $ {format_number(total_amount):>7}\n")

def write_payments(file, total_amount, payment_method, efectivo):

    try:
        payment_quantity = int(efectivo) if efectivo else 0 # Convert to integer if it's a string
    except ValueError:
        print("Error: 'efectivo' Debe ser un valor válido.")
        return
        
    file.write(" ---------------------P A G O S----------------------- \n")
    
    payment_method_name = str(payment_method)

    if payment_method_name == "Efectivo":

        file.write(f" {payment_method_name}           $ {format_number(payment_quantity):>10}\n")
        file.write(f" Vuelto             $ { format_number(payment_quantity-total_amount):>10}\n")
        file.write(" ===================================================== ")
    else:
        file.write(f" {payment_method_name:<7}            $ {format_number(total_amount):>10}\n")
        file.write(" Vuelto             $          0\n")
        file.write(" ===================================================== ")

def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

def clear_cart(request):
    request.session['cart'] = {}
    request.session['total_price'] = 0
    request.session['local_query'] = ''
