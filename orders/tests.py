from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from .models import Order, Payment
from shop.models import Product, Category
from cart.models import Cart, CartItem

User = get_user_model()


class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            price=1000.00,
            category=self.category
        )

        self.cart = Cart.objects.create(user=self.user)

        self.create_order_url = reverse('orders:create_order')
        self.checkout_url = reverse('orders:checkout')
        self.cart_detail_url = reverse('cart:cart_detail')

    def add_item_to_cart(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_create_order_redirects_if_cart_empty(self):
        response = self.client.get(self.create_order_url)
        self.assertRedirects(response, self.cart_detail_url)

    def test_create_order_get_with_items(self):
        self.add_item_to_cart()
        response = self.client.get(self.create_order_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create_order.html')
        self.assertIn('form', response.context)

    def test_create_order_post_valid_data(self):
        self.add_item_to_cart()

        data = {
            'address': 'Kyiv, Khreshchatyk 1'
        }

        response = self.client.post(self.create_order_url, data)
        self.assertRedirects(response, self.checkout_url)

        order_exists = Order.objects.filter(
            user=self.user,
            address='Kyiv, Khreshchatyk 1',
            status='pending'
        ).exists()
        self.assertTrue(order_exists)

        order = Order.objects.get(user=self.user, status='pending')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)

    def test_checkout_redirects_if_cart_empty(self):
        response = self.client.get(self.checkout_url)
        self.assertRedirects(response, self.cart_detail_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your cart is empty.')

    def test_checkout_get_with_items(self):
        self.add_item_to_cart()
        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')
        self.assertIn('form', response.context)
        self.assertIn('total_price', response.context)

    def test_checkout_post_valid_data(self):
        self.add_item_to_cart()

        order = Order.objects.create(user=self.user, address='Test', status='pending')

        data = {
            'payment_method': 'credit_card'
        }

        response = self.client.post(self.checkout_url, data)

        payment = Payment.objects.get(user=self.user, status='completed')
        self.assertEqual(payment.payment_method, 'credit_card')

        order.refresh_from_db()
        self.assertEqual(order.status, 'paid')
        self.assertEqual(self.cart.items.count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Payment successful!')

        confirmation_url = reverse('orders:confirmation', kwargs={'payment_id': payment.id})
        self.assertRedirects(response, confirmation_url)

    def test_payment_confirmation_success(self):
        payment = Payment.objects.create(
            user=self.user,
            cart=self.cart,
            payment_method='credit_card',
            amount=1000.0,
            status='completed',
            shipping_address='Test address'
        )
        order = Order.objects.create(user=self.user, address='Test', status='paid')

        url = reverse('orders:confirmation', kwargs={'payment_id': payment.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/confirmation.html')
        self.assertEqual(response.context['payment'], payment)
        self.assertEqual(response.context['order'], order)

    def test_payment_confirmation_404_for_other_user(self):
        other_user = User.objects.create_user(
            username='other',
            email='other@mail.com',
            password='testpassword'
        )
        payment = Payment.objects.create(
            user=other_user,
            cart=None,
            payment_method='paypal',
            amount=500.0,
            status='completed',
            shipping_address='Other address'
        )

        url = reverse('orders:confirmation', kwargs={'payment_id': payment.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)