from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, Payment, OrderItem
from .forms import OrderForm, CheckoutForm


@login_required(login_url='/login/')
def create_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        return redirect('cart:cart_detail')

    if not cart_items.exists():
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                address=form.cleaned_data['address'],
                status='pending'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )



            return redirect('orders:checkout')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total_amount = cart.get_total_price()

            payment = Payment.objects.create(
                user=request.user,
                cart=cart,
                payment_method=form.cleaned_data['payment_method'],
                amount=total_amount,
                status='completed',
            )

            order = Order.objects.filter(user=request.user, status='pending').last()

            if order:
                order.status = 'paid'
                order.save()

            cart_items.delete()

            messages.success(request, 'Payment successful!')
            return redirect('orders:confirmation', payment_id=payment.id)
    else:
        form = CheckoutForm()

    total_price = cart.get_total_price()
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }

    return render(request, 'orders/checkout.html', context)


@login_required
def payment_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    latest_order = Order.objects.filter(user=request.user, status='paid').order_by('-created_at').first()

    context = {
        'payment': payment,
        'order': latest_order,
    }

    return render(request, 'orders/confirmation.html', context)