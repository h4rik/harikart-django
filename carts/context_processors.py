# Counter Context Processor for Cart Icon in Navbar to print the count of items in cart
from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    # if we are inside the admin we dont want to see anything
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:  # if request user is authenticated,then that means the user is any user is logged in. Then give me the count of the cart items for that particular user.Not based on the cart ID.
                cart_items = CartItem.objects.all().filter(user = request.user)
            else: # if the user is not logged in
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            # we only need one result so [:1], even if you have many cart ID's it will give you only one cart ID.
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)

# add this context processors in settings.py of templates 
"""
In Django, context_processors.py is used to define context processors, which are functions that inject additional data into the context of your templates.
Context processors make certain data available to all templates without having to explicitly pass that data in every view.


Use of context_processors.py:
The primary purpose of context_processors.py is to make common data globally available to templates.
This is particularly useful when you need to access the same data (e.g., user information, site settings, cart data, etc.) across multiple views and templates.
"""

