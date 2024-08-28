# context processors is a funciton in python which takes request as an argument and returns dictionary of data.
# it is used to list down all categories ( which we can see in the home page as All category)
from .models import Category


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

# it will bring all the categories list and it will store them into the links variable
# i have used the links dictionary in navbar.html
"""
We also need to tell main settings.py that we are using the context processor, 
we are going to tell the templates that we are using context processor.               
add this inside TEMPLATES -> context_processors ->add this 'category.context_processors.menu_links',
So by adding this here, what will happen is we can we will be able to call this, you know, use this menu links in any templates we want. 

"""