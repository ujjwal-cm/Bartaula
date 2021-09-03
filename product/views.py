from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Template, Context
from .models import Product, file
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def view_add_product(request):
    return render(request, "add_product.html")


def view_index(request):
    list_of_products = Product.objects.all()[:3]
    context_variable = {"products": list_of_products}

    return render(request,"index.html", context_variable)

def view_dashboard(request):
    list_of_products = Product.objects.all()[:3]
    context_variable = {"products": list_of_products}
    return render (request,"dashboard.html", context_variable)

def view_product_lists(request):
    list_of_products = Product.objects.all()
    context_variable = {"products": list_of_products}
    return render(request, "display_product.html", context_variable)


def view_productdata_save(request):
    if request.method == "POST":
        # get_all = request.POST
        get_name = request.POST["product_name"]

        get_code = request.POST["product_code"]
        get_price = request.POST["product_price"]
        # get_image = request.POST['product_image']
        # img = request.FILES['product_image']
        # Bookfile = file(product_image = img)
        # Bookfile.save()
        product_obj = Product(
            product_name=get_name, product_code=get_code, product_price=get_price
        )
        product_obj.save()
        return HttpResponse("Record saved")
    else:
        return HttpResponse("Error record saving")


def view_productdata_updateform(request, ID):

    product_obj = Product.objects.get(id=ID)

    context_varible = {"product": product_obj}
    return render(request, "update_product.html", context_varible)


def view_update_form_data_in_db(request, ID):
    product_obj = Product.objects.get(id=ID)

    product_form_data = request.POST

    product_obj.product_name = request.POST["product_name"]
    product_obj.product_code = request.POST["product_code"]
    product_obj.product_price = request.POST["product_price"]
    # product_obj.product_image = request.POST['product_image']

    product_obj.save()
    return HttpResponse("Record Updated!!")


def view_delete(request, ID):
    product_obj = Product.objects.get(id=ID)
    product_obj.delete()
    return HttpResponse("deleted")


def view_login_page(request):
    return render(request, "register_user.html")


def view_register_user(request):
    if request.method == "GET":
        return render(request, "register_user.html")
    else:
        print(request.POST)
        user = User.objects.create_user(
            username=request.POST["input_username"],
            password=request.POST["input_password"],
            email=request.POST["input_email"],
        )
        user.save()
        return render(request, "add_product.html")


@csrf_exempt
def view_authenticate_user(request):

    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        print(request.POST)
        user = authenticate(
            username=request.POST["input_username"],
            password=request.POST["input_password"],
        )
        print(user)
        if user is not None:

            login(request, user)
            list_of_products = Product.objects.all()
            context_variable = {"products": list_of_products}

            return render(request, "page.html", context_variable)
        else:
            return HttpResponse("Authentication Failed")
    else:
        return HttpResponse("asdsadsad")


# def view_logout(request):
#     try:
#         del request.session['input_username']
#     except:
#     pass
#     return render(request, 'login.html')


def view_logout_request(request):
    logout(request)
    return render(request, "index.html")


def view_our_product(request):
    list_of_products = Product.objects.all()
    context_variable = {"products": list_of_products}

    return render(request, "product.html", context_variable)


# def view_search(request):
#     print(request.method)
#     print(request.GET)
#     if request.method=='GET':
#         input=request.GET['search']
#         match=Product.objects.filter(Q(product_name__startswith=input))
#         if match:
#             return render(request,'search.html',{'source':match})
#         else:
#             return HttpResponse('not found')
#     else: return HttpResponse('error')


def view_search(request):
    if request.method == "POST":
        srh = request.POST["search"]

        if srh:
            match = Product.objects.filter(product_name__icontains=srh)

            if match:
                return render(request, "search.html", {"sr": match})
            else:
                return HttpResponse("Item Not found")
        else:
            return "Not success"
    else:
        return render(request, "search.html")


def view_upload(request):
    return render(request, "upload.html")


def view_uploaded_files(request):
    list_of_files = file.objects.all()
    context_variable = {"files": list_of_files}

    return render(request, "display_files.html", context_variable)


def view_upload_pic(request):

    img = request.FILES["file"]
    print(img)
    Bookfile = file(file=img)
    Bookfile.save()
    return HttpResponse("File Uploaded!!")


def view_contact(request):
    return render(request, "contact.html")

