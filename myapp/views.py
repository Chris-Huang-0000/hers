from django.shortcuts import render,redirect
from django.urls import reverse
from myapp.models import *
import csv
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.hashers import make_password,check_password #將密碼轉譯成亂碼
from django.db import transaction
from django.contrib import messages

# Create your views here.
def all(request):
    with open("./product_list.csv","r",encoding="utf-8-sig") as file:
        text = csv.DictReader(file)
        for row in text:
            if any(keyword in row['title'] for keyword in ['Bra','安全褲','無痕褲褲']):
                p_name = row["title"]
                p_price = row['price']
                p_image = row['image']
                p_color = row['color']
                p_color_image = row['color image']
                p_category = 'inner'
                p_stock_quantity = 15
                Products.objects.create(name=p_name,price=p_price,image=p_image,color=p_color,color_image=p_color_image,category=p_category,stock_quantity=p_stock_quantity)
            elif any(keyword in row['title'] for keyword in ['洋裝','套裝','連身褲','吊帶褲']):
                p_name = row["title"]
                p_price = row['price']
                p_image = row['image']
                p_color = row['color']
                p_color_image = row['color image']
                p_category = 'dress'
                p_stock_quantity = 15
                Products.objects.create(name=p_name,price=p_price,image=p_image,color=p_color,color_image=p_color_image,category=p_category,stock_quantity=p_stock_quantity)
            elif any(keyword in row['title'] for keyword in ['上衣','背心','衫','外套','短洋裝','大學T','棉T']):
                p_name = row["title"]
                p_price = row['price']
                p_image = row['image']
                p_color = row['color']
                p_color_image = row['color image']
                p_category = 'shirt'
                p_stock_quantity = 15
                Products.objects.create(name=p_name,price=p_price,image=p_image,color=p_color,color_image=p_color_image,category=p_category,stock_quantity=p_stock_quantity)
            elif any(keyword in row['title'] for keyword in ['褲','裙']):
                p_name = row["title"]
                p_price = row['price']
                p_image = row['image']
                p_color = row['color']
                p_color_image = row['color image']
                p_category = 'pants'
                p_stock_quantity = 15
                Products.objects.create(name=p_name,price=p_price,image=p_image,color=p_color,color_image=p_color_image,category=p_category,stock_quantity=p_stock_quantity)
            elif any(keyword in row['title'] for keyword in ['襪','鞋','靴','帽']):
                p_name = row["title"]
                p_price = row['price']
                p_image = row['image']
                p_color = row['color']
                p_color_image = row['color image']
                p_category = 'shoes_cap'
                p_stock_quantity = 15
                Products.objects.create(name=p_name,price=p_price,image=p_image,color=p_color,color_image=p_color_image,category=p_category,stock_quantity=p_stock_quantity)
            else:
                p_name = row["title"]
                p_price = row['price']
                p_image = row['image']
                p_color = row['color']
                p_color_image = row['color image']
                p_category = 'accessory'
                p_stock_quantity = 15
                Products.objects.create(name=p_name,price=p_price,image=p_image,color=p_color,color_image=p_color_image,category=p_category,stock_quantity=p_stock_quantity)
            
    return HttpResponse("成功")


def hers(request):
    return HttpResponse('Success')

def shirt(request):
    datas = Products.objects.filter(category='shirt')
    object = []
    items = []
    for i in datas:
        if not object or i.name == object[-1].name:
            object.append(i)
        else:
            items.append(object)
            object = [i]
    if object:
        items.append(object)
    return render(request,'products.html',locals())

def accessory(request):
    datas = Products.objects.filter(category='accessory')
    object = []
    items = []
    for i in datas:
        if not object or i.name == object[-1].name:
            object.append(i)
        else:
            items.append(object)
            object = [i]
    if object:
        items.append(object)
    return render(request,'products.html',locals())

def dress(request):
    datas = Products.objects.filter(category='dress')
    object = []
    items = []
    for i in datas:
        if not object or i.name == object[-1].name:
            object.append(i)
        else:
            items.append(object)
            object = [i]
    if object:
        items.append(object)
    return render(request,'products.html',locals())

def inner(request):
    datas = Products.objects.filter(category='inner')
    object = []
    items = []
    for i in datas:
        if not object or i.name == object[-1].name:
            object.append(i)
        else:
            items.append(object)
            object = [i]
    if object:
        items.append(object)
    return render(request,'products.html',locals())

def pants(request):
    datas = Products.objects.filter(category='pants')
    object = []
    items = []
    for i in datas:
        if not object or i.name == object[-1].name:
            object.append(i)
        else:
            items.append(object)
            object = [i]
    if object:
        items.append(object)
    return render(request,'products.html',locals())

