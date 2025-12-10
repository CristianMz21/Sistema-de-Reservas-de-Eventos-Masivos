import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Usuario


# ------------------ MODEL TESTS ------------------
class UsuarioModelTests(TestCase):
    def test_create_user(self):
        u = Usuario(username="testuser", email="test@mail.com")
        u.set_password("secret")
        u.save()
        self.assertTrue(u.check_password("secret"))
        self.assertFalse(u.check_password("badpass"))
        self.assertTrue(u.is_active)

    def test_soft_delete_attributes(self):
        u = Usuario.objects.create(username="soft", email="soft@mail.com")
        u.set_password("pwd")
        u.save()
        # simulamos soft-delete
        suffix = f".inactiva.{uuid.uuid4().hex[:8]}"
        u.email = f"{u.email}{suffix}"
        u.username = f"{u.username}{suffix}"
        u.is_active = False
        u.save()
        self.assertFalse(u.is_active)
        self.assertTrue(".inactiva." in u.email)


# ------------------ API TESTS ------------------
class UsuarioAPITests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.auth_user = Usuario.objects.create(
            username="authed", email="authed@mail.com"
        )
        self.auth_user.set_password("pass")
        self.auth_user.save()

    def test_list_only_active(self):
        Usuario.objects.create(username="active", email="active@mail.com")
        Usuario.objects.create(
            username="inactive", email="inactive@mail.com", is_active=False
        )

        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(reverse("usuario-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 1 active created + 1 auth user = 2 active users
        self.assertEqual(len(response.data), 2)
        # Check usernames present
        usernames = [u["username"] for u in response.data]
        self.assertIn("active", usernames)
        self.assertIn("authed", usernames)

    def test_create_user(self):
        # Registration should be public
        data = {
            "username": "demo",
            "email": "demo@mail.com",
            "password": "Str0ngP@ss",
            "nombre": "Demo",
            "apellido": "User",
            "telefono": "+34666555444",
            "fecha_nacimiento": "1995-06-15",
            "tipo_usuario": "cliente",
        }
        response = self.client.post(reverse("usuario-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # comprobamos que la pass se ha hasheado
        user = Usuario.objects.get(username="demo")
        self.assertTrue(user.check_password("Str0ngP@ss"))

    def test_retrieve_user(self):
        user = Usuario.objects.create(username="retrieve", email="retrieve@mail.com")
        user.set_password("pwd")
        user.save()

        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse("usuario-detail", kwargs={"uuid": user.uuid})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "retrieve")
        # password no debe aparecer
        self.assertNotIn("password", response.data)

    def test_update_user(self):
        user = Usuario.objects.create(username="update", email="update@mail.com")
        user.set_password("old")
        user.save()

        self.client.force_authenticate(user=user)
        data = {
            "username": "update2",
            "email": "update2@mail.com",
            "password": "NewStr0ngP@ss",
            "nombre": "Updated",
            "apellido": "User",
            "telefono": "+34666777888",
            "fecha_nacimiento": "1995-06-15",
            "tipo_usuario": "organizador",
        }
        response = self.client.put(
            reverse("usuario-detail", kwargs={"uuid": user.uuid}), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, "update2")
        self.assertTrue(user.check_password("NewStr0ngP@ss"))

    def test_partial_update(self):
        user = Usuario.objects.create(username="partial", email="partial@mail.com")
        user.set_password("pwd")
        user.save()

        self.client.force_authenticate(user=user)
        data = {"nombre": "SóloNombre"}
        response = self.client.patch(
            reverse("usuario-detail", kwargs={"uuid": user.uuid}), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.nombre, "SóloNombre")

    def test_soft_delete(self):
        user = Usuario.objects.create(username="softdel", email="softdel@mail.com")
        user.set_password("pwd")
        user.save()
        original_email = user.email
        original_user = user.username

        # DELETE → soft-delete
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            reverse("usuario-detail", kwargs={"uuid": user.uuid})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # usuario físico sigue
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertTrue(".inactiva." in user.email)
        self.assertTrue(".inactiva." in user.username)

        # ya no aparece en el listado
        self.client.force_authenticate(user=self.auth_user)  # use other active user
        list_response = self.client.get(reverse("usuario-list"))
        # Using uuid for comparison as id is not in ListSerializer
        uuids = [str(u["uuid"]) for u in list_response.data]
        self.assertNotIn(str(user.uuid), uuids)

        # se puede re-crear con el mismo email/username original
        data = {
            "username": original_user,
            "email": original_email,
            "password": "NewAfterSoft",
        }
        recreate = self.client.post(reverse("usuario-list"), data, format="json")
        self.assertEqual(recreate.status_code, status.HTTP_201_CREATED)
