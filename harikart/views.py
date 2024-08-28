from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }

    #return HttpResponse('Home Page')
    return render(request, 'home.html', context)    
    # if we declare context then only we can use products in html file otherwise we cant use that 