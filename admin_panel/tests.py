from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product, Category
from orders.models import Order

User = get_user_model()


class DashboardViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff_admin',
            email='staff@test.com',
            password='password',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular_user',
            email='user@test.com',
            password='password'
        )

        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            price=1000.0,
            category=self.category
        )

        Order.objects.create(user=self.regular_user, address='Test', status='pending')
        Order.objects.create(user=self.regular_user, address='Test', status='paid')

        self.client = Client()
        self.dashboard_url = reverse('admin_panel:dashboard')

    def test_dashboard_redirects_anonymous_user(self):
        response = self.client.get(self.dashboard_url)


    def test_dashboard_redirects_regular_user(self):
        self.client.login(username='regular_user', password='password')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)

