from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages

from Vivacontrol.forms import RegistrationForm

def home(request):
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'sobre_nosotros.html')

def contacto(request):
    return render(request, 'contacto.html')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente")
            return redirect("register")
        else:
            messages.error(request, form.errors)
            return redirect("register")

    else:
        form = RegistrationForm()
        return render(request, "register.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("home")
        
        else:
            messages.error(request, form.errors)
            return redirect("login")
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})
        
def logout(request):
    auth.logout(request)
    return redirect('home')