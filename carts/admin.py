from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)

"""
The admin.site.register() function takes two or three arguments: the model class, the admin class, and optionally a custom admin site.

"""