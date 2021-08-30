from django.urls import path
from .views import *

app_name="product"

urlpatterns = [
    path("",IndexView.as_view(),name="product_index"),
    path("post_product/",AddProductView,name="add_product"),
    path("update_product/<int:id>",UpdateProductView, name="update_product"),
    path("remove_product/<int:id>",RemoveProductView,name="delete_product"),
    path("product_detail/<int:pk>/",ProductDetailView.as_view(),name="product_detail")
]
