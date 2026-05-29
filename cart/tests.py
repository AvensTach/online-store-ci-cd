from django.test import TestCase
from django.urls import reverse
from users.models import User
from shop.models import Product, Category
from .models import CartItem

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=100, category=self.category)
        self.client.login(username='testuser', password='12345')

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)