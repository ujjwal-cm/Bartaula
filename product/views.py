from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.views.generic import View,ListView,DetailView,UpdateView,CreateView
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from .models import Product
# Create your views here.

from django.core.paginator import Paginator

class IndexView(ListView):
    model=Product
    template_name="product/index.html"

    def get(self,request, *args,**kwargs):

        if(not request.user.is_authenticated and request.user.ecommerceUser.isSeller==False):
            redirect("core:home")

        user=request.user
        query=Product.objects.filter(owner__id=user.id)

        if("search_query" in request.GET):
            query=Product.objects.filter(owner__id=user.id).filter(product_name__contains=request.GET["search_query"])

        p=Paginator(query,10)

        page_num=1

        if "page" in request.GET:
            page_num=request.GET["page"]

        page=p.page(page_num)




        context={
            "page_title":"Homepage",
            "user":user,
            "products":page.object_list,
            "ecommerce_user":user.ecommerce_user.all()[0]
        }

        return render(request,self.template_name, context=context)
    



class ProductDetailView(DetailView):
    model=Product
    template_name="product/product_detail.html"
    context_object_name="prd"


def AddProductView(req):

    if(not req.user.is_authenticated and req.user.ecommerceUser.isSeller==False):
        redirect("core:home")
    
    if req.method=="POST":
        product_image=req.FILES["product_image"]

        fs=FileSystemStorage()
        filename=fs.save(product_image.name,product_image)
        url=fs.url(filename)

        

        product_name=req.POST["product_name"]
        product_description=req.POST["product_description"]
        product_price=req.POST["product_price"]
        product_slug=req.POST["product_slug"]
        
        product=Product(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            slug=product_slug,
            owner=req.user,
            product_image=url
        )

        product.save()

        return redirect("product:product_index")

    else:
        user=req.user
        context={
            "page_title":"Add Product",
            "user":user
        
        }

    return render(req,"product/add_product.html", context=context)


    
def UpdateProductView(req,id):

    if(not req.user.is_authenticated and req.user.ecommerceUser.isSeller==False):
        redirect("core:home")
    
    if req.method=="POST":
        product_image=req.FILES["product_image"]

        fs=FileSystemStorage()
        filename=fs.save(product_image.name,product_image)
        url=fs.url(filename)

        product_name=req.POST["product_name"]
        product_description=req.POST["product_description"]
        product_price=req.POST["product_price"]
        product_slug=req.POST["product_slug"]

        product=Product.objects.get(id=id)

        product.product_name=product_name
        product.product_description=product_description
        product.product_price=product_price
        product.product_image=url
        product.slug=product_slug
        
        product.save()
        return redirect("product:product_index")


    else:
        user=req.user
        context={
            "page_title":"Update Product",
            "user":user,
            "prd":Product.objects.get(id=id)
        
        }

    return render(req,"product/edit_product.html", context=context)


def RemoveProductView(req,id):
    Product.objects.get(id=id).delete()

    return redirect("product:product_index")

    
