from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EcommerceUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="ecommerce_user")
    isSeller=models.BooleanField(default=False)