from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products, name='product-list'),
    path('categories/', views.get_categories, name='category-list'),
    path('products/create/', views.create_product, name='product-create'),
    path('products/<int:pk>/update/', views.update_product, name='product-update'),
    path('products/<int:pk>/delete/', views.delete_product, name='product-delete')
]