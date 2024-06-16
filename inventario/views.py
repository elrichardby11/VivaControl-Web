from django.shortcuts import render

# Create your views here.
def listar_movimientos(request):
    return render(request, "inventario.html")