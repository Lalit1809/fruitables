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
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
    print("Total unique products in session cart:", product_count)
    product = Product.objects.all()
    context = {'products':product,'product_count':product_count}

    return render(request,'index.html',context)

def shop(request):
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {'category':categorys,'products':products,'product_count':product_count}

    return render(request,'shop.html',context)

def shop_detail(request,slug):
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
    products = get_object_or_404(Product, slug=slug)
    categorys = Category.objects.all()
    context = {'category':categorys,'product':products,'product_count':product_count}

    return render(request,'shop-detail.html',context)

def cart(request):
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
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
            context = {'cart_items':cart_items,'total_price':total_price, 'total_quantity': total_quantity,'product_count':product_count}
            
        
        return render(request, 'cart.html', context)

    else:
        messages.error(request, 'Cart is empty :-')
        return render(request, 'cart.html')
    

# create a viewss for update_card quentity and price
@csrf_exempt
def update_cart(request):
    if request.method == "POST":
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        print(action,'this is action which is comming from ajax')
        print(product_id,'this is product id which is commimg from ajax')
        product = Product.objects.get(id=product_id)
        print(product,'this is product')
        cart = request.session.get('cart', {})
        print(cart,'this is cart')

        if str(product_id) in cart:
            quantity = cart[str(product_id)]['quantity']

            if action == "increase":
             quantity += 1
            if action == "decrease":
             quantity = max(1, quantity - 1)

            cart[str(product_id)]['quantity'] = quantity
            request.session['cart'] = cart
            # return redirect('cart')
            item_price = product.price * quantity
            total_price = sum(Product.objects.get(id=int(pid)).price * data['quantity'] for pid, data in cart.items())

        
        
    # return render(request,'cart.html')
    return JsonResponse({'success':True,'item_price': item_price,'total_price': total_price,'quantity': quantity})   
 


# create a view for remove cart
def remove_cart(request,product_id):
     cart = request.session.get('cart', {})
     print(product_id,':-this is cart id')
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

@csrf_exempt
def chackout(request):
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
    cart_items = []
    total_price = 0
    total_quantity = 0

    if carts:
        for product_id, cart_item in carts.items():
         prod = Product.objects.get(id=product_id)
         quantity = cart_item['quantity']
         item_price = prod.price * quantity
         total_price += item_price
         total_quantity += quantity
         cart_items.append({'prod': prod, 'quantity': quantity, "item_price": item_price})

        context = {'cart_items': cart_items, 'total_price': total_price, 'total_quantity': total_quantity,'product_count':product_count}

        if request.method == "POST":
            firstname = request.POST.get('firstname')
            print(firstname,'this is first name')
            lastname = request.POST.get('lastname')
            companyname = request.POST.get('companyname')
            address = request.POST.get('address')
            city = request.POST.get('city')
            country = request.POST.get('country')
            pincode = request.POST.get('pincode')
            phonenumber = request.POST.get('phonenumber')
            email = request.POST.get('email')
            message = request.POST.get('message')

            # for item in cart_items:
            #     order = Order.objects.create(user=request.user,quentity=item['quantity'],total_amount=item['item_price'],)
            #     order.product.add(item['prod'])

                    # Create single order with total quantity
            order = Order.objects.create(
                user=request.user,
                quentity=total_quantity,
                total_amount=total_price,
            )

                # Add all products to the M2M field
            order.product.set([item['prod'] for item in cart_items])
            billing_details=Billing_details.objects.create( 
                order=order, 
                firstname=firstname, 
                lastname=lastname, 
                companyname=companyname, 
                address=address,
                city=city,
                country=country,
                pincode=pincode,
                phonenumber=phonenumber,
                email=email,
                message=message)

            
            messages.success(request, "Order placed successfully.")
            return redirect('payment')

        return render(request, 'chackout.html', context)

    else:
            messages.error(request, 'Cart is empty :-')
            return redirect('cart')


def payment (request):
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
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
            context = {'cart_items':cart_items,'total_price':total_price, 'total_quantity': total_quantity,'product_count':product_count}
            
        
        return render(request, 'payment.html', context)

    else:
        messages.error(request, 'Cart is empty :-')

    return render(request,"payment.html")



def testimonial(request):
    carts = request.session.get('cart', {}) 
    product_count=len(carts)
    context={'product_count':product_count}

    return render(request,'testimonial.html',context)

def E404(request):

    return render(request,'404.html')
@csrf_exempt
def contact(request):
    carts = request.session.get('cart', {}) 
    product_count=len(carts)
    context = {'product_count':product_count}
    if request.method == "POST":
        name = request.POST.get('names')
        email = request.POST.get('emails')
        message = request.POST.get('messages')
        print(name,email,message,'this ffffffffffffffffffffffffffffff')

        contects = Contect.objects.create(name=name,email=email,message=message)
        return redirect("home")

    return render(request,'contact.html',context)

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
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
    user = request.user
    print(user,'userrrrrrrrrrrrrrrrrrrrrrrrrr')
    context = {'profile':user,'product_count':product_count}
    return render(request,'profile.html',context)


@csrf_exempt
def edit_page(request):
    carts = request.session.get('cart', {}) 
    product_count = len(carts)
    user = request.user
    context = {'edit':user,'product_count':product_count}
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


@csrf_exempt
def password_change(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print('This is the email form input :-', email)

        try:
            user = User.objects.get(email=email)
            subject = "Password Reset Link"
            message = f"Hi {user.username},\nClick the link below to reset your password:\nhttp://127.0.0.1:8000/new-confrim-password/?email={email}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
            return redirect('home')  # Home page name

        except User.DoesNotExist:
            return HttpResponse("User with this email doesn't exist.")

    return render(request, 'password-change-login.html')


@csrf_exempt
def new_confrim_change(request):
    email = request.GET.get('email')
    if not email:
        return HttpResponse("Invalid or expired link.")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("User not found.")

    if request.method == "POST":
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confrim-password')

        if new_password != confirm_password:
            return HttpResponse("Passwords do not match.")

        # ✅ Check if new password is same as current
        if check_password(new_password, user.password):
            return HttpResponse("New password cannot be the same as the old password.")

        # ✅ All good, update password
        user.set_password(new_password)
        user.save()
        return redirect('home')

    return render(request, 'new-confrim-password.html')




