from django.test import TestCase
from accounts.models import CustomUser


class CustomUserModelTests(TestCase):

    def test_create_user_with_email(self):
        user = CustomUser.objects.create_user(
            email='test@EXAMPLE.com',
            password='pass1234'
        )
        self.assertEqual(user.email, 'test@example.com')

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email=None, password='pass')

    def test_create_user_without_password_raises(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='test@test.com', password=None)

    def test_default_role_is_traveler(self):
        user = CustomUser.objects.create_user(
            email='test@test.com',
            password='pass1234'
        )
        self.assertEqual(user.role, CustomUser.RoleChoices.TRAVELER)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email='admin@test.com',
            password='admin123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, CustomUser.RoleChoices.ADMIN)

    def test_is_admin_property(self):
        user = CustomUser.objects.create_user(
            email='admin@test.com',
            password='pass',
            role=CustomUser.RoleChoices.ADMIN
        )
        self.assertTrue(user.is_admin)

    def test_get_full_name(self):
        user = CustomUser.objects.create_user(
            email='test@test.com',
            password='pass',
            first_name='Ivan',
            last_name='Ivanov'
        )
        self.assertEqual(user.get_full_name(), 'Ivan Ivanov')
