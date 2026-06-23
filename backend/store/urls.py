from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

urlpatterns = [
  path('register/', views.register_view),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('products/', views.get_products),
  path('products/create/', views.create_product),
  path('products/update/<int:pk>/', views.update_product),
  path('products/delete/<int:pk>/', views.delete_product),
  path('categories/', views.get_categories),
  path('cart/', views.get_cart),
  path('cart/add/', views.add_to_cart),
  path('cart/remove/', views.remove_from_cart),
  path('cart/update/', views.update_cart_quantity),
  path('orders/create/', views.create_order),
  #CBVs
    path('register/', views.RegisterView.as_view()),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('products/',views.ProductListView.as_view()),
    path('products/create/',views.CreateProductView.as_view()),
    path('products/update/<int:pk>/',views.UpdateProductView.as_view()),
    path('products/delete/<int:pk>/',views.DeleteProductView.as_view()),
    path('categories/',views.CategoryListView.as_view()),
    path('cart/',views.CartView.as_view()),
    path('cart/add/',views.AddToCartView.as_view()),
    path('cart/update/',views.UpdateCartQuantityView.as_view()),
    path('cart/remove/',views.RemoveFromCartView.as_view()),
    path('orders/create/',views.CreateOrderView.as_view()),
]
