from django.contrib import admin
from .models import Product, Variation

# Register your models here.
# to auto prepoluate slug
class ProductAdmin(admin.ModelAdmin):
    # list display means, things to appear on the admin pannel
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name', )}

# we dont want the variaitons to be shown like this Variation object (2), to do that make the below class to show all the variations in a tabular format
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')



admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)