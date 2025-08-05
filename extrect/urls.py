from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('shop/',views.shop,name = 'shop'),
    path('shop-detail/<str:slug>/',views.shop_detail,name ='shop-detail'),
    path('cart/',views.cart,name ='cart'),
    path('chackout/',views.chackout,name ='chackout'),
    path('testimonial/',views.testimonial,name ='testimonial'),
    path('404/',views.E404,name ='E404'),
    path('contact/',views.contact,name ='contact'),
    path('signup/',views.signUp,name='signup'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.sign_out,name='sign_out'),
    path('profile/',views.profile_page,name='profile'),
    path('edit/',views.edit_page,name='edit'),
    path('add_cart/<int:product_id>',views.add_cart , name='add_cart'),
    path('remove_cart/<int:product_id>',views.remove_cart, name='remove_cart'),
    path('send-email/',views.send_mail_page,name='send-email'),
    path('forgot-password/',views.password_forgot,name='forgot-password'),
    path('otp/',views.enter_otp,name='otp'),
    path('change-password/',views.change_password,name='c-password'),
    path('update_cart/', views.update_cart,name="update-cart"),
    path('payment/<int:order_id>',views.payment,name='payment'),
    path('password-change/',views.password_change,name='p-change'),
    path('new-confrim-password/',views.new_confrim_change,name="new-confrim-password"),
    path('payment-status/<int:order_id>',views.payment_status,name='payment-status'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)