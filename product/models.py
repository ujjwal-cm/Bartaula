from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

app_name="products"

class Product(models.Model):

    product_name=models.TextField(max_length=200)
    product_description=models.TextField()
    product_price=models.FloatField(null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner")
    product_image=models.ImageField(null=True)
    updated=models.DateTimeField(auto_now=True)
    published=models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("product:product_detail", args=[self.id])
    
    class Meta:
        ordering=['-published']

    def __str__(self):
        return self.product_name
    
    


