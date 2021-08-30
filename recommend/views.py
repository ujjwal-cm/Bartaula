from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import pandas as pd
import numpy as np

from product.models import Product
from django.contrib.auth.models import User
# Create your views here.

def load_data(req):
    df=pd.read_csv("recommend/data/dataset.csv")
    for index,row in df.iterrows():
        
        title=(row["Title"])
        des=row["Cleaned_Ingredients"]
        img="/media/images/"+row["Image_Name"]+".jpg"

        user=User.objects.get(id=1)

        product=Product(product_name=title,product_description=des,product_image=img,owner=user)
        product.save()



    return HttpResponse("DONE")

