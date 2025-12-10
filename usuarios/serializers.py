from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario


class UsuarioBaseSerializer(serializers.ModelSerializer):
    """Serializer base con campos comunes."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        fields = ["uuid", "username", "email", "full_name", "tipo_usuario", "is_active"]
        read_only_fields = ["uuid", "is_active"]


class UsuarioListSerializer(UsuarioBaseSerializer):
    """Serializer para listar usuarios (datos mínimos)."""

    class Meta(UsuarioBaseSerializer.Meta):
        fields = ["uuid", "username", "email", "full_name", "tipo_usuario", "is_active"]


class UsuarioDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalles de usuario (datos completos)."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        exclude = ["password", "id", "groups", "user_permissions"]
        read_only_fields = [
            "uuid",
            "fecha_registro",
            "last_login",
            "is_active",
            "is_verified",
        ]


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear nuevos usuarios con password."""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "password",
            "nombre",
            "apellido",
            "telefono",
            "fecha_nacimiento",
            "tipo_usuario",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario


class UsuarioUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar usuarios."""

    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "password",
            "nombre",
            "apellido",
            "telefono",
            "fecha_nacimiento",
            "tipo_usuario",
        ]
        read_only_fields = []  # Username should be editable per tests

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


# Maintain compatibility or for generic usage if needed, though specific ones are better.
class UsuarioSerializer(UsuarioDetailSerializer):
    """Serializer genérico de compatibilidad (alias de Detail)."""

    pass
