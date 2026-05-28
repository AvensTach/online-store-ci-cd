from django.test import TestCase
from django.urls import reverse
from users.models import User
from shop.models import Product
from .models import CartItem

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Test Product', price=100)
        self.client.login(username='testuser', password='12345')

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 1)