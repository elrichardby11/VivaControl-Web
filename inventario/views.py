from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_movimientos(request):
    return render(request, "inventario.html")