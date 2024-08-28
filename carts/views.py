from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
    # this function is to get session id that is cart id and _cart_id means it is a private funciton and coding standard of pep8
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# add the product to the cart, then that means we have a product to add. But where is the cart now?
# we don't have the cart, right? So that's when the session comes in.
# we have a session keys.So what we are going to do is we are going to store the session key as a cart ID

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # to get the product 

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    # we can get cart id that is session id from the left side of (i button)website url which contains cookies folder and inside it sessionID and store it in database
    # underscore cart_id with the request so that it will match the cart id with the session id 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    # the below is to add product into cart so that it becomes cart item
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # when will click add item the cart item quantity should be increased by one
        cart_item.quantity += 1 
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    #return HttpResponse(cart_item.product)
    #return HttpResponse(cart_item.quantity) # it gets every time when we click add to cart button
    #exit()
    return redirect('cart')

def remove_cart(request, product_id):
    # for reducing the quantity number
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')






#this is to remove the whole cart item by clicking remove button
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()
    return redirect('cart')
    




def cart(request, total = 0, quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context ={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }


    return render(request, 'store/cart.html', context)






"""
Let me break down the code for you step by step, explaining what each part does. This code is from your Django `views.py` file, which is handling the functionality for adding a product to the cart and displaying the cart. Here's the detailed breakdown:

### **1. Helper Function: `_cart_id(request)`**

```python
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
```

- **Purpose:** 
  - This function is designed to get or create a session ID, which acts as the "cart ID" for anonymous users (users who haven't logged in). A session is a way to track data for a particular user across multiple requests without requiring them to log in.
  
- **How It Works:** 
  - `request.session.session_key`: This checks whether the user already has a session. If the session key exists, it assigns that key to the variable `cart`.
  - `request.session.create()`: If the session key doesn't exist (i.e., the user doesn't have an active session), it creates a new session and assigns the new session key to `cart`.
  
- **Return Value:** 
  - This function returns the session key, which is used as a unique identifier for the user's cart.

### **2. Function: `add_cart(request, product_id)`**

```python
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # to get the product
```

- **Purpose:** 
  - This function is responsible for adding a product to the cart. When the user clicks "Add to Cart," the product's ID is sent to this view, and the corresponding product is fetched from the database.

- **How It Works:**
  - `product = Product.objects.get(id=product_id)`: It retrieves the product from the database based on the `product_id` passed in the URL.

```python
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
```

- **Purpose:** 
  - This line attempts to retrieve an existing cart from the database by using the session's cart ID. The function `_cart_id(request)` is used to get the current session ID, which is being used as the cart identifier.

- **How It Works:**
  - `Cart.objects.get(cart_id=_cart_id(request))`: It tries to find a cart in the `Cart` model that matches the current user's session ID. If it finds a match, it assigns it to the variable `cart`.

```python
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
```

- **Purpose:** 
  - If the cart does not exist for the session, it creates a new `Cart` instance.

- **How It Works:**
  - `Cart.objects.create(cart_id=_cart_id(request))`: A new cart is created with the session ID as the cart ID.
  - `cart.save()`: This ensures the new cart is saved to the database.

### **3. Adding Items to the Cart**

```python
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 
        cart_item.save()
```

- **Purpose:** 
  - This code tries to find an existing `CartItem` for the product in the current cart and increments the quantity if the item is already in the cart.

- **How It Works:**
  - `CartItem.objects.get(product=product, cart=cart)`: It looks for an existing cart item in the cart that matches both the current `product` and `cart`.
  - `cart_item.quantity += 1`: If the item already exists in the cart, its quantity is increased by 1.
  - `cart_item.save()`: This saves the updated cart item (with the new quantity) back into the database.

```python
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
```

- **Purpose:** 
  - If the product does not already exist in the cart, a new `CartItem` is created with a quantity of 1.

- **How It Works:**
  - `CartItem.objects.create(...)`: This creates a new cart item in the database with the given product, quantity (set to 1), and associated cart.
  - `cart_item.save()`: This saves the new cart item to the database.

### **4. Redirect to the Cart Page**

```python
    return redirect('cart')
```

- **Purpose:** 
  - After adding the item to the cart, the user is redirected to the cart page.
  
- **How It Works:** 
  - `redirect('cart')`: This tells Django to send an HTTP redirect response to the user, pointing them to the view named `'cart'`.

### **5. Cart View: `cart(request)`**

```python
def cart(request):
    return render(request, 'store/cart.html')
```

- **Purpose:** 
  - This function renders the cart page when the user visits the cart URL.

- **How It Works:**
  - `render(request, 'store/cart.html')`: This function renders the `cart.html` template, passing in the `request` object. This template will display the cart contents to the user.

### **Summary of the Flow**

1. **User clicks "Add to Cart" on a product:**
   - The `add_cart` view is called with the `product_id` of the product.

2. **Product and Cart Lookup:**
   - The product is fetched from the `Product` model.
   - The function checks whether a cart exists for the current session using the session key as the cart ID. If no cart exists, it creates one.

3. **Cart Item Handling:**
   - The function then checks whether the product is already in the cart. If it is, it increases the quantity by 1. If it's not, it creates a new `CartItem` with a quantity of 1.

4. **Redirect to Cart Page:**
   - After the product has been added to the cart, the user is redirected to the cart page, where they can see all their cart items.

### **Key Concepts to Understand**

- **Session ID (`_cart_id` function):** This is used to track users who are not logged in, allowing their cart to persist even if they aren't authenticated.
  
- **Database Models (`Product`, `Cart`, `CartItem`):** These are the database tables used to store information about products, the cart, and items in the cart.

- **Try/Except Blocks:** These are used to handle the situation where an item or cart doesn't already exist in the database, allowing the code to create them when necessary.

- **Redirects:** After an action (like adding to the cart), the user is redirected to another page (in this case, the cart page) to continue their interaction with the app.

This setup is a typical approach to implementing a shopping cart in an e-commerce site using Django. Let me know if you need further clarification on any part!
"""