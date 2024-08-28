from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        # the above brings slug from Category table 
        products = Product.objects.filter(category=categories, is_available = True)
        # the above category(which is inside Product table) takes value from categories from the above result and filetrs 
        Product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        Product_count = products.count()
    
    
    context = {
        'products': products,
        'Product_count': Product_count,
    }
    #if we pass the variable in context then only we can use in the html template
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product  = Product.objects.get(category__slug=category_slug, slug=product_slug)
        #category__slug(2 underscores) is the syntax to get slug which is defined in category model and match(=) with the slug coming from the product_detail function
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)