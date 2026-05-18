from django.shortcuts import render, redirect
from .forms import OrderForm

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})