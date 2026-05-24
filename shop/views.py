from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    """
    Main page: show a few featured products and list categories.
    """
    featured = Product.objects.all()[:6]
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {
        'featured': featured,
        'categories': categories,
    })

def catalog(request, category_id=None):
    """
    Catalog page: list all products, optionally filtered by category.
    """
    categories = Category.objects.all()
    products = Product.objects.all()
    current_category = None
    if category_id:
        current_category = get_object_or_404(Category, pk=category_id)
        products = products.filter(category=current_category)
    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    })

def product_detail(request, pk):
    """
    Product details page.
    """
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories,
    })