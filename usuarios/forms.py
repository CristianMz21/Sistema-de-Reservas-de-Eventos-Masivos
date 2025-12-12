from django import forms
from .models import Usuario

from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Usuario", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Contraseña", "class": "form-control"}
        )
    )


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Usuario"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Correo Electrónico"})
    )
    password = forms.CharField(
        max_length=128, widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"})
    )
    confirm_password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar Contraseña"}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")
