from django.contrib import messages, auth
from django.shortcuts import render, redirect
from accounts.models import Account
from carts.models import Cart, CartItem
from carts.views import _cart_id
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests 

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # request.POST contains all the feild values 
        if form.is_valid():  # it is used to check if all the feilds are present or not, if yes then we will create a user.
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]  # we are automatically creating a username by taking before the @ of email address
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password) # this will create a user object  
            user.phone_numer = phone_number # this will user with phone number, we cant pass phone_number to the above because we didn't pass the phone number in the create_user of MyAccountManager in models.py
            user.save()  

            # USER ACTIVATION to make verification by sending mail to user
            current_site = get_current_site(request)
            # So we need to get the current site. It is because right now we are using the localhost, but in future we are going to we don't know, we may, we may use a different kind of domains
            # So that's why we need to first get the current site, get current site so we can get it with this request.
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,  # the user after : is object
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
                # go to bottom of this file to know about uid and token
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.')   
            return redirect('/accounts/login/?command=verification&email='+email)
        # the above redirect will show the success message  of the above which is now written in login.html in the 
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        # the email inside post is the name in login.html
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try: # the try is to check if already cart items exist or not
                cart = Cart.objects.get(cart_id=_cart_id(request))  # the _cart_id is in carts views which is used to fetch the cart ID from the browser.
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    # the above is used to bring all the cart items that  are inside the cartId, that are that are already assigned for this cart ID.
                    
                    # Getting the product variations by Cart ID
                    product_variation = []    # this is used to group the products that are added before logging in and they should be combine with the same variation products if alrady there in cart, after logging in 
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation)) # we are using list because varitaion is bydefault a query set. so we are converting into list
                    

                    # get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)   # here the user (after =) means authenticated user  
                    ex_var_list = []  
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation)) 
                        id.append(item.id) 

                    
                    for product in product_variation:
                        if product in ex_var_list:
                            index = ex_var_list.index(product)
                            # the index gives the position of where we found the common item
                            item_id = id[index]
                            item = CartItem.objects.get(id = item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            for item in cart_item:
                                item.user = user
                                item.save()
                            #this is just assigning the user to the cart item

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are a now logged in.')
            #return redirect('dashboard')
            # handling the checkout redirection, instead of asking again user to login even after user is logged in 
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                #print('query-> ', query) it orints after the ? mark part in the url http://127.0.0.1:8000/accounts/login/?next=/carts/checkout/
                # next=/carts/checkout/ , now we need to split the at '='
                params=dict(x.split('=') for x in query.split('&'))
                #print('params -> ', params) # this prints params ->  {'next': '/carts/checkout/'}, we need to redirect the user to this part /carts/checkout/ 
                if 'next' in params:
                    nextPage = params['next']
                return redirect('nextPage') 
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

"""
we are going to send the activation link to the user after the registration and if user 
clicks on that activation link, then only this is active status will be true.(which we can see on admin pannel button)
So after that he can log in. and with superuser you can always login without any problem
superuser means which we created using python manage.py createsuperuser
"""


"""
BESTWAY TO VERIFY USERS USING ACTIVATION LINK:

For the account verification process, we are actually going to send the verification email to the user with the activation link.
So the activation link will contain a token so that so that the link will automatically gets expired after the verification is done.
So this is actually the safest way of activating the users.
"""


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out..')
    return redirect('login')




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # this will decode the uidb64 and send it to the uid 
        user = Account._default_manager.get(pk=uid)  #this will give user object, and we can that to change the is_active status of user to true
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):  # this is used to check the user from the token token  and change status to active
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations!, Your account is activated!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    # activate function is used to activate the user, when user clicks on the link.




@login_required(login_url = 'login')
# the above decorator tells that if you are only logged in then only you can see the dashboard
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
    
    

def  forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']  # taking the email from forgotpassword.html
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email) 

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user, 
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
                # go to bottom of this file to know about uid and token
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email addres. ')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotpassword')        


    return render(request, 'accounts/forgotpassword.html')
    

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # this will decode the uidb64 and send it to the uid 
        user = Account._default_manager.get(pk=uid)  #this will give user object, and we can that to change the is_active status of user to true
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid 
        #  the use of session is that we can access this session later when I'm resetting the password.
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired')
        # so using token is the safest way 
        return redirect('login')    
    

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')   # uid wll only be saved, if we are coming from the validation link
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password and confirm_password do not match')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')



"""
login_required(login_url='login'):

    This decorator ensures that only users who are logged in can access the logout function. 
     If a user tries to log out without being logged in, they are redirected to the login page (login_url='login').
"""


"""
ALL ABOUT THE MAIL THINGS AND STUFF

1.In render_to_string, we pass the template, which is essentially the content of the email(like please verify email and other message). 
Instead of writing the email body directly in the code, we create an HTML template for it.

2.To protect the user’s primary key and securely manage user activation, we encode the user ID using Base64 encoding and generate a unique token. Here's a simplified version:

1. **Encoding User ID**:  
   We use `urlsafe_base64_encode(force_bytes(user.pk))` to encode the user's primary key, hiding the actual ID for security. This ensures the ID is not visible to anyone.

2. **Generating a Token**:  
   The `default_token_generator.make_token(user)` creates a unique token for the user. This token will be used to verify the user's identity during account activation.

3. **Decoding**:  
   Later, when the account is activated, we'll decode the encoded ID and check the token to confirm the user’s authenticity.

So, in short, we are encoding the user ID and creating a token for secure account activation.

"""

"""
email__exact=email

means 
email__exact.
So what this exact will do is it will check if the email address he is entering is exactly same as what we are what we have in the database.
There is another thing exact also. So if we put __iexact, then it will be case insensitive.
__exact is case sensitive.


The correct usage of the filter method requires you to pass keyword arguments in the form of field lookups (e.g., email=email). 

 The filter() method requires keyword arguments like email=email to specify which field and value to filter on.


 the main purpose of chekcing token and all this stuff is actually to know whether this is the secure request or not.
"""

"""
About set_password to save the password instead of user.save()

we have to use this_set password. If you just save the password inside the database, then it is not going to work.
It will either give you an error, otherwise it will not allow you to log in with that password.
Because the set password is actually the inbuilt function of Django.
So what it will do is it will actually take the password and it will hash it.So it will save it in the hashed format.

after save_password, we can save that
"""