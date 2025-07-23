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
    path('edit/',views.edit_page,name='edit')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)