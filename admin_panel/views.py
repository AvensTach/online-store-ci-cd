from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from shop.models import Product, Category
from orders.models import Order
from django.contrib.auth import get_user_model


@staff_member_required
def dashboard(request):
    User = get_user_model()

    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    orders_count = Order.objects.count()
    users_count = User.objects.count()

    pending_orders = Order.objects.filter(status='pending').count()
    delivered_orders = Order.objects.filter(status='delivered').count()

    recent_orders = Order.objects.select_related('user', 'product').order_by('-created_at')[:10]

    context = {
        'products_count': products_count,
        'categories_count': categories_count,
        'orders_count': orders_count,
        'users_count': users_count,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_panel/dashboard.html', context)

