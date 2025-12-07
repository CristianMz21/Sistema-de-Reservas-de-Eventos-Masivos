from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
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

    return render(request, '/home/mackroph/Projectos/Python/sistema-reservas/usuarios/templates/login.html', {'form': form, 'message': message})