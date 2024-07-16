from django.contrib import messages
from django.shortcuts import redirect, render
from auxiliares.models import Comuna, TipoAuxiliar, Auxiliar


def auxiliares(request):
    auxiliares = Auxiliar.objects.all()
    tipos = TipoAuxiliar.objects.all()
    comunas=Comuna.objects.all()

    return render (request,'auxiliares.html', context={"auxiliares": auxiliares,
                                                       "tipos": tipos,
                                                       "comunas": comunas} )

def registrar_auxiliar(request):
    rut = request.POST['txtRut']
    dv = request.POST['txtDV']
    razon_social = request.POST["txtRazonSocial"]
    direccion = request.POST["txtDireccion"]
    web = request.POST["txtSitioWeb"]
    fecha = request.POST["txtFecha"]
    telefono = request.POST["txtNumero"]
    activo = request.POST["txtActivo"]
    activo = True if activo == "on" else False
    id_tipo = request.POST["tipo_auxiliar"]
    id_comuna = request.POST["comunas"]
    tipo = TipoAuxiliar.objects.get(id=id_tipo)
    comuna = Comuna.objects.get(id=id_comuna)

    try:
        # Crear auxiliar 
        auxiliar = Auxiliar.objects.create(
            rut_auxiliar=rut, dv=dv, razon_social=razon_social, direccion=direccion,
            sitio_web=web, fecha_inicio_acuerdo=fecha, telefono=telefono, activo=activo,
            tipo_auxiliar=tipo, comuna=comuna
        )
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            if "rut" in e.args[0]:
                e = "El rut ingresado ya existe! "
        messages.error(request, f"Error al crear auxiliar: {e}")
    else:
        messages.success(request, "Auxiliar registrado correctamente! ")
    finally:
        return redirect("auxiliares")

def editar_auxiliar(request, rut_auxiliar):
    try:
        if request.method =="POST":
            rut_auxiliar = request.POST['txtRut']
            dv = request.POST['txtDV']
            razon_social = request.POST["txtRazonSocial"]
            direccion = request.POST["txtDireccion"]
            web = request.POST["txtSitioWeb"]
            fecha = request.POST["txtFecha"]
            telefono = request.POST["txtNumero"]
            activo = request.POST["txtActivo"]
            activo = True if activo == "on" else False
            id_tipo = request.POST["tipo_auxiliar"]
            id_comuna = request.POST["comunas"]

            auxiliar = Auxiliar.objects.get(rut_auxiliar=rut_auxiliar)
            auxiliar.rut_auxiliar = rut_auxiliar
            auxiliar.dv = dv
            auxiliar.razon_social = razon_social
            auxiliar.direccion = direccion
            auxiliar.sitio_web = web
            auxiliar.fecha_inicio_acuerdo = fecha
            auxiliar.telefono = telefono
            auxiliar.activo = activo
            auxiliar.tipo_auxiliar = TipoAuxiliar.objects.get(id=id_tipo)
            auxiliar.comuna = Comuna.objects.get(id=id_comuna)

            auxiliar.save() 
            
            messages.success(request,"Se han modificados los cambios del Auxiliar")
            return redirect("auxiliares")
        
    except Exception as e:
            messages.error(request, f"No se pudo actualizar el auxiliar: {e}")
 
    auxiliar = Auxiliar.objects.get(rut_auxiliar=rut_auxiliar)
    tipos = TipoAuxiliar.objects.all()
    comunas = Comuna.objects.all()

    return render(request,'editar_auxiliar.html', context={"auxiliar": auxiliar,
                                                           "tipos": tipos,
                                                           "comunas": comunas})

def eliminar_auxiliar(request, rut_auxiliar):
    try:
      
        auxiliar = Auxiliar.objects.get(rut_auxiliar=rut_auxiliar)
        auxiliar = auxiliar.delete()
        messages.success(request,"Se ha eliminado el Auxiliar correctamente")
        
        return redirect("auxiliares")
    except Exception as e:
            messages.error(request, "No se puedo eliminar el auxiliar")
            return redirect("auxiliares")

def list_types(request):
    tipos = TipoAuxiliar.objects.all()

    return render (request,'tipo.html', context={'tipos': tipos,})

def guardar_tipo(request):
    try:
        nombre=request.POST['nombre']
        descripcion=request.POST['descripcion']
     
        tipo = TipoAuxiliar.objects.create(nombre=nombre,descripcion=descripcion)
  
        messages.success(request,'Se ha guardado exitosamente el nuevo Tipo de Auxiliar')
     
        return redirect('tipos')
    except Exception as e:
     
        messages.error(request, f"No se guardo el Tipo Auxiliar: {e}")
    return redirect('tipos')

def editar_tipos(request, id):
    try:
        if request.method =="POST":
            nombre=request.POST['nombre']
            descripcion=request.POST['descripcion']
          
            tipo=TipoAuxiliar.objects.get(id=id)
            tipo.descripcion=descripcion
            tipo.nombre=nombre

            tipo.save() 
            
            messages.success(request,"Se han modificados los cambios en el Tipo Auxiliar")
            return redirect("tipos")
        
    except Exception as e:
            messages.error(request, f"No se pudo actualizar el tipo: {e}")
 
    tipo = TipoAuxiliar.objects.get(id=id)
    return render(request,'editar_tipo.html',context={'tipo': tipo})

def eliminar_tipos(request,id):
    try:
      
        tipo=TipoAuxiliar.objects.get(id=id)
        tipo=tipo.delete()
        messages.success(request,"Se ha eliminado el Tipo Auxiliar")
        
        return redirect("tipos")
    except Exception as e:
            messages.error(request, "No se puedo eliminar el producto")
            return redirect("tipos")

def listar_comunas(request):
    
    comunas=Comuna.objects.all()
    
    return render (request,'comunas.html', context={'comunas': comunas,})

def guardar_comunas(request):
    try:
       
        nombre=request.POST['nombre']
         
        comuna = Comuna.objects.create(nombre=nombre
                                        )
  
        messages.success(request,'Se ha registrado una nueva Comuna')
     
        return redirect('comunas')
    except Exception as e:
     
        messages.error(request, f"No se pudo ingresar el producto: {e}")
    return redirect('comunas')

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

def eliminar_comunas(request,id):
    try:
      
        comuna=Comuna.objects.get(id=id)
        messages.success(request,f"Se ha eliminado la Comuna de {comuna.nombre}")
        comuna=comuna.delete()
        
        return redirect("comunas")
    except Exception as e:
            messages.error(request, "No se puedo eliminar la comuna")
            return redirect("comunas")
