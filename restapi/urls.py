from django.urls import path
from .views import *

urlpatterns = [
    path('product/',view_get_post_product),
    path('products/<int:ID>',view_get_update_delete_product),
    path('productes/PageNo=<int:PAGENO>/Size=<int:SIZE>',view_product_pagination),
]