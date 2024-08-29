from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    Images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # as we are using category we used that here
    # What this models.Cascade will do is whenever we delete the category, the products attached to that category will be deleted. So we want to delete all the products then we delete the category itself.
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
        # this is to get url when we click on product card on home or store page http://127.0.0.1:8000/, it should go to that particular product page(that is product_detail.html of that product)
    
    # string representation of our model
    def __str__(self):
        return self.product_name

# variation manager is used to modify the query set 
# earlier when we add new size variation in the database, it would appear in choose color dropdown in product_detail.html
# so by using VariationManager we can chnage that
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    




variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
# the above choice will go to  choices=variation_category_choice here and so that it will make a drop down list in the admin pannel



#  WE ARE using variation class to make the color and size dynamic nature earlier we can see that, we have used <select> and that stuff
# which is static in nature so we are using this variation class to dynamic values for a particular products
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # cascade means if the product is deleted, then the variation should also be deleted.
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()


    #def __unicode__(self):
        #return self.product
    # we should not use str because we dont want string , we want the variation be added in the database
    def __str__(self):
        return self.variation_value