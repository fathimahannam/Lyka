from django.contrib import admin
from.models import *
# Register your models here.
admin.site.register(products1)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Wishlist)

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)