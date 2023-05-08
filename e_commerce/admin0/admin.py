from django.contrib import admin
from .models import AddressDetails, Coupon, Customer, Product
# Register your models here.
admin.site.register(Customer)
admin.site.register(Coupon)
admin.site.register(Product)
admin.site.register(AddressDetails)