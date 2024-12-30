from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from carts.models import CartItem
from orders.models import OrderProduct
from .models import Product, ReviewRating
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages

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
    
    if request.user.is_authenticated:  #when we dont use this if statement we get error(because of "user=request.user" in the below orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()), when try to see products without logging in.
        try:
            #we use OrderProduct because it is where the user and product info is available
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    #Get the reviews
    # if admin wants to hide some comments, then can set status to False
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct, 
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    # keyword is the attribute passed in input field of search and and we want to value of keyword when someone searches 
    # ex :http://127.0.0.1:8000/store/search/?keyword=shirts here the key is keyword and shirts is value which we want
        if keyword:  # to check if keyword is not blank
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

            # underscore underscore contains means this will look for the whole description and product name of products (both) and 
            # if it found anything related to this keyword,ex: jeans, then it is it will bring that product and show it inside the search result page.
            # and i djnago we cant use | (OR) operator alone with filter ex :description__icontains=keyword | product_name__icontains=keyword the example does not work.
            # and , between those two acts as AND .
            # So we need to use some things called Q, through which we can use OR operator inside filter. 
            Product_count = products.count()

    context = {
        'products': products,
        'Product_count': Product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  # HTTP_REFERER is used to get the url of the previous page.and store it in url variable
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            #inside the request, we are going to have all the stars, review, etc and also we use instance because if there is already an existing review 
            # it will update with the new one for the same user and product, otherwise will create a new review for the new userid and product
            form.save()
            messages.success(request, 'Thank you!, Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
        # if a review and rating does not exist it will create a new record
            form = ReviewForm(request.POST)  
            if form.is_valid():
                data = ReviewRating() # here ReviewRating is a object
                data.subject = form.cleaned_data['subject']  # so here we are taking all the values from the form what user has entered and creating a new record
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you!, Your review has been submitted.')
                return redirect(url)




# In product__id, we use double underscore because inside the ReviewRating class(in models.py) we access the product and its id from Product table which is a foreign key     product = models.ForeignKey(Product, on_delete=models.CASCADE)
