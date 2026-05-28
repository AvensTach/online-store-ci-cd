from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in.")
            return redirect('login')
        if not request.user.is_admin_user():
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('shop:home')
        return view_func(request, *args, **kwargs)
    return wrapper