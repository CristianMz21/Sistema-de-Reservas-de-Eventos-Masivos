import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.validators import RegexValidator


class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Superusuarios deben ser activos por defecto (aunque nuestro default lo es)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuario debe tener is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset()


class UsuarioActivoManager(UsuarioManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9]{4,50}$",
                message="Solo se permiten letras y números, entre 4 y 50 caracteres.",
            )
        ],
    )

    email = models.EmailField(max_length=255, unique=True)

    # password field is inherited from AbstractBaseUser

    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    fecha_nacimiento = models.DateField(blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    # last_login is inherited from AbstractBaseUser, maps to ultimo_login concept

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Requerido para admin

    is_verified = models.BooleanField(default=False)

    TIPO_USUARIO_CHOICES = [
        ("cliente", "Cliente"),
        ("admin", "Administrador"),
        ("organizador", "Organizador"),
    ]

    tipo_usuario = models.CharField(
        max_length=20, choices=TIPO_USUARIO_CHOICES, default="cliente"
    )

    objects = UsuarioManager()
    activos = UsuarioActivoManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or self.email})"

    @property
    def full_name(self):
        """Retorna el nombre completo del usuario"""
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre or ""

    def get_full_name(self):
        return self.full_name

    def soft_delete(self):
        """
        Realiza un borrado lógico del usuario:
        - Lo marca como inactivo.
        - Modifica email y username para liberar esos valores (apéndice UUID).
        """
        suffix = f".inactiva.{uuid.uuid4().hex[:8]}"
        if ".inactiva." not in self.email:
            self.email = f"{self.email}{suffix}"
        if ".inactiva." not in self.username:
            self.username = f"{self.username}{suffix}"

        self.is_active = False
        self.save(update_fields=["email", "username", "is_active"])
