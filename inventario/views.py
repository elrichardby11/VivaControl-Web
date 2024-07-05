from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movimiento
from django.core.paginator import Paginator             

@login_required
def inventario_list(request):
    movimientos = Movimiento.objects.all()
    paginator = Paginator(movimientos, 5)  # Mostrar 5 elementos por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventario.html', {'page_obj': page_obj})
