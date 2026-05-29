from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Making email unique is crucial for an online shop
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def is_admin_user(self):
        """Check if user is in 'admin' group."""
        return self.groups.filter(name='admin').exists()

    def is_customer_user(self):
        """Check if user is in 'customer' group."""
        return self.groups.filter(name='customer').exists()

    # --- Overrides to grant superuser access to 'admin' group users ---
    # Note: For users to log into the admin panel, they MUST manually
    # have the native `is_staff=True` database field checked.

    def has_perm(self, perm, obj=None):
        """
        If the user is in the 'admin' group, they have all permissions.
        """
        if self.is_active and self.is_admin_user():
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        """
        If the user is in the 'admin' group, they have permissions for all modules/apps.
        """
        if self.is_active and self.is_admin_user():
            return True
        return super().has_module_perms(app_label)