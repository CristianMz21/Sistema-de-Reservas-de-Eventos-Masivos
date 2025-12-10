import uuid
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Usuario
from .serializers import (
    UsuarioSerializer,
    UsuarioListSerializer,
    UsuarioDetailSerializer,
    UsuarioCreateSerializer,
    UsuarioUpdateSerializer,
)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar usuarios.
    """

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    lookup_field = (
        "uuid"  # Usar UUID para lookups en la API es mejor práctica si existe
    )

    def get_queryset(self):
        return Usuario.objects.filter(is_active=True)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [
                IsAuthenticated
            ]  # Or use default from settings (which is IsAuth)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return UsuarioListSerializer
        elif self.action == "retrieve":
            return UsuarioDetailSerializer
        elif self.action == "create":
            return UsuarioCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UsuarioUpdateSerializer
        return UsuarioDetailSerializer

    def perform_destroy(self, instance):
        """Soft-delete: desactiva y libera email/username."""
        suffix = f".inactiva.{uuid.uuid4().hex[:8]}"
        # Solo anexar sufijo si no lo tiene ya (en caso de delete idempotente raro)
        if ".inactiva." not in instance.email:
            instance.email = f"{instance.email}{suffix}"
        if ".inactiva." not in instance.username:
            instance.username = f"{instance.username}{suffix}"

        instance.is_active = False
        instance.save(update_fields=["email", "username", "is_active"])
