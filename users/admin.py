from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # This controls what columns you see in the admin list view
    list_display = ['username', 'email', 'is_staff', 'is_active']

    # If you add custom fields later, you will add them to fieldsets here
    # fieldsets = UserAdmin.fieldsets + (
    #     ('Extra Info', {'fields': ('phone_number',)}),
    # )