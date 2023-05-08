from django.urls import path,include
from .import views


urlpatterns = [
   path('adminlogin',views.adminlogin,name="adminlogin"),
   path('dashboard/',views.dashboard,name='dashboard'),
   path('users/',views.users,name='users'),
   path('products/',views.products,name='products'),
   path('orders/',views.orders,name='orders'),
   path('coupons/',views.coupons,name='coupons'),
   path('addproducts/',views.addproduct,name='addproducts'),
   path('addcategory/',views.addcategory,name='addcategory'),
   path('updateproduct/<int:product_id>/',views.updateproduct,name='updateproduct'),
   path('deleteproduct/<int:product_id>/',views.deleteprodect,name='deleteproduct'),
   path('<int:id>/blockuser/', views.blockuser, name='blockuser'),
   path('category/',views.category,name='category'),
   path('deletecategory/<int:category_id>/',views.deletecategory,name='deletecategory'),
   path('updatecategory/<int:category_id>/',views.updatecategory,name='updatecategory'),
   path('CatSearch/',views.CatSearch,name='CatSearch'),
   path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
   path('order_list/', views.order_list, name='order_list'),
   path('admin_sales',views.admin_sales,name='admin_sales'),
]
