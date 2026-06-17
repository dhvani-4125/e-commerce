from django.contrib import admin
from .models import Product, Category, UserProfile, Order, OrderItem

admin.site.register(Product)
admin.site.register(Category)   
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)