from django.test import TestCase
from usuarios.models import Usuario


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

        # Test the soft_delete method directly
        u.soft_delete()

        self.assertFalse(u.is_active)
        self.assertTrue(".inactiva." in u.email)
        self.assertTrue(".inactiva." in u.username)
