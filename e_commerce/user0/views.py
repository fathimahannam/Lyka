from django.shortcuts import get_object_or_404, render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib import auth,messages
from django.contrib.auth.models import User
# from admin_side.views import *
# from user_side.views import *
from admin0.form import *
from django.db.models import Q 
from .models import *
from .form import *
from django.core.mail import send_mail,EmailMessage
import random
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from django.utils import timezone




def index(request):

    context=Product.objects.all()

    return render(request, 'index.html',{'use':context})



def product(request):

    context=Product.objects.all()
   
    
    return render(request, 'product.html',{'pro':context})



def login(request):
    if request.method=='POST':
        username=request.POST['user_name']
        password=request.POST['pass_word']
        user =auth.authenticate(username=username,password=password) 
        print(user)
        if user is not None: 
            auth.login(request,user)         
            return redirect(index)
        else:
            messages.warning(request,f'wrong username or password ')
            
            return redirect(login)
    return render(request,'login.html')

def register(request):
    usr = None
    #Register Form
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        # OTP Verification
        if get_otp:
            get_usr=request.POST.get('usr')
            usr=Customer.objects.get(username=get_usr)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                messages.success(request,f'Account is created for {usr.username}')
                return redirect(login)
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'register.html',{'otp':True,'usr':usr})
        form = CreateUserForm(request.POST)
        #Form Validation
        if form.is_valid():
            form.save()
            email=form.cleaned_data.get('email')
            username=form.cleaned_data.get('username')
            usr=Customer.objects.get(username=username)
            usr.email=email
            usr.username=username
            usr.is_active=False
            usr.save()
            usr_otp=random.randint(100000,999999)
            UserOTP.objects.create(user=usr,otp=usr_otp)
            mess=f'Hello\t{usr.username},\nYour OTP to verify your account for Trendsetter is {usr_otp}\nThanks!'
            send_mail(
                    "welcome to Trendsetter -Verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently=False
                )
            messages.info(request,f'OTP send to your email')

            return render(request,'register.html',{'otp':True,'usr':usr})
            
        else:
            errors = form.errors
            for field, errors in errors.items():
              for error in errors:
                messages.error(request, f" {error}")
                       
    #Resend OTP
    elif (request.method == "GET" and 'username' in request.GET):
        get_usr = request.GET['username']
        if (Customer.objects.filter(username = get_usr).exists() and not Customer.objects.get(username = get_usr).is_active):
            usr = Customer.objects.get(username=get_usr)
            id = usr.id
            
            otp_usr = UserOTP.objects.get(user_id=id)
            usr_otp=otp_usr.otp
            mess = f"Hello, {usr.username},\nYour OTP is {usr_otp}\nThanks!"
            
            send_mail(
        "Welcome to Trendsetter - Verify Your Email",
        mess,
        settings.EMAIL_HOST_USER,
        [usr.email],
        messages.success(request, f'OTP resend to  {usr.email}'),

        # fail_silently = False
         )
        return render(request,'register.html',{'otp':True,'usr':usr})
    else:
            errors = ''
    form=CreateUserForm()
    context = {'form': form, 'errors': errors}

    return render (request, 'register.html', context)

def logout(request):
    auth.logout(request)
    # if 'username' in request.session:
    #     request.session.flush()
    return redirect(index)


def profile(request):
    return render(request,'profile.html')

def password_reset(request):

    return render(request, 'password_reset.html')

def shop(request):


    prod=Product.objects.all()

    return render(request,'product.html',{'pos':prod})


def shopdetails(request,id):

      product=Product.objects.get(id=id)
      prod=Product.objects.all()
    #   multipleimg = MultiProduct.objects.filter(product=product)

      context={
    'pro':product,
    'con':prod,
    
     }

      return render(request, 'shopdetails.html',context )
 

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            products = Product.objects.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()

    context = {
        'pro': products,
        'products_count': products_count,
    }

    return render(request, 'product.html', context)


# def add_to_cart(request, product_id):
#     user = request.user
#     product = Product.objects.get(id=product_id)
    
