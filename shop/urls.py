from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/category/<int:category_id>/', views.catalog, name='catalog_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]