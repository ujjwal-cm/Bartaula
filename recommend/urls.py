from django.urls import path
from .views import *

app_name="recommend"
urlpatterns = [
    path("",load_data)    
]
