from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
from .models import Usuario
from django.utils import timezone

def login_view(request):
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = Usuario.objects.get(username=username, is_active=True)
                if user.check_password(password):
                    # Login exitoso
                    request.session['user_id'] = str(user.uuid)  # Usar UUID como identificador
                    user.ultimo_login = timezone.now()
                    user.save(update_fields=['ultimo_login'])
                    return HttpResponse("Login exitoso")
                else:
                    message = 'Contraseña incorrecta'
            except Usuario.DoesNotExist:
                message = 'Usuario no encontrado o desactivado'
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'message': message})




def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if Usuario.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
                return render(request, 'register.html', {'form': form})  
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está en uso.')
                return render(request, 'register.html', {'form': form})  

            # Crear usuario
            user = Usuario(
                username=username,
                email=email,
                tipo_usuario='cliente',
                is_active=True
            )
            user.set_password(password)
            user.save()
            messages.success(request, 'Registro exitoso')
            return redirect('login')          
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})