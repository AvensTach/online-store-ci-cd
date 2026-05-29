from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserModelTests(TestCase):
    def test_email_is_unique(self):
        User.objects.create_user(
            username="user1",
            email="unique@example.com",
            password="pass12345",
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="user2",
                email="unique@example.com",
                password="pass12345",
            )

    def test_role_helpers(self):
        user = User.objects.create_user(
            username="roleuser",
            email="roleuser@example.com",
            password="pass12345",
        )
        admin_group, _ = Group.objects.get_or_create(name="admin")
        customer_group, _ = Group.objects.get_or_create(name="customer")

        self.assertFalse(user.is_admin_user())
        self.assertFalse(user.is_customer_user())

        user.groups.add(admin_group)
        user.refresh_from_db()
        self.assertTrue(user.is_admin_user())
        self.assertFalse(user.is_customer_user())

        user.groups.add(customer_group)
        user.refresh_from_db()
        self.assertTrue(user.is_admin_user())
        self.assertTrue(user.is_customer_user())


class AuthViewTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name="customer")
        self.user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="pass12345",
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_authenticates_user(self):
        response = self.client.post(
            reverse("login"),
            data={"username": "loginuser", "password": "pass12345"},
        )
        self.assertEqual(response.status_code, 302)

    def test_register_view_creates_customer_user(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "pass12345",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

        created = User.objects.get(username="newuser")
        self.assertTrue(created.groups.filter(name="customer").exists())