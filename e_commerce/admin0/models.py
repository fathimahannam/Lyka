
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission,Group

# Create your models here.
class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    phone = models.CharField(max_length=10, default=1234567890, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customers')
    groups = models.ManyToManyField(Group, related_name='customers')

class UserOTP(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description= models.TextField(max_length=255, blank=True) 
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
  
  

    def _str_(self):
        return self.category_name
    
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images1         = models.ImageField(upload_to ='photos/products')  
    is_available    = models.BooleanField(default=True) 
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock           = models.IntegerField(null=True)
   
        
    def _str_(self):
        return self.product_name
    
class Coupon(models.Model):
    name = models.CharField(max_length=15)
    min_amount = models.PositiveBigIntegerField(default=15000)
    discount_price = models.PositiveBigIntegerField(default=799)
    is_expired = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
 
    


class AddressDetails(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    order_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.order_address},{self.city}, {self.state}, {self.country}, PIN: {self.zip_code}"
    
    def __str__(self):
        return self.user.username
