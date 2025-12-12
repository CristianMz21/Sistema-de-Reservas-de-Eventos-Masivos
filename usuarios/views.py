from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import Usuario


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # AuthenticationForm cleans data and checks credentials
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect("/")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, "usuarios/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # El formulario ya ha validado la unicidad y que las contraseñas coinciden
            user = Usuario(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
            )
            user.set_password(form.cleaned_data["password"])
            user.save()

            messages.success(request, "¡Registro exitoso! Por favor, inicia sesión.")
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "usuarios/register.html", {"form": form})
