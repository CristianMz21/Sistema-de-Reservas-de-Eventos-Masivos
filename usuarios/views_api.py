import uuid
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        return Usuario.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        """Soft-delete: desactiva y libera email/username."""
        suffix = f'.inactiva.{uuid.uuid4().hex[:8]}'
        instance.email = f'{instance.email}{suffix}'
        instance.username = f'{instance.username}{suffix}'
        instance.is_active = False
        instance.save(update_fields=['email', 'username', 'is_active'])