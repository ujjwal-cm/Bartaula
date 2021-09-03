from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
import json

# Create your views here.


@csrf_exempt
def view_get_post_product(request):
    print("What's the request => ",request.method)
    if request.method == "GET":
        print("Queryset obj python_dictionary_objs =>  ",products_queryset)
        list_of_products = list(products_queryset.values("product_code","product_price"))
        print("list of product obj python_dictionary_objs =>",list_of_products)
        dictionary_obj = {
           "products":list_of_products
        }
        return JsonResponse(dictionary_obj)
    elif request.method == "POST":
        print("Request body content =>", request.body)
        print("Request body type =>", type(request.body))
        python_dictionary_obj = json.loads(request.body)
        print("Python dictionary contents=>",python_dictionary_obj)
        print("Python dictionary type=>",type(python_dictionary_obj))
        print(python_dictionary_obj['product_name'])
        print(python_dictionary_obj['product_code'])
        print(python_dictionary_obj['product_price'])
        Product.objects.create(product_name=python_dictionary_obj['product_name'],product_code=python_dictionary_obj['product_code'],product_price=python_dictionary_obj['product_price'])
        return JsonResponse({
            "message":"The document successfully posted!!"
        })
    else:
        return HttpResponse(" verbs testing of HTTP")

@csrf_exempt 
def view_get_update_delete_product(request,ID):
    print("What's the request =>",request.method)
    if request.method == "GET":
        product = Product.object.get(id=ID)

    
        print(product)
        dict ={ 
            "product_name":product.product_name,
            "product_code":product.product_code,
            "product_price":product.product_price
        }
        return JsonResponse(dict)

    elif request.method == "DELETE":
        product = Product.objects.get(id = ID)
        product.delete()
        return JsonResponse({
            "message":"Successfully deleted!!"
        })

    elif request.method == "PUT":
        update = json.loads(request.body)
        product = Product.objects.get(id = ID)
        product.product_name = update['product_name']
        product.product_code = update['product_code']
        product.product_price = update['product_price']
        product.save()
        return JsonResponse({
            "message":"Successfully Updated!!"})

    else:
        return JsonResponse({
        "message":" Testing is error"
        }) 

@csrf_exempt 
def view_product_pagination(request,PAGENO,SIZE):
    skip=SIZE*(PAGENO -1)
    product=Product.objects.values() [skip:(PAGENO*SIZE)]
    
    dict={
        "product":list(product.values("product_name","product_code","product_price"))
        }
    return JsonResponse(dict)
        
    
