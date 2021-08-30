from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.views.generic import View,ListView,DetailView,UpdateView,CreateView
from product.models import Product
from cart.models import Cart
from .models import EcommerceUser

from django.core.paginator import Paginator

import pandas as pd

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class IndexView(ListView):
    model=Product
    template_name="product/index.html"

    def get(self,request, *args,**kwargs):
        user=request.user

        ecommerce_user=""

        if user.is_authenticated:
            ecommerce_user=user.ecommerce_user

        next_page=1
        prev_page=0
        recommendation=[]
        query=Product.objects.all()
        if("search_query" in request.GET):
            search_query=request.GET["search_query"]
            query=Product.objects.filter(product_name__contains=search_query)       
            recommendation=getRecommendation(query[0],10)
    



        p=Paginator(query,10)

        page_num=1

        if "page" in request.GET:
            page_num=request.GET["page"]
        
        page=p.page(page_num)

        next_page=page.next_page_number()
               

        context={
            "page_title":"Homepage",
            "user":user,
            "products":page.object_list,
            "ecommerce_user":ecommerce_user,
            "next_page":next_page,
            "recommendation":recommendation
        }

        return render(request,self.template_name, context=context)
    

def Login(req):

    if req.user.is_authenticated:
            return redirect("core:index")

    if req.method=="GET":
        context={
            "page_title":"login"
        }
        return render(req,"core/login.html",context=context)
    else:
        username=req.POST["username"]
        password=req.POST["password"]
        user=authenticate(username=username,password=password)
        if(user!=None):
            login(req,user)
            return redirect("core:index")
        else:
            return redirect("core:login")



def Sign_Up(req):
    if req.user.is_authenticated:
            return redirect("core:index")

    if req.method=="GET":
        context={
            "page_title":"Sign Up"
        }
        return render(req,"core/sign_up.html",context=context)
    else:
        username=req.POST["username"]
        password=req.POST["password"]
        email=req.POST["email"]

        user=User.objects.create_user(email=email,username=username,password=password)
        user.save()

        ecommerce_user=EcommerceUser(user=user,isSeller=False)
        ecommerce_user.save()

        return redirect("core:login")

def UserSetting(req):

    user=req.user

    if not req.user.is_authenticated:
            return redirect("core:index")

    if req.method=="POST":
        ecommerce_user=EcommerceUser.objects.get(user__id=req.user.id)
        
        ecommerce_user.isSeller=True if ("isSeller" in req.POST) else (False)
        ecommerce_user.save()
        return redirect("core:user_setting")
    else:
        context={
            "page_title":"User Setting",
            "user":req.user,
            "ecommerce_user":user.ecommerce_user.all()[0]

        }
        return render(req,"core/setting.html",context=context)
        
def Logout(req):
    logout(req)
    return redirect("core:login")



def getRecommendation(search_term,number_of_recommendation):

    id=(search_term.id)

    products=Product.objects.all()

    df=pd.DataFrame(products.values("id","product_description"))

    cv=CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)
    
    count_matrix=cv.fit_transform(df["product_description"]) 
    cosine_sim=cosine_similarity(count_matrix)

    similar_foods=list(enumerate(cosine_sim[id-1]))

    sorted_similar_food = sorted(similar_foods,key=lambda x:x[1],reverse=True)
    
    i=0
    recommendation=[]
    for element in sorted_similar_food:
        try:
            print(element[0])
            recommendation.append(Product.objects.get(id=element[0]))
        except:
            continue
        i=i+1
        if i > number_of_recommendation:
            break
    return recommendation


