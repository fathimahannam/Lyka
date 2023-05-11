from django.db import models
from admin0.models import Customer
from admin0.models import Product
from admin0.models import Coupon,AddressDetails,AbstractUser


# Create your models here.

    

class products1(models.Model):
    prohead=models.CharField(max_length=100 ,null=True )
    proimg=models.ImageField(upload_to='uploads' , null=True)
    proprice=models.IntegerField(null=True)
    prodetails=models.CharField(max_length=100,null=True)

    def _str_(self):
        return self.prohead

class MultiProduct(models.Model):
    

    image=models.ImageField(upload_to='uploads')

class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    coupon = models.ForeignKey(Coupon ,on_delete=models.SET_NULL , null=True, blank= True)
    is_active = models.BooleanField(default=True)
    razorpay_order_id = models.CharField(max_length=100 ,null=False, blank=True,unique=True)
    razorpay_payment_id = models.CharField(max_length=100 ,null=True, blank=True,unique=True)
    
    def get_cart_total(self):
        cart_items = CartItem.objects.filter(cart=self.id)
        price = []
        for cart_item in cart_items:
            quantity = cart_item.quantity
            price.append(cart_item.product.price * quantity)

        if self.coupon:
            return sum(price) - self.coupon.discount_price
        
        

        return sum(price)
    
    


    

class CartItem(models.Model):
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField()
    
    def get_product_price(self):
        return self.product.price
    
    
    def _str_(self):
        return self.product.product_name



# Create your models here.

class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250,blank=True)

    def _str_(self):
        return self.wishlist_id
    
class WishlistItem(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)   

    def _str_(self):
        return str(self.product)
    

# Create your models here.

class Payment(models.Model):

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    transaction_id = models.CharField(max_length=100)

    cart_total = models.PositiveIntegerField()

   

  

    payment_method = models.CharField(max_length=30, default='RazorPay')

    is_paid = models.BooleanField(default=True)

    paid_date = models.DateTimeField(auto_now_add=True)



    def str(self) -> str:

        return self.transaction_id
    

class Order(models.Model):

    order_id = models.CharField(max_length=100, unique=True)

    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

   

    delivery_address = models.ForeignKey(AddressDetails, on_delete=models.SET_NULL, null=True)

    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

    ordered_date = models.DateTimeField(auto_now_add=True, editable=False)



    def str(self) -> str:

        return f'{self.id} of {self.user}'    
    



class OrderItem(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded')
    )
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    order_status = models.CharField(max_length=20, choices=STATUS, default='Ordered')
    item_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    item_total = models.PositiveIntegerField()

    def _str_(self):
        return self.product.product_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='user_order_page')
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(products1,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.name
    def sub_total(self):
        return self.product.price * self.quantity
