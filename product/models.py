from django.db import models
from django.contrib.auth.models import User


class file(models.Model):
  file=models.ImageField(upload_to="media")
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_code = models.CharField(max_length=10)
    product_price = models.CharField(max_length=10)
    product_image=models.ImageField(upload_to="product_image")
    
    def __str__(self):
        return self.product_name

    def check_valid_format_of_code(self):
      if self.product_code == 'CharField':
        return True
      else:
        return False
    
    def check_valid_product_price(self):
      if self.product_price > 100:
        print("product available")
        return True
      else :

        return False


    

class customerDetail(models.Model):
    customer_name=models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    customer_address=models.CharField(max_length=200)
    customer_contact=models.CharField(max_length=200)
    
    def __str__(self):
        return self.customer_name
      
    def check_total_contact_list(self):
      if self.customer_contact > 20:
        print("max contact")
        return True
      else:
        print("min contact")
        return False
    
    def check_contact_detail_of_customer(self):
      return self.customer_address