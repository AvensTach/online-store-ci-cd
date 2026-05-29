from django.contrib import admin
from .models import Order, Payment,OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'address')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Order Information', {'fields': ('user', 'status', 'created_at')}),
        ('Delivery', {'fields': ('address',)}),
    )
    inlines = [OrderItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at')
