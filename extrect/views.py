from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
# def category(request, slug):
#     categorys = get_object_or_404(Category,slug=slug)
#     products = Product.objects .filter(category=category)
#     context = {'category':categorys,'product':products}
#     return render(request, '')

def home(request):
    product = Product.objects.all()
    context = {'products':product}

    return render(request,'index.html',context)

def shop(request):
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {'category':categorys,'products':products}

    return render(request,'shop.html',context)

def shop_detail(request,slug):
    products = get_object_or_404(Product, slug=slug)
    categorys = Category.objects.all()
    context = {'category':categorys,'product':products}

    return render(request,'shop-detail.html',context)

def cart(request):
    carts = request.session.get('cart')
    cart_items = []
    total_price = 0
    total_quantity = 0
    if carts:
        for product_id,cart_item in carts.items():
            prod = Product.objects.get(id=product_id)
            quantity = cart_item['quantity']
            item_price = prod.price * quantity
            print(item_price,"itemmmmmmmmmmmmmmmmmmmmmmm")
            total_price = item_price + total_price
            total_quantity = quantity + total_quantity
            cart_items.append({'prod':prod,'quantity':quantity,"item_price":item_price})
            context = {'cart_items':cart_items,'total_price':total_price}
            
        
        return render(request, 'cart.html', context)

    else:
        messages.error(request, 'Cart is empty :-')
        return render(request, 'cart.html')
# create a view for remove cart
def remove_cart(request,product_id):
     cart = request.session.get('cart', {})
     if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        
     return redirect('cart')

    

def add_cart(request,product_id):
    product = get_object_or_404( Product,id=product_id)
    print(product,'productttttttttttttttttttttt')
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'title': product.title,
            'price': product.price,
            'product_id':product.id,
            'quantity': 1
        }   

    request.session['cart'] = cart
    print(request.session['cart'],'fdgs')
    
    return redirect('cart')


def chackout(request):
    carts = request.session.get('cart')
    cart_items = []
    total_price = 0
    total_quantity = 0
    if carts:
        for product_id,cart_item in carts.items():
            prod = Product.objects.get(id=product_id)
            quantity = cart_item['quantity']
            item_price = prod.price * quantity
            print(item_price,"itemmmmmmmmmmmmmmmmmmmmmmm")
            total_price = item_price + total_price
            total_quantity = quantity + total_quantity
            cart_items.append({'prod':prod,'quantity':quantity,"item_price":item_price})
            context = {'cart_items':cart_items,'total_price':total_price,'total_quantity':total_quantity}
            
        
        return render(request, 'chackout.html', context)

    else:
        messages.error(request, 'Cart is empty :-')

    return render(request,'chackout.html',context)

def testimonial(request):

    return render(request,'testimonial.html')

def E404(request):

    return render(request,'404.html')
@csrf_exempt
def contact(request):
    if request.method == "POST":
        name = request.POST.get('names')
        email = request.POST.get('emails')
        message = request.POST.get('messages')
        print(name,email,message,'this ffffffffffffffffffffffffffffff')

        contects = Contect.objects.create(name=name,email=email,message=message)
        return redirect("home")

    return render(request,'contact.html')

@csrf_exempt
def signUp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        state = request.POST.get('state')
        print(state,'stateeeeeeeeeeeeee')
        city = request.POST.get('city')
        country = request.POST.get('country')
        image = request.FILES.get('image')

        user = User.objects.filter(username=username).exists()
        if user:
         messages.error(request, 'user name already exists')
         return redirect("signup")
        else:
         user = User.objects.create_user(username=username,email=email,password=password,state=state,city=city,country=country,image=image)

         return redirect("login")

    return render(request,'sign_up.html')

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        print('xxxxxxxxxxxxxx')
        username = request.POST.get('username')
        # print(email,'eeeeeeeeeeeee')
        password = request.POST.get('password')
        print(password,'ppppppppppp')
        user = authenticate(request,username=username,password=password)
        print(user,'userrrrrrrrrrrrrrrrr')
        if user:
            print('inside the ifffffffffffffffffff')
            login(request,user)
            return redirect("home")
        else:
            # print('absyfb jdasgfbssssssssssssss')
            messages.error(request, 'Invalid username or password.')
            return redirect("login")
            

    return render(request,'login.html')
@csrf_exempt
def sign_out(request):
    logout(request)
    return redirect("home")
@csrf_exempt
def profile_page(request):
    user = request.user
    print(user,'userrrrrrrrrrrrrrrrrrrrrrrrrr')
    context = {'profile':user}
    return render(request,'profile.html',context)
@csrf_exempt
def edit_page(request):
    user = request.user
    context = {'edit':user}
    if request.method =="POST":
        username = request.POST.get('username')
        print(username,'this userrrrrrrrrrrrrrrrrrrrrr')
        email = request.POST.get('email')
        state = request.POST.get('state')
        city = request.POST.get('city')
        country = request.POST.get('country')
        image = request.FILES.get('image')
# ye line waps save krvane ke liye
        user.username = username
        user.email = email
        user.state = state
        user. city = city
        user. country = country
        user. image = image
        user.save()

        return   redirect("profile")
    return render(request,'edit.html',context)


