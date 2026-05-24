from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Making email unique is crucial for an online shop
    email = models.EmailField(unique=True)

    # You can add more fields here later (e.g., phone_number, shipping_address)

    def __str__(self):
        return self.username

    def is_admin_user(self):
        """Check if user is in 'admin' group."""
        return self.groups.filter(name='admin').exists()

    def is_customer_user(self):
        """Check if user is in 'customer' group."""
        return self.groups.filter(name='customer').exists()