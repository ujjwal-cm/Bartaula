from django.contrib import admin
from .models import Product, customerDetail, file

# Register your models here.
admin.site.register(Product)
admin.site.register(customerDetail)
admin.site.register(file)
