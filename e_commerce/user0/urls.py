
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('',views.index,name='index'),         
   path('login/',views.login,name='login'),
   path('register/',views.register,name='register'),
   path('logout/',views.logout,name='logout'),
   path('product/',views.product,name='product'),
   path('profile/',views.profile   ,name='profile'),
   path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
   path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
   path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
   path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
   path('accounts/login/',views.login,name='login'),
   path('shopdetails/<int:id>/',views.shopdetails ,name='shopdetails'),
   path('search/',views.search,name='search'),
 
   # path('increment_cart/<int:id>/', views.increment_cart, name='increment_cart'),
   path('add_address/', views.add_address, name='add_address'),
   path('manageaddress/',views.manageaddress,name='manageaddress'),
   path('deleteaddress/<int:id>/',views.deleteaddress,name='deleteaddress'),
   path('edit_address/<int:id>/', views.edit_address, name='editaddress'),
   path('wishlist/',views.wishlist,name='wishlist'),
   path('add_wishlist/<int:product_id>/', views.add_wishlist, name='add_wishlist'),    
   path('remove_wishlistitem/<int:product_id>/<int:wishlist_id>/', views.remove_wishlistitem, name='remove_wishlistitem'),

   path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
   path('showcart/',views.show_cart,name='show_cart'),
   path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
   path('remove_cartitem/<int:product>/', views.remove_cartitem, name='remove_cartitem'),

   path('checkout/', views.checkout, name='checkout'),
   path('checkout/success/', views.success, name='success'),
   path('orders-list/', views.orders_list, name="orders_list"),
   path('order-details/<str:order_id>/', views.order_details, name="order_details"),
   path('order-tracking/<int:item_id>/', views.order_tracking, name="tracking"),
   path('order-invoice/<str:order_id>/', views.order_invoice, name="order_invoice"),
   path('cancel-order/<int:item_id>/<str:order_id>', views.cancel_order, name="cancel_order"),
   path('orderslist/', views.orders_list, name="orders_list"),
   path('coupons/', views.coupon_list, name='coupon_list'),
   path('coupons/add/', views.add_coupon, name='add_coupon'),
   path('coupons/edit/<int:pk>/',views.edit_coupon, name='edit_coupon'),
   path('remove-coupon/', views.remove_coupon, name="remove_coupon"),
   path('coupons/delete/<int:pk>/', views.delete_coupon, name='delete_coupon'),
   path('order-items/<int:id>/', views.order_items, name='ordered_items'),
   path('order-details/<str:order_id>/', views.order_details, name="order_details"),
   path('invoice/', views.invoice, name="invoice"),

]
