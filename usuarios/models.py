import uuid
import bcrypt
from django.db import models

#DB usuarios

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    username = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        max_length=255
    )

    password_hash = models.CharField(max_length=255)

    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    fecha_nacimiento = models.DateField(blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
        ('organizador', 'Organizador'),
    ]

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='cliente'
    )

    class Meta:
        db_table = 'usuarios'
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                condition=models.Q(is_active=True),
                name='unique_active_email'
            ),
            models.UniqueConstraint(
                fields=['username'],
                condition=models.Q(is_active=True),
                name='unique_active_username'
            ),
        ]
        indexes = [
            models.Index(fields=['email'], name='idx_usuario_email'),
            models.Index(fields=['username'], name='idx_usuario_username'),
        ]

    def __str__(self):
        return self.username

    def set_password(self, raw_password: str):
        """Hashea y guarda la contraseña"""
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = hashed.decode('utf-8')

    def check_password(self, raw_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))
