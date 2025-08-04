from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.utils import timezone

STATUS_CHOICES=[
      ('Pending','Pending'),
      ('Paid','Paid'),
      ('UnPaid','UnPaid'),
      ('Shipped','Shipped'),
      ('Cancelled','Cancelled')
   ]

class Contect(models.Model):
   name = models.CharField(max_length=40)
   email = models.EmailField(unique=True)
   message = models.TextField()

   def __str__(self):
      return self.name

class Category( models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')
    
    def __str__ (self):
        return self.name

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    state = models.CharField(null=True,blank=True)
    city = models.CharField(null=True,blank=True)
    country = models.CharField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    email_otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
     return self.username
    
class Product(models.Model):
   category = models.ForeignKey(Category,on_delete=models.CASCADE)
   author = models.ForeignKey(User,on_delete=models.CASCADE)
   image = models.ImageField(null=True,blank=True)
   title = models.CharField(max_length=50)
   detail = models.TextField()
   price = models.PositiveIntegerField()
   quantity = models.PositiveIntegerField(default=1)
   slug = AutoSlugField(populate_from = 'title')
   
   def __str__ (self):
     return self.title
   
class Order(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   product = models.ManyToManyField(Product,null=True,blank=True)
   quentity = models.PositiveIntegerField()
   created_date = models.DateTimeField(default=timezone.now)    
   status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Pending')
   update_at = models.DateTimeField(default=timezone.now)
   
   total_amount = models.IntegerField()
   
   def __str__(self):
      return self.user.username
      
class Billing_details(models.Model):
   order = models.OneToOneField(Order,on_delete=models.CASCADE)
   firstname = models.CharField(max_length=10)
   lastname = models.CharField(max_length=10)
   companyname = models.CharField(max_length=20,null=True,blank=True)
   address = models.CharField(max_length=50)
   city = models.CharField(max_length=20)
   country = models.CharField(max_length=20)
   pincode = models.CharField(max_length=10)
   phonenumber = models.CharField(max_length=10)
   email = models.EmailField()
   message = models.TextField(null=True,blank=True)

   def __str__ (self):
      return self.firstname
   


   


   
       