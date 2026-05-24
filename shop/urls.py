from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/category/<slug:category_slug>/', views.catalog, name='catalog_by_category'),
    path('product/add/', views.product_create, name='product_add'),
    path('category/add/', views.category_create, name='category_add'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]