#     # Check if the product is already in the cart
#     cart_item = Cart.objects.filter(user=user, product=product).first()
#     if cart_item:
#         # Product is already in the cart, so just increase its quantity
#         cart_item.quantity += 1
#         cart_item.save()
#     else:
#         # Product is not in the cart, so add a new item
#         Cart(user=user, product=product, quantity=1).save()
    
#     return redirect(show_cart)


# def show_cart(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user)
#     total = 0
#     for item in cart:
#         total += item.quantity * item.product.price
#         print(total)

#     context = {'cart': cart, 'total': total}
#     return render(request, 'cart.html', context)

    # ...
# def addcartitem(request, product_id):
#     if request.user.is_authenticated:
#         current_user = request.user
#         product = get_object_or_404(Product, id=product_id)
#         cart_item = Cart.objects.filter(user=current_user, product=product).first()
#         if cart_item:
#             cart_item.quantity += 1
#             cart_item.save()
#     return redirect('cart')




# def removecartitem(request,product_id):
#     current_user = request.user
#     product = get_object_or_404(Product, id=product_id)

#     cart_items = Cart.objects.filter(user_id=current_user.id, product=product)
#     print(cart_items)
#     for cart_item in cart_items:
#         if cart_item.quantity == 1:
#             cart_item.delete()  # remove the item from the cart if the quantity is 1
#         else:
#             cart_item.quantity -= 1
#             cart_item.save()  # decrement the quantity by 1
#     return redirect('cart')




def deleteprodect(request,product_id):

    dele=Product.objects.get(id=product_id)
    dele.delete()


    return redirect(product)



