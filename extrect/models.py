from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField

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

    def __str__(self):
     return self.username
    
class Product(models.Model):
   category = models.ForeignKey(Category,on_delete=models.CASCADE)
   author = models.ForeignKey(User,on_delete=models.CASCADE)
   image = models.ImageField(null=True,blank=True)
   title = models.CharField(max_length=50)
   detail = models.TextField()
   price = models.CharField(max_length=60)
   quantity = models.PositiveIntegerField(default=1)
   slug = AutoSlugField(populate_from = 'title')
   
   def __str__ (self):
     return self.title
   


   


   
       