def shoes_cap(request):
    datas = Products.objects.filter(category='shoes_cap')
    object = []
    items = []
    for i in datas:
        if not object or i.name == object[-1].name:
            object.append(i)
        else:
            items.append(object)
            object = [i]
    if object:
        items.append(object)
    return render(request,'products.html',locals())

def search(request):
    if 'search_text' in request.GET:
        search_data = request.GET['search_text'].split()

    q_objects = Q()
    for data in search_data:
        q_objects.add(Q(name__contains=data),Q.OR)

    datas = Products.objects.filter(q_objects)
    object = []
    items = []
    for i in datas:
        if not object or i.name == object[-1].name:
            object.append(i)
        else:
            items.append(object)
            object = [i]
    if object:
        items.append(object)
    return render(request,'products.html',locals())


def adduser(request):
    if request.method == "POST":
        try:
            user = Members.objects.get(username=request.POST['name'])
            message = "此帳號已存在!"
            return render(request,"adduser.html",{"message":message})
        except:
            hash_passwd = make_password(request.POST['passwd'])
            user = Members.objects.create(username=request.POST['name'],password=hash_passwd,
                                          email=request.POST['useremail'],address=request.POST['useraddress'],
                                          tel=request.POST['usertel'],first_name=request.POST['userfirst_name'],
                                          last_name=request.POST['userlast_name'])
            user.save()
            message = "會員註冊成功!"
            return render(request,"login.html",{"message":message})
    else:
        return render(request,"adduser.html",locals())

def login(request):
    if request.method == "POST":
        name = request.POST['name']
        passwd = request.POST['passwd']
        try:
            # user = Members.objects.get(username=name)
            user = auth.authenticate(username=name,password=passwd)
            # if check_password(passwd,user.password):
            if user:
                auth.login(request,user)
                request.session.set_expiry(0)
                return redirect("/hers/shirt/")
            else:
                message = "帳號密碼輸入錯誤，請重新輸入!"
        except:
            message = "帳號不存在!"
        return render(request,"login.html",{"message":message})
    else:
        message = request.session.get('message',"")
        return render(request,"login.html",locals())
    
def logout(request):
    auth.logout(request)
    return redirect("/hers/shirt/")


def cart(request):
    if request.user.is_authenticated:
        product = request.GET['product']
        items = Products.objects.filter(name=product)
        # print(items)
        return render(request,"cart.html",locals())
    else:
        request.session['message'] = "請先登入會員!"
        request.session.set_expiry(2)
        return redirect("/login/")


def addcart(request):
    if request.method == "POST":
        product_image = request.POST['selected_image'].split("/")[-1]
        nums = request.POST['productnums']
        user = request.user
        print(product_image,nums)
        print(user)
        try:
            item = Cart.objects.create(product=Products.objects.get(image=product_image),
                                   member=Members.objects.get(username=user),
                                   quantity=nums)
            item.save()
            return JsonResponse({'success':True})
        except:
            return JsonResponse({'success':False})

def cart_list(request):
    if request.user.is_authenticated:
        user = request.user
        items = Cart.objects.filter(member=user)
        if items:
            total_price = 0
            for i in items:
                # print(i.quantity,i.member.first_name,i.product.name)
                total_price += i.quantity*i.product.price
            print(total_price)
            return render(request,"cart_list.html",locals())
        else:
            return HttpResponse("你的購物車是空的喔！") 
    else:
        request.session['message'] = "請先登入會員!"
        request.session.set_expiry(2)
        return redirect("/login/")

def delete_cart_item(request,id=None):
    if id != None:
        item = Cart.objects.get(id=id)
        item.delete()
        messages.success(request,"刪除成功!")
    return redirect("/cart_list/")


def create_order_from_cart(member):
    cart_items = Cart.objects.filter(member=member)
    print(cart_items)
    if not cart_items.exists():
        return None  # 沒有項目就不建立訂單

    with transaction.atomic():
        # 建立一筆 Order
        order = Orders.objects.create(member=member)

        # 建立對應的 OrderItem
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # 清空購物車
        cart_items.delete()

    return order

def checkout(request):
    if request.user.is_authenticated:
        member = request.user  # 假設登入會員與 Members 有關聯
        if request.method == "POST":
            order = create_order_from_cart(member)
            if order:
                return render(request,"order_list.html",{"orders":[order]})
        else:
            order = Orders.objects.filter(order_status="待出貨",member=member)
            if order:
                return render(request,"order_list.html",{"orders":order})
            else:
                return HttpResponse("目前未有成立的訂單！")
    else:
        request.session['message'] = "請先登入會員!"
        request.session.set_expiry(2)
        return redirect("/login/")

