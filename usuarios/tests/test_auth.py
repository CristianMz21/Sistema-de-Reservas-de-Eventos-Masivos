from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from usuarios.models import Usuario


class AuthenticationTests(APITestCase):
    def test_custom_token_claims(self):
        # Create user
        user = Usuario.objects.create(
            username="jwtuser", email="jwt@mail.com", tipo_usuario="organizador"
        )
        user.set_password("jwtpass")
        user.save()

        # Get token
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "jwtuser", "password": "jwtpass"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check standard tokens
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Check custom user data
        self.assertIn("user", response.data)
        user_data = response.data["user"]
        self.assertEqual(user_data["username"], "jwtuser")
        self.assertEqual(user_data["tipo_usuario"], "organizador")
        self.assertEqual(str(user.uuid), user_data["uuid"])
