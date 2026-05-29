from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm
from .decorators import admin_required

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

    # Category filter
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    # Price range filter
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        try:
            products = products.filter(price__gte=float(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            products = products.filter(price__lte=float(price_max))
        except ValueError:
            pass

    # Ordering
    sort_by = request.GET.get('sort_by', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('name')

    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'price_min': price_min,
        'price_max': price_max,
        'sort_by': sort_by,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.images.all()
    categories = Category.objects.all()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'images': images,
        'categories': categories,
    })

@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save()
            for idx, f in enumerate(files):
                ProductImage.objects.create(product=product, image=f, order=idx)
            messages.success(request, f"Product '{product.name}' created successfully.")
            return redirect('shop:product_detail', slug=product.slug)
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form, 'action': 'Create'})

@admin_required
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        files = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save()
            for idx, f in enumerate(files):
                ProductImage.objects.create(product=product, image=f, order=idx)
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('shop:product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {
        'form': form,
        'product': product,
        'action': 'Edit'
    })

@admin_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' deleted successfully.")
        return redirect('shop:catalog')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})

@admin_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created successfully.")
            return redirect('shop:catalog_by_category', category_slug=category.slug)
    else:
        form = CategoryForm()
    return render(request, 'shop/category_form.html', {'form': form, 'action': 'Create'})