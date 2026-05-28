from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import CartItem

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart/cart_detail.html', {'items': items})