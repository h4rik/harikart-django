from django.contrib import admin
from .models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')
#the above is to automatically populate the text which we entered on category field, for space in category field it gives one - in slug field.

admin.site.register(Category, CategoryAdmin)
