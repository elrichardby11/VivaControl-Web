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

def save_ticket(request, contexto, cart, total_amount, local_query, type_mov, payment_method=None, cash=None, rut_aux=None, total_price_cost=None):
    try:

        id_movimiento = save_payment_details(request, contexto, cart, total_amount, local_query, type_mov, payment_method, rut_aux, total_price_cost)
        now, fecha, hora = get_date()

        with open_file(now, id_movimiento) as file:
            write_header(file, fecha, hora, type_mov)
            write_detail(file, cart, total_amount, type_mov, total_price_cost)

            if type_mov == 1:
                write_payments(file, total_amount, payment_method, cash, total_price_cost)
            else:
                file.write(" -------------------- SALIDA ESPECIAL ---------------- \n")
                file.write(" Nota: \n")
                file.write("     Esta operación corresponde a una salida especial. \n")
                file.write(" ===================================================== ")
    
    except Exception as e:
        messages.error(request, f"Error al procesar la transacción: {str(e)}")
        return redirect(contexto)

def save_payment_details(request, contexto, cart, total_amount, local_query, type_mov, payment_method, rut_aux=None, total_price_cost=None):
    try:
        # Obtener la sucursal
        sucursal = Sucursal.objects.get(id_sucursal=local_query)

        # Obtener el estado y el tipo de movimiento
        tipo_movimiento = TipoMovimiento.objects.get(id=type_mov)
        cstate_movimiento = CStateMovimiento.objects.get(nombre="Activo")

        # Crear PagoMovimiento
        with transaction.atomic():  # Usar transacción atómica para asegurar consistencia

            if type_mov in [1, 2]:
                max_id_pago = PagoMovimiento.objects.aggregate(Max('id_pago'))['id_pago__max'] or 0
                new_id_pago = max_id_pago + 1
                pago_movimiento = PagoMovimiento.objects.create(
                    id_pago=new_id_pago,
                    metodo=payment_method,
                    monto=total_amount
                )

            else:
                pago_movimiento = None

            # Obtener el auxiliar
            auxiliar = rut_aux if rut_aux else Auxiliar.objects.get(rut_auxiliar=1)
            # Precio total 0 si es salida especial
            total_amount = 0 if type_mov not in [1, 2] else total_amount

            # Crear Movimiento
            movimiento = Movimiento.objects.create(
                fecha=datetime.now(),
                periodo=datetime.now().year,
                tipo_movimiento=tipo_movimiento,
                cstate_movimiento=cstate_movimiento,
                auxiliar=auxiliar,
                precio_total=total_amount,
                coste_total=total_price_cost if total_price_cost else 0,  # Lo calcularemos a continuación
                pago=pago_movimiento
            )

            if movimiento.coste_total == 0:
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
                        movimiento__tipo_movimiento__nombre="Compra"
                    ).order_by('movimiento__fecha')

                    ventas = DetalleMovimiento.objects.filter(
                        sucursal_producto_id=sucursal_producto,
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

            else:
                # Iterar sobre el carrito y crear DetalleMovimiento
                for product_id, item in cart.items():
                    cantidad = item['quantity']
                    producto = Producto.objects.get(id_producto=product_id)

                    # Obtener el SucursalProducto
                    sucursal_producto, created = SucursalProducto.objects.get_or_create(
                        id_sucursal=sucursal, 
                        id_producto=producto,
                        defaults={
                            'cantidad': 0, 
                            'precio': item["sale_price"]
                        }
                    )
                    DetalleMovimiento.objects.create(
                        movimiento=movimiento,
                        sucursal_producto=sucursal_producto,
                        cantidad=cantidad,
                        precio_unitario=item["sale_price"],
                        coste_unitario=item["cost_price"]
                    )

            movimiento.save()
            return movimiento.id

    except Exception as e:
        messages.error(request, f"Error al procesar el pago: {str(e)}")
        return redirect(contexto)

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

def write_header(file, fecha, hora, type_mov):
    # Encabezado diferenciado según el tipo de movimiento

    if type_mov == 1:
        file.write(" _____________________________________________________ \n")
        file.write("|                       VENTA                         |\n")
    elif type_mov not in [1, 2]:
        file.write(" _____________________________________________________ \n")
        file.write("|                     SALIDA ESPECIAL                 |\n")

    type_obj = TipoMovimiento.objects.get(id=type_mov)

    file.write("|RUT: 11.111.111-1                                    |\n")
    file.write("|RAZON SOCIAL: FANTASIA S.A                           |\n")
    file.write("|BLABLA NRO 999 - PISO 1234B                          |\n")
    file.write("|LAS CONDES - SANTIAGO F. -256784321                  |\n")
    file.write("|_____________________________________________________|\n")
    file.write(f" {fecha}          {hora}\n")
    file.write(f" {type_obj.nombre.capitalize()} Electronica:        123.456.789\n")
    file.write(" CAJA: 1 CAJERO: RICHARD MAZUELOS\n")
    file.write("  D E T A L L E  \n")
    file.write(" --------------- \n")

def write_detail(file, cart, total_amount, type_mov, total_price_cost=None):

    if type_mov not in [1, 2]:
        for product_code, item in cart.items():
            product_name = item["name"]
            quantity = item["quantity"]
            formatted_quantity = format_number(quantity)

            if quantity > 1:
                cantidad = (40 - (len(formatted_quantity) + len(product_name)))
                file.write(f" Codigo: {product_code}\n")
                file.write(f" {formatted_quantity} {product_name}{' ' * (cantidad+11)}\n")
            else:
                cantidad = 28 - len(product_name)
                file.write(f" {product_code:>13} {product_name}{' ' * (cantidad+11)}\n")

        file.write(" ----------------------------------------------------- \n")
        file.write(f"                                         TOTAL SALIDA  \n")
    
    else:
        if type_mov == 1:
            price_key = "cost_price"
            total_amount = total_price_cost
        else:
            price_key = "price"

        neto = round(total_amount / 1.19)
        iva = round(total_amount - neto)

        for product_code, item in cart.items():
            product_name = item["name"]
            price = item[price_key]
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
                file.write(f" {product_code:>13} X {product_name}{' ' * cantidad}{'$'}{formatted_total_price:>11}\n")
        file.write(" ----------------------------------------------------- \n")
        file.write(f"                                SUBTOTAL      $ {format_number(total_amount):>7}\n")
        file.write(f"                        TOTAL AFECTO       $ {format_number(neto):>10}\n")
        file.write(f"                        TOTAL EXCENTO      $          0\n")
        file.write(f"                        TOTAL IVA 19%      $ {format_number(iva):>10}\n")
        file.write(f"                                TOTAL         $ {format_number(total_amount):>7}\n")

def write_payments(file, total_amount, payment_method, cash, total_price_cost=None):

    total_amount = total_price_cost if total_price_cost is not None else total_amount

    try:
        payment_quantity = int(cash) if cash else 0 # Convert to integer if it's a string
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
