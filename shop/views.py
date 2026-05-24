from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Product, Category
from .forms import ProductForm, CategoryForm

def home(request):
    featured = Product.objects.all()[:6]
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {
        'featured': featured,
        'categories': categories,
    })

def catalog(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.select_related('category').all()
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories,
    })

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('shop:product_detail', slug=product.slug)
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('shop:catalog_by_category', category_slug=category.slug)
    else:
        form = CategoryForm()
    return render(request, 'shop/category_form.html', {'form': form})