from django.contrib import admin
from .models import Product

# Register your models here.
# to auto prepoluate slug
class ProductAdmin(admin.ModelAdmin):
    # list display means, things to appear on the admin pannel
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name', )}


admin.site.register(Product, ProductAdmin)