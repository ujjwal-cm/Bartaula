from django.urls import path

from .views import *

app_name="cart"

urlpatterns = [
    path("",CartIndexView.as_view(),name="cart"),
    path("add/<int:product_id>",AddToCartView.as_view(),name="add-cart"),
    path("remove/<int:product_id>",RemoveToCartView.as_view(),name="remove-cart"),
]
