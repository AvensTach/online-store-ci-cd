from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not request.user.is_authenticated:
        return redirect('login')
    items = CartItem.objects.filter(cart__user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'items': items})

def add_one(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart:cart_detail')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart:cart_detail')