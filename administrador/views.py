from django.shortcuts import render

from auxiliares.models import Comuna
from administrador.models import Sucursal
from django.contrib import messages
from django.shortcuts import redirect


def metodos_pago(request):
    return render(request, "metodos_pago.html")


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


def eliminar_sucursal(request, id):
    sucursal = Sucursal.objects.get(id_sucursal=id)
    sucursal.delete()
    messages.success(request, "Sucursal eliminada correctamente")
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


def editar_comunas(request, id):
    try:
        if request.method =="POST":
            nombre=request.POST['nombre']
            comuna=Comuna.objects.get(id=id)
            comuna.nombre=nombre

            comuna.save() 

            messages.success(request,"Se han modificados los cambios de la Comuna")
            return redirect("comunas")

    except Exception as e:
            messages.error(request, f"No se pudo actualizar la Comuna: {e}")
 
    comuna = Comuna.objects.get(id=id)
    return render(request,'editar_comunas.html',context={'comuna': comuna})