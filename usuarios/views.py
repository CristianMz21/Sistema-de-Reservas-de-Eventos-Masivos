from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import LoginForm, RegistrationForm
from .models import Usuario
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = Usuario.objects.get(username=username, is_active=True)
                if user.check_password(password):
                    # Login exitoso
                    request.session['user_id'] = str(user.uuid)
                    user.ultimo_login = timezone.now()
                    user.save(update_fields=['ultimo_login'])
                    messages.success(request, f'Bienvenido, {user.username}!')
                    # Redirigir a una página principal (aún no creada)
                    return redirect('/') 
                else:
                    messages.error(request, 'Usuario o contraseña incorrectos.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # El formulario ya ha validado la unicidad y que las contraseñas coinciden
            user = Usuario(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            messages.success(request, '¡Registro exitoso! Por favor, inicia sesión.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'usuarios/register.html', {'form': form})