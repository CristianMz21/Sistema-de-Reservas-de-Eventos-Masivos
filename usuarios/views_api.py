from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario
from .serializers import (
    UsuarioSerializer,
    UsuarioListSerializer,
    UsuarioDetailSerializer,
    UsuarioCreateSerializer,
    UsuarioUpdateSerializer,
    CustomTokenObtainPairSerializer,
)
from .permissions import IsOwnerOrAdmin


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista de obtención de token personalizada para devolver datos extras.
    """

    serializer_class = CustomTokenObtainPairSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar usuarios.
    """

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    lookup_field = "uuid"

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
                IsAuthenticated,
                IsOwnerOrAdmin,
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
        instance.soft_delete()
