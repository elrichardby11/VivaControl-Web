from django.shortcuts import render, redirect

from auxiliares.models import Comuna
from administrador.models import MetodosPago, Sucursal
from django.contrib import messages


def metodos_pago(request):
    metodos = MetodosPago.objects.all()
    return render(request, "metodos_pago.html", context={"metodos": metodos})

def agregar_metodo(request):
    nombre = request.POST["txtNombre"]
    descripcion = request.POST["txtDescripcion"]
    try:
        metodo = (
            MetodosPago.objects.create(
                nombre=nombre,
                descripcion=descripcion,
            ),
        )
        messages.success(request, "Método de pago agregado correctamente")
        return redirect("metodos_pago")
    except Exception as e:
        messages.error(request, f"Error al crear el método de pago: {e}")
        return redirect("metodos_pago")

def editar_metodo(request, id):
    try:
        if request.method =="POST":
            nombre=request.POST['txtNombre']
            descripcion=request.POST['txtDescripcion']

            metodo=MetodosPago.objects.get(id=id)
            metodo.nomre=nombre
            metodo.descripcion=descripcion

            metodo.save()

            messages.success(request,"Se han modificados los cambios del método de pago")
            return redirect("metodos_pago")

    except Exception as e:
            messages.error(request, f"No se pudo actualizar el método de pago: {e}")

    metodo = MetodosPago.objects.get(id=id)
    return render(
        request,
        "editar_metodo.html",
        context={"metodo": metodo},
    )

def eliminar_metodo(request, id):
    metodo = MetodosPago.objects.get(id=id)
    metodo.delete()
    messages.success(request, "Método de Pago eliminado correctamente")
    return redirect("metodos_pago")

def sucursales(request):
    comunas = Comuna.objects.all()
    sucursal = Sucursal.objects.all()
    return render(
        request, "sucursales.html", context={"comunas": comunas, "sucursales": sucursal}
    )

def agregar_sucursal(request):
    id_sucursal = request.POST["id_sucursal"]
    direccion = request.POST["direccion"]
    comuna = request.POST["Comuna"]
    try:
        sucursal = (
            Sucursal.objects.create(
                id_sucursal=id_sucursal,
                direccion=direccion,
                comuna=Comuna.objects.get(id=comuna),
            ),
        )
        messages.success(request, "Local agregado correctamente")
        return redirect("sucursales")
    except Exception as e:
        messages.error(request, e)
        return redirect("sucursales")

def editar_sucursal(request, id_sucursal):
    try:
        if request.method =="POST":
            direccion=request.POST['direccion']
            comunas=request.POST['Comuna']

            sucursal=Sucursal.objects.get(id_sucursal=id_sucursal)
            sucursal.direccion=direccion
            sucursal.comuna=Comuna.objects.get(id=comunas)

            sucursal.save()

            messages.success(request,"Se han modificados los cambios de la sucursal")
            return redirect("sucursales")

    except Exception as e:
            messages.error(request, f"No se pudo actualizar la sucursal: {e}")

    comunas = Comuna.objects.all()
    sucursal = Sucursal.objects.get(id_sucursal=id_sucursal)
    return render(
        request,
        "editar_sucursal.html",
        context={"sucursal": sucursal, "comunas": comunas},
    )

def eliminar_sucursal(request, id):
    sucursal = Sucursal.objects.get(id_sucursal=id)
    sucursal.delete()
    messages.success(request, "Sucursal eliminada correctamente")
    return redirect("sucursales")
