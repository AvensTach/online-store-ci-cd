from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Making email unique is crucial for an online shop
    email = models.EmailField(unique=True)

    # You can add more fields here later (e.g., phone_number, shipping_address)

    def __str__(self):
        return self.username