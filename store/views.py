from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from carts.models import CartItem
from .models import Product
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        # the above brings slug from Category table 
        products = Product.objects.filter(category=categories, is_available = True)
        # the above category(which is inside Product table) takes value from categories from the above result and filetrs 
        paginator = Paginator(products, 1) # to show only  products in simgle page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        Product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3) # to show only  products in simgle page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) # all the 3 OR WAHT EVER NUMBER products will be stored in paged_products 
        Product_count = products.count()

    
    
    context = {
        'products': paged_products,
        'Product_count': Product_count,
    }
    #if we pass the variable in context then only we can use in the html template
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product  = Product.objects.get(category__slug=category_slug, slug=product_slug)
        #category__slug(2 underscores) is the syntax to get slug which is defined in category model and match(=) with the slug coming from the product_detail function
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product= single_product).exists()
        # cart__cart_id means to get the cart_id from cart is from CartItem class and cart_id is from Cart and exists() returns true or false
        # in_cart gives true of the product is already inside the cart, else it returns False 
        #return HttpResponse(in_cart)
        #exit()
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)