from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:home')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('shop:home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': 'Username taken'})
        user = User.objects.create_user(username=username, email=email, password=password)
        from django.contrib.auth.models import Group
        customer_group = Group.objects.get(name='customer')
        user.groups.add(customer_group)
        login(request, user)
        return redirect('shop:home')
    return render(request, 'users/register.html')