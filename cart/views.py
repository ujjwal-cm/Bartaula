from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.views.generic import View,ListView,DetailView,UpdateView,CreateView
from django.contrib.auth.models import User

from .models import Cart
from product.models import Product
# Create your views here.

class CartIndexView(ListView):
    model=Cart
    template_name="cart/index.html"

    def get(self,request, *args,**kwargs):
        user=request.user
        
        if(not request.user.is_authenticated):
            return redirect("core:login")

        context={
            "page_title":"Cart",
            "user":request.user,
            "cart_items":Cart.objects.filter(user__id=request.user.id),
            "ecommerce_user":user.ecommerce_user.all()[0]

        }
        

        return render(request,self.template_name, context=context)


class AddToCartView(View):
    model=Cart
    template_name="cart/index.html"

    def get(self,request, *args,**kwargs):
        
        if(not request.user.is_authenticated):
            return redirect("core:login")

        product_id=self.kwargs["product_id"]

        user=User.objects.get(id=request.user.id) 
        product=Product.objects.get(id=product_id)

        cart=Cart(user=user,product=product)
        cart.quantity=1
        cart.save()


        return redirect("core:index")


class RemoveToCartView(View):

    model=Cart
    template_name="cart/index.html"


    def get(self,request, *args,**kwargs):
        
        if(not request.user.is_authenticated):
            return redirect("core:login")

        product_id=self.kwargs["product_id"]

        user=User.objects.get(id=request.user.id) 
        product=Product.objects.get(id=product_id)

        cart_items=Cart.objects.filter(user__id=request.user.id).filter(product__id=product_id)
        
        if(len(cart_items)>0):
            cart_items[0].delete()
        

        context={
            "page_title":"Cart",
            "user":request.user,
            "cart_items":Cart.objects.filter(user__id=request.user.id),
            "ecommerce_user":user.ecommerce_user.all()[0]

        }

        return render(request,self.template_name, context=context)
