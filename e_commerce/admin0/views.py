from django.shortcuts import render,redirect
from django.contrib import auth

from user0.models import *
from .models import *
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .form import CategoryForm
from .models import Category, Product

# Create your views here.
from django.shortcuts import render



from datetime import datetime,timedelta
from django.db.models.functions import TruncDay,Cast
from django.db.models import DateField,Sum,Q,FloatField


def adminlogin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password'] 
        u = auth.authenticate(username=username,password=password)
        if u is not None :
            if u.is_superuser:
                return redirect(dashboard)
            else:
                pass
        else:
            redirect(adminlogin)

    return render(request,'adlogin.html')

def dashboard(request):

    return render(request, 'dashboard.html')
def blockuser(request, id):
    # user = get_object_or_404(User, id=id)
    user=Customer.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, "user has been blocked.")
    else:
        user.is_active = True
        messages.success(request, "user has been unblocked.")
    user.save()
    return redirect(users)


def users(request):
    user = Customer.objects.all().order_by('id')[1:]
    return render(request, 'users.html',locals())


def products(request):
    prodect=Product.objects.all()
    return render(request, 'products.html',locals())


def orders(request):

    return render(request, 'orders.html')


def coupons(request):

    return render(request, 'coupouns.html')

def addproduct(request):
    category = Category.objects.all()
    

    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        
        cat = request.POST['category']
        
        desc = request.POST['desc']
        image_1 = request.FILES['image1']
        

        # slug = slugify(name)

        catobj = Category.objects.get(id=cat)
        Product.objects.create( product_name=name, price=price,  category=catobj, description=desc, images1=image_1)
        # messages.success(request, "Product added")
        return redirect(addproduct)
        
   
    
    return render(request,'addproduct.html',locals())

def addcategory(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        cat_image = request.FILES.get('cat_image')

        # slug = slugify(name)

        category = Category(category_name=name, description=description, cat_image= cat_image)
        category.save()

        msg = "Category added"
        # return redirect('adminapp:viewcategory')

    return render(request, 'addcatogery.html', locals())

def updateproduct(request,product_id):
    product = Product.objects.get(id=product_id)
   
   
    if request.method == 'POST':
    
        price = request.POST['price']
       
        
        try:
            image_1 = request.FILES['image1']
            

            image = Product.objects.get(id=product_id)
            image.images1 = image_1
            
            image.save()


        except :
            pass


        Product.objects.filter(id=product_id).update(price=price)
        
        return redirect(products)




    return render(request,'updateprodect.html',locals())

def deleteprodect(request,product_id):

    dele=Product.objects.get(id=product_id)
    dele.delete()


    return redirect(products)

def category(request):

    context=Category.objects.all()
    return render(request, 'category.html',{'cat':context})

def deletecategory(request,category_id):

    dele=Category.objects.get(id=category_id)
    dele.delete()


    return redirect(category)

def updatecategory(request, category_id):
    # Retrieve the category object using its slug
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        # Create a form instance with the submitted data and files,
        # and bind it to the category instance
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category edited successfully.')
            return redirect('category')
        else:
            # If the form is invalid, display error messages
            messages.error(request, 'Invalid input')

    # Create a new form instance with the category object
    form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'updatecategory.html', context)

def CatSearch(request):
    print(request.GET)
    cat = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cat = Category.objects.filter(category_name__icontains=keyword)
            
            if not cat:
                message = "No products found for the keyword entered."
                context = {
                    'message': message
                }
                return render(request, 'category.html', context)
                
    context = {}
    if cat is not None:
        context['cat'] = cat
        
    return render(request, 'category.html', context)

def order_list(request):
    orders = OrderItem.objects.all()
    return render(request, 'admin_order.html', {'orders': orders})


def change_order_status(request, order_id):
    order = get_object_or_404(OrderItem, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        order.order_status = new_status
        order.save()
        return redirect('order_list')
    return render(request, 'change_order_status.html', {'order': order})

def dashboard(request):
    
    sales = OrderItem.objects.all().count()
    users = Customer.objects.all().count()
    recent_sales = Order.objects.order_by('-id')[:5]
     # Graph setting
    # Getting the current date
    today = datetime.today()
    date_range = 8

    # Get the date 7 days ago
    four_days_ago = today - timedelta(days=date_range)

    #filter orders based on the date range
    payments = Payment.objects.filter(paid_date__gte=four_days_ago, paid_date__lte=today)


    # Getting the sales amount per day
    sales_by_day = payments.annotate(day=TruncDay('paid_date')).values('day').annotate(total_sales=Sum('cart_total')).order_by('day')
    context={
          'sales':sales,
          'users':users,
          "recent_sales":recent_sales,
          'sales_by_day': sales_by_day,

     }

    return render(request, 'dashboard.html',context)


def admin_sales(request):
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(admin_sales)

        order_items = OrderItem.objects.filter(order__ordered_date__gte=start_date, order__ordered_date__lte=end_date).order_by('-id')


        if order_items:
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')

    return render(request,'admin_sales.html',context)