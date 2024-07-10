from django.shortcuts import render

def metodos_pago(request):
    return render(request, 'metodos_pago.html')
