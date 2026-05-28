from io import BytesIO
from decimal import Decimal
from unittest.mock import patch
import tempfile
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from shop.models import Category, Product, ProductImage


def _image_file(name="test.jpg", size=(10, 10), color=(255, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file_obj, format="JPEG")
    file_obj.seek(0)
    return SimpleUploadedFile(name, file_obj.read(), content_type="image/jpeg")


# Use a temp directory for media during tests
TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ShopModelTests(TestCase):
    def test_category_slug_is_auto_generated(self):
        category = Category.objects.create(name="Mobile Phones")
        self.assertEqual(category.slug, "mobile-phones")

    def test_category_slug_is_unique(self):
        Category.objects.create(name="Mobile Phones")
        second = Category.objects.create(name="Mobile Phones")
        self.assertEqual(second.slug, "mobile-phones-1")

    def test_product_slug_is_auto_generated(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="iPhone 15",
            price=Decimal("999.99"),
            description="Smartphone",
            category=category,
        )
        self.assertEqual(product.slug, "iphone-15")

    def test_product_main_image_returns_first_image(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Camera",
            price=Decimal("49.99"),
            description="Nice camera",
            category=category,
        )
        first = ProductImage.objects.create(product=product, image=_image_file("1.jpg"), order=0)
        second = ProductImage.objects.create(product=product, image=_image_file("2.jpg"), order=1)

        self.assertEqual(product.main_image, first)
        self.assertNotEqual(product.main_image, second)


class ShopViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Headphones",
            price=Decimal("59.99"),
            description="Good sound",
            category=self.category,
        )
        ProductImage.objects.create(product=self.product, image=_image_file(), order=0)

        User = get_user_model()
        self.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="pass12345",
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="pass12345",
        )
        admin_group, _ = Group.objects.get_or_create(name="admin")
        customer_group, _ = Group.objects.get_or_create(name="customer")
        self.admin.groups.add(admin_group)
        self.customer.groups.add(customer_group)

    def test_home_page_loads(self):
        response = self.client.get(reverse("shop:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Headphones")

    def test_catalog_page_loads(self):
        response = self.client.get(reverse("shop:catalog"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Headphones")

    def test_catalog_category_filter_works(self):
        response = self.client.get(reverse("shop:catalog_by_category", args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_uses_slug(self):
        response = self.client.get(reverse("shop:product_detail", args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_404_for_numeric_id_url(self):
        response = self.client.get("/product/1/")
        self.assertEqual(response.status_code, 404)

    def test_admin_buttons_hidden_for_anonymous(self):
        response = self.client.get(reverse("shop:product_detail", args=[self.product.slug]))
        self.assertNotContains(response, "Edit")
        self.assertNotContains(response, "Delete")

    def test_admin_buttons_visible_for_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("shop:product_detail", args=[self.product.slug]))
        self.assertContains(response, "Edit")
        self.assertContains(response, "Delete")

    def test_product_create_redirects_anonymous_to_login(self):
        response = self.client.get(reverse("shop:product_add"))
        self.assertEqual(response.status_code, 302)

    def test_product_create_is_allowed_for_admin(self):
        self.client.force_login(self.admin)
        with patch("shop.views.messages.success"):
            response = self.client.post(
                reverse("shop:product_add"),
                data={
                    "name": "Mouse",
                    "price": "19.99",
                    "description": "Wireless mouse",
                    "category": self.category.id,
                    "images": [_image_file()],
                },
            )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name="Mouse").exists())

    def test_product_edit_is_allowed_for_admin(self):
        self.client.force_login(self.admin)
        with patch("shop.views.messages.success"):
            response = self.client.post(
                reverse("shop:product_edit", args=[self.product.slug]),
                data={
                    "name": "Headphones Pro",
                    "price": "79.99",
                    "description": "Better sound",
                    "category": self.category.id,
                },
            )
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Headphones Pro")

    def test_product_delete_is_allowed_for_admin(self):
        self.client.force_login(self.admin)
        with patch("shop.views.messages.success"):
            response = self.client.post(reverse("shop:product_delete", args=[self.product.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())


class ShopAdminPermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.customer = User.objects.create_user(
            username="customer2",
            email="customer2@example.com",
            password="pass12345",
        )
        customer_group, _ = Group.objects.get_or_create(name="customer")
        self.customer.groups.add(customer_group)
        self.category = Category.objects.create(name="Audio")

    def test_customer_cannot_access_product_create(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse("shop:product_add"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shop:home"), fetch_redirect_response=False)