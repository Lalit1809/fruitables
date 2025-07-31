from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
import random
from .models import *
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.core.mail import send_mail
from django.conf import settings
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
    
    return redirect('home')


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


def send_mail_page(request):
     context = {}

     if request.method == 'POST':
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if address and subject and message:
            # try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                context['result'] = 'Email sent successfully'
            # except Exception as e:
            #     context['result'] = f'Error sending email: {e}'
                return redirect("home")
        else:
            context['result'] = 'All fields are required'

            return redirect("home")
    
     
     return render(request, 'send-email.html',context)


@csrf_exempt
def password_forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email
        print(request.session['email'], 'this session email')
        user = User.objects.get(email=email)
        print(user,'this is user')

        if user:
            otp = random.randint(1000, 9999)
            print(otp,':-This is genrated otp')
            user.email_otp = otp
            user.save()

            send_mail(
            'Email Verification OTP',
            f'Your OTP for email verification is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            )
            return redirect("otp")

        else:
            messages.error(request, 'Invalid User Email.')
            return redirect("forgot-password")

    return render(request,'forgot-password.html')

@csrf_exempt
def enter_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('opt')
        print(otp,':-This is otp')
        user = User.objects.filter(email_otp=otp).first()
        print(user,'this is user')
        if user:
            return redirect('c-password')
        else:
            messages.error(request,'Invalid Otp')
            return redirect('otp')
    
    return render(request,'otp.html')

@csrf_exempt
def change_password(request):
    email = request.session.get('email')
    print(email,':-this is email which is stored in sessions')
    user = User.objects.get(email=email)
    print(user,':-This is user')
    if request.method == 'POST':
        new_password = request.POST.get('new-password')
        confrim_password = request.POST.get('confrim-password')
        print(new_password,'This is our new password')
        print(confrim_password,'This is our confrim password')
        if new_password != confrim_password :
            messages.error(request,'Confrim password not match')
            return redirect('c-password')
        
        else:

            if check_password(new_password, user.password):
                messages.error(request,'New password cannot be same as old password')
                return redirect('c-password')
            
        user.password = make_password(new_password)
        user.save() 
        return redirect('login')
         


    return render(request,'change-password.html')



