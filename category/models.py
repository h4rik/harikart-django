from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    # slug means url of the category 
    #A slug is the part of a URL that identifies a particular page on a website in an easy-to-read form. 
    description = models.TextField(max_length=240, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    # blank means whether it is optional(true) or compulsory (false)    
    # as we using image field we need to use install pillow package in the environment
    '''
    So we added shirt here and we added the slug manually. So this should not be like this.
    So when we add a new category here, when we add the jeans, this jeans should replicate. 
    It means auto populate inside this slug. Whatever we write in category field, 
    this should automatically generate the category slug. So it is because it is not a good idea to always manually write the slugs.
    so in the above we changed     slug = models.charField(max_length=250, unique=True)
    to     slug = models.SlugField(max_length=250, unique=True)
    and make migrations as we changed field name and 
    also add class CategoryAdmin in admin.py


    ''' 

    '''
    One thing you have to notice here is Django models. Usually when it comes to the Django administration panel, it automatically makes the model into the plural form. 
    So for for making it plural form, it just adds s after the the model name. That means if you create a model called product, then it creates like it adds the s after product that is products.
    But for the category thing, it shows as catogorys ,this is wrong.The spelling is wrong, so in order to handle this case, we just need to write a 1 or 2 lines of code.
    That is we need to create Meta class and add verbose things
    '''
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    # reverse is a function takes the name of the category slug and gives the url of that category.

    def __str__(self):
        return self.category_name
    # the above is called string representation of the model.



"""
Custom User Model:
In the project, the default Django authentication system requires using a username for login. 
However, since most modern applications use an email address for login instead, we will create a custom user model. 
This custom model will override Django's default behavior, allowing us to use email addresses for authentication while still retaining Django's built-in functionality.
 The custom user model will give us the flexibility to tailor the authentication system to our needs.
"""