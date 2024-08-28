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