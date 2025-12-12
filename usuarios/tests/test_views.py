from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario


class AuthViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create(username="testuser", email="test@mail.com")
        self.user.set_password("secret")
        self.user.save()
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "secret"}
        )
        # Check redirection
        self.assertEqual(response.status_code, 302)
        # Check session
        self.assertTrue(int(self.client.session["_auth_user_id"]) == self.user.id)

    def test_login_failure(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Usuario o contraseña incorrectos"
        )  # Or generic error form AuthenticationForm
        # Usually AuthenticationForm puts errors in non_field_errors
        # But we added a message in view too, let's see which one triggers first or if both.
        # Actually in our view we added messages.error ONLY if form is NOT valid,
        # but AuthenticationForm is not valid if auth fails.
        # So expectation is correct.

    def test_logout(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        # Check session cleared
        self.assertFalse("_auth_user_id" in self.client.session)