def edit_address(request,id):
    address = get_object_or_404(AddressDetails, id=id, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('manageaddress')
    else:
        form = AddressForm(instance=address)

    return render(request, 'edit_address.html', {'form': form})


def manageaddress(request):
    user=request.user
    add=AddressDetails.objects.filter(user_id=user.id)
    
    return render(request,'manageaddress.html',locals())

def deleteaddress(request,id):
    dele=AddressDetails.objects.get(id=id)
    dele.delete()
    return redirect(manageaddress)
   
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('manageaddress')
    else:
        form = AddressForm()
    return render(request, 'add_address.html', {'form': form}) 


def wishlist(request):
    return render(request,'wishlist.html')








###########################cart$##########################

def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        user = request.user

        cart, _ = Cart.objects.get_or_create(user=user, is_active=True)
        is_cart_item = CartItem.objects.filter(cart=cart, product=product).exists()

        if is_cart_item:
            cart_item = CartItem.objects.get(cart=cart, product=product)

            if cart_item.quantity == product.stock:
                messages.error(request, f'Only {cart_item.quantity} product in stock')
                return redirect('cart')

            cart_item.quantity += 1
            cart_item.save()

        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            cart_item.save()

    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
        return redirect('cart')

    return redirect('show_cart')

def show_cart(request):
    cart=None
    cart_items=None
    
    try:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart_items = CartItem.objects.filter(cart=cart).order_by('id')
        coupons = Coupon.objects.filter(is_expired=False)
        print(coupons)
    except Exception as e:
        print(e)

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(name__icontains=coupon)



        if not coupon_obj.exists():
            messages.error(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart.coupon:
            messages.warning(request, 'Coupon Already applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart.get_cart_total() < coupon_obj[0].min_amount:
            messages.warning(
                request, f'Total amount should be greater than ₹{coupon_obj[0].min_amount} excluding tax')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, 'This coupon has expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       
        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request, 'Coupon Applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'cart_items': cart_items,
               'cart': cart,
               'coupons' : coupons,
               

               }
    return render(request, 'cart.html', context)


def remove_from_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        user = request.user

        cart = Cart.objects.get(user=user, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, product=product)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()

        messages.success(request, "Product removed from cart successfully")

    except (Product.DoesNotExist, Cart.DoesNotExist, CartItem.DoesNotExist):
        messages.error(request, "An error occurred while removing the product from cart")

    return redirect('show_cart')


def remove_cartitem(request, product):
    try:
        product = Product.objects.get(id=product)
        cartt = Cart.objects.get(user=request.user, is_active=True)
        cart_item = CartItem.objects.get(cart=cartt, product=product)

        cart_item.delete()
        messages.success(request, "Product deleted from cart successfully")

    except:
        pass

    return redirect(show_cart)



######################wishlist#######################
def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def remove_wishlistitem(request,product_id,wishlist_id):
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        wishlist_item = WishlistItem.objects.get(product=product,user=request.user,id=wishlist_id)
    else:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)
    wishlist_item.delete()
    messages.success(request, f"{product.product_name} has been removed from the wishlist")
    return redirect('wishlist')

def wishlist(request,wishlist_items=None):
    try:
        if request.user.is_authenticated:#fro login users
           wishlist_items = WishlistItem.objects.filter(user=request.user,is_active=True)
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
            
    except ObjectDoesNotExist:
        pass

    context = {        
        'wishlist_items':wishlist_items,
    }
    
    return render(request, 'wishlist.html',context)


def add_wishlist(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
    
        is_wish_item_exists = WishlistItem.objects.filter(product=product, user=current_user).exists()
        if is_wish_item_exists:
            wishlist_item = WishlistItem.objects.get(product=product,user=current_user)
        else:
            wishlist_item = WishlistItem.objects.create( #if not exist it will create one cart
            product=product,
            user = current_user,
        )
        wishlist_item.save()
    else:

        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        except Wishlist.DoesNotExist: 
            wishlist = Wishlist.objects.create( 
                wishlist_id=_wishlist_id(request)
            )
        wishlist.save()  

        try:
            wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)
            wishlist_item.save()
        except WishlistItem.DoesNotExist:
            wishlist_item = WishlistItem.objects.create(
                product=product,
                wishlist=wishlist
            )
        wishlist_item.save()
    messages.success(request, f"{product.product_name} has been added to wishlist")
    return redirect('wishlist')





def checkout(request):
    # get the current user
    current_user = request.user
    
    # get the user's saved addresses
    addresses = AddressDetails.objects.filter(user=current_user).order_by('id')
    
    # get the user's active cart
    try:
        cart = Cart.objects.get(user=current_user, is_active=True)
    except Cart.DoesNotExist:
        # redirect the user to their cart if they don't have an active cart
        return redirect('show_cart')
    
    # get the cart items and check if any have an invalid quantity
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        if item.quantity > (item.product.stock or 0):
            item.quantity = item.product.stock or 0
            item.save()
            messages.warning(request, f'{item} has only {item.product.stock} quantity left')
            return redirect('show_cart')

    # create a Razorpay order for the cart total amount
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    amount = int(cart.get_cart_total() * 100) # convert to paise
    currency = 'INR'
    payment = client.order.create({'amount': amount, 'currency': currency, 'payment_capture': 1})
    print(payment)
    # save the Razorpay order ID to the cart
    cart.razorpay_order_id = payment['id']
    cart.save()
    
    # define the context data to pass to the template
    
    
    # render the checkout page template with the context data
  
    return render(request, 'checkout.html', locals())


def success(request):
    try:
        razorpay_order_id = request.GET.get('razorpay_order_id')
        cart = Cart.objects.get(user=request.user, is_active=True)
        # Payment details storing
        user = request.user
        transaction_id = request.GET.get('razorpay_payment_id')
        cart_total = cart.get_cart_total()
        # tax = cart.get_tax()
        
        
        print('gettingf g totalla')

        payment = Payment.objects.create(user=user, transaction_id=transaction_id, cart_total=cart_total)
        payment.save()
        
        print('before adderess')
        address_id = request.GET.get('address')
        print('address  : ' , address_id)
        delivery_address = AddressDetails.objects.get(user=user, id=address_id)
        
        # Creating the order in Order table
        order = Order.objects.create(order_id=razorpay_order_id, user=user, delivery_address=delivery_address, payment=payment)

        if cart.coupon:
            order.coupon = cart.coupon
            order.save()

        # Storing ordered products in OrderItem table
        order_items = CartItem.objects.filter(cart=cart)
        for item in order_items:
            item.product.stock -= item.quantity
        
            item.product.save()
        
            ordered_item = OrderItem.objects.create(user=user,order=order, product=item.product, item_price=item.get_product_price(), quantity=item.quantity, item_total=cart.get_cart_total())
        

            ordered_item.save()
            
       

        # Deleting the cart once it is ordered/paid
        cart.is_active = False
        cart.delete()

        return render(request, 'success.html', {'order_id': razorpay_order_id})
    except:
        return redirect('orders_list')


def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    # order_items = OrderItem.objects.filter(order=orders)
    return render(request, 'orderlist.html', {'orders' : orders})


def order_details(request,order_id):
    try:
        order = Order.objects.get(uid=order_id)
        order_items = OrderItem.objects.filter(order=order)
        print(order_items)
    except:
        order_items = None
        
    return render(request, 'orders/order_details.html', {'order_items' : order_items})


def order_tracking(request, item_id):
    current_date = timezone.now()
    item = OrderItem.objects.get(id=item_id)

    context = {
        'item' : item,
        'current_date' : current_date
    }
    return render(request, 'orders/order_tracking.html' ,context)



def order_invoice(request, order_id):

    order = Order.objects.get(uid=order_id,user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order' : order,
        'order_items' : order_items
    }
    return render(request, 'orders/invoice.html',context)


def cancel_order(request, item_id=None, order_id=None):
        
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        order = Order.objects.get(order_id=order_id,user=request.user)
        payment_id = order.payment.transaction_id
        item = OrderItem.objects.get(order=order, id=item_id)
        item_amount = int(item.item_total) * 100
        
        refund = client.payment.refund(payment_id,{'amount':item_amount})

        if refund is not None:
            item.order_status = 'Refunded'
            item.product.stock += item.quantity
            item.product.save()

            current_user = request.user
            subject = "Refund succesfull!"
            mess = f'Greetings {current_user.first_name}.\nYour refund for the product {item} of order: {order.order_id} has been succesfully generated. \nThank you for shopping with us!'
            send_mail(
                        subject,
                        mess,
                        settings.EMAIL_HOST_USER,
                        [current_user.email],
                        fail_silently = False
                     )

            item.save()
            return render(request, 'orders/refund_success.html',{'order_id':order_id})

        else:
            return HttpResponse('Payment not captured')
        
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    # order_items = OrderItem.objects.filter(order=orders)
    return render(request, 'orders-list.html', {'orders' : orders})

########################3coupon#################
def coupon_list(request):
    coupons = Coupon.objects.all()
    context = {'coupons': coupons}
    return render(request, 'coupon_list.html', context)


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm()
    context = {'form': form}
    return render(request, 'coupon_form.html', context)


def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm(instance=coupon)
    context = {'form': form}
    return render(request, 'coupon_form.html', context)

def remove_coupon(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.coupon = None
        cart.save()
        messages.success(request, 'Coupon removed successfully')
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        return redirect('coupon_list')
    context = {'coupon': coupon}
    return render(request, 'coupon_confirm_delete.html', context)

def order_items(request,order_id):
    print(order_id,'---------its order id--------------------------')
    order = Order.objects.get(user=request.user, order_id=order_id)
    ordered_items = OrderItem.objects.filter(order=order).order_by('-id')
    
    

    context = {
        'order' : order,
        'ordered_items' : ordered_items
    }

    return render(request,'orderitems.html',context)



def order_details(request,order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        print(order_items)
    except:
        order_items = None
        
    return render(request, 'vieworder.html', {'order_items' : order_items,'order':order})


def invoice(request,order_id):
    order =Order.objects.filter(order_id=order_id,user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    orders = Order.objects.filter(user=request.user)

    context={
        'order': order,
        'orderitems':orderitems,
        'ord':orders
    }

    return render(request,'invoice.html',context)