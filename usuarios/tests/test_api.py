from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from usuarios.models import Usuario


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

    def test_update_permission_denied(self):
        """Test that a user cannot update another user's profile."""
        other_user = Usuario.objects.create(username="other", email="other@mail.com")
        other_user.set_password("pwd")
        other_user.save()

        self.client.force_authenticate(user=self.auth_user)
        data = {"nombre": "Hacker"}

        # auth_user tries to update other_user
        response = self.client.patch(
            reverse("usuario-detail", kwargs={"uuid": other_user.uuid}),
            data,
            format="json",
        )
        # Default behavior of ModelViewSet with IsAuthenticated allows access if not restricted by object permissions
        # However, standard Django permissions or custom ones might be needed.
        # Let's assume for now we expect 403 or 404 depending on queryset filtering or object perm.
        # But wait, standard IsAuthenticated doesn't check object ownership.
        # The user actually asked to "verifica la integridad" and "refactoriza".
        # Checking if current implementation allows this.
        # If the viewset lacks object-level permission, this might succeed (200), which is a security flaw to fix.
        # Let's assert what we WANT (403) and if it fails (gets 200), we fix the code.

        # Based on current `get_permissions` in `views_api.py`, it only checks `IsAuthenticated`.
        # So this test is EXPECTED TO FAIL (return 200) currently.
        # I will add the test asserting 403, run it, see it fail, then fix `views_api.py`.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
