from pyexpat.errors import messages
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User        
from django.contrib.auth import authenticate       
from django.contrib.auth import login,logout
from myapp.models import Gifts,Cart,Address,Order
from django.db.models import Q     
import razorpay 
from django.core.mail import send_mail     


# Home page
def home(request):
    return render(request,'home.html')

# New User Registration
def register(request):
    context={}
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        uname=request.POST['uname']
        ue=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']

        if uname=='' or ue=='' or p=='' or cp=='':
            # print('Please fill all the fields')
            context['errormsg']='Please fill all the fields'
        elif len(p)<8:
            # print('Password must be atleast 8 character')
            context['errormsg']='Password must be atleast 8 character'
        elif p!=cp:
            # print('Password and Confirm password must be same')
            context['errormsg']='Password and Confirm password must be same'
        else:
            try:
                u=User.objects.create(username=ue,email=ue,first_name=uname)
                u.set_password(p)  # set_password : To convert password into encripted form
                u.save()
                context['success']='User Created Successfully'
            except Exception:
                context['errormsg']='User Already Exists'
        return render(request,'register.html',context)
    

# User Login
def user_login(request):
    context={}
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        e=request.POST['ue']
        p=request.POST['upass']
        u=authenticate(username=e,password=p) # For Authentication Purpose
        if u is not None:
            login(request,u)        # Login Method
            return redirect('/')
        else:
            context['errormsg']='Invalid Credential'
            return render(request,'login.html',context)


# User/Admin Logout
def user_logout(request):
    logout(request)
    return redirect('/')

# User Profile Page
# def myprofile(request):
#     context={}
#     a=User.objects.filter(id=request.user.id)    

#     context['data']=a
#     return render(request,'profile.html',context)
def myprofile(request):
    user = request.user  # Get the currently logged-in user
    try:
        address = Address.objects.get(uid=user)  # Fetch the address associated with the user
    except Address.DoesNotExist:
        address = None  # Handle if the user has no address

    context = {
        'user': user,
        'address': address,
    }
    return render(request, 'profile.html', context)

# Add Address/Phone
def addaddress(request):
    context={}
    if request.method == 'GET':
        return render(request, 'addaddress.html')
    else:       # Retrieve form data
        street_address = request.POST['street_address']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['postal_code']
        phone = request.POST.get('phone', '')

        if street_address=='' or city=='' or state=='' or postal_code=='' or phone=='':
            context['errormsg']='Please fill all the fields'
        else:
            if request.user.is_authenticated:
                Address.objects.create(
                    uid=request.user,  
                    street_address=street_address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    phone=phone
                )
                return redirect('/myprofile')
            else:
                # If user is not authenticated, redirect to login page
                return redirect('login')  # Adjust to your login URL name



# Gifts/Product Page
def gifts(request):
    context={}
    g=Gifts.objects.filter(is_active=True) # Filter and Display only those data which are active
    context['data']=g
    return render(request,'gifts.html',context)


# Sort by Price [high->low or low->high]: 
def sort(request,x):
    context={}
    if x=='1':
        p=Gifts.objects.order_by('-price').filter(is_active=True)   # high-->low
    else:
        p=Gifts.objects.order_by('price').filter(is_active=True)    # low-->high

    context['data']=p
    return render(request,'gifts.html',context)


# Search products
def search(request):
    s=request.GET['srch']
    #print(s)
    p=Gifts.objects.filter(name__icontains=s)
    #print(p)
    p1=Gifts.objects.filter(pdetails__icontains=s)

    allprod=p.union(p1)
    context={}
    if len(allprod)!=0:
        context['data']=allprod
    else:
        context['errmsg']='Product Not Found'
    return render(request,'gifts.html',context)


# Gift Detail Page
def giftdetail(request,pid):
    p=Gifts.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request, 'giftdetail.html', context)


# Add to Cart Functionaliy
def addtocart(request, pid):
    context={}
    if request.user.is_authenticated :  #check whether is login or not (if not then re-direct to login page)
        # print('User is logged in')
        u=User.objects.filter(id=request.user.id)       #used to get id of authenticated user id
        # print(u)
        p=Gifts.objects.filter(id=pid)
        
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==0:
            c=Cart.objects.create(pid=p[0],uid=u[0])         #import cart
            c.save()
            context['success']='Product Added Successfully...!'
        else:
            context['errormsg']='Product Already Exist in Cart..!'
  
        context['data']=p
        return render(request,'giftdetail.html',context)
    
    else:
        return redirect('/login')
    


# View Cart functionality 
def viewcart(request):
    context={}
    c=Cart.objects.filter(uid=request.user.id)  
    #from cart table we have to fetched data of requested-authenticated user
    address = Address.objects.get(uid=request.user.id) 

    amt=0
    for i in c:
        amt = amt + i.pid.price * i.qty
    
    # context['totalamt']=amt
    # context['data']=c
    # context['data1']=a
    context={
        'data': c,
        'address': address,
        'totalamt': amt
    }
    return render(request, 'cart.html', context)


# update quntity funcntinality
def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    # print(c)      # display all cart products of authenticated user
    q=c[0].qty      # 
    if x=='1' :         #add qty functionality
        q=q+1
    elif q>1:           #decrease qty functionality
        q=q-1   
    c.update(qty=q)
    return redirect('/viewcart')


# Remove Product from cart 
def remove(request, cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')


# Place Order Page Logic
# def place_order(request):
#     c=Cart.objects.filter(uid=request.user.id)
#     a=Address.objects.filter(uid=request.user.id)
#     print(a)
#     for i in c:
#         o=Order.objects.create(
#             pid=i.pid, 
#             uid=i.uid, 
#             qty=i.qty, 
#             totalamt=i.qty*i.pid.price,
#             aid=a.id
#         )
#         o.save()
#         i.delete()  
#     return redirect('/fetchorder')
def place_order(request):
    c = Cart.objects.filter(uid=request.user.id)  # Fetch all cart items for the user
    a = Address.objects.filter(uid=request.user.id).first()  # Fetch the first address for the user

    if not a:  # If no address is found
        messages.error(request, "Please add an address before placing an order.")
        return redirect('/cart')  # Redirect to cart if no address is found

    for i in c:
        o = Order.objects.create(
            pid=i.pid,  # Product ID from the Cart item
            uid=i.uid,  # User ID from the Cart item
            qty=i.qty,  # Quantity from the Cart item
            totalamt=i.qty * i.pid.price,  # Total amount: qty * product price
            aid=a  # Use the address ID of the first address for the user
        )
        o.save()  # Save the order
        i.delete()  # Remove the cart item after the order is created
    
    return redirect('/fetchorder')  # Redirect to order confirmation or order listing page


def fetchorder(request):
    context={}
    o=Order.objects.filter(uid=request.user.id)
    amt=0
    for i in o:
        amt = amt + i.totalamt
    
    context['finalamt']=amt
    context['data']=o
    return render(request, 'pay.html', context )



def makepayment(request):
    context={}
    client = razorpay.Client(auth=("rzp_test_c66P03WlENQIxJ", "Om1tOy0A2HuYZUT0rHFnZgTd"))

    o=Order.objects.filter(uid=request.user.id)   #calculate the total amount to pay and add amt to dict
    amt=0
    for i in o:
        amt = amt + i.totalamt

    amt=amt*100 # to convert amount to paise 

    data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    context['payment']=payment

    c=Order.objects.filter(uid=request.user.id)
    # for i in c:
    #     o=OrderHistory.objects.create(pid=i.pid, uid=i.uid, qty=i.qty , totalamt=i.totalamt)
    #     o.save()
    #     i.delete() 

    return render(request, 'pay.html', context)
    


#paymentsuccess page after placing order
def paymentsuccess(request):
    sub="Santa's Treasure Order Status"
    msg="Your order has been successfully placed! Estimated delivery is within 3-4 days. Thank you for shopping with us!"
    frm='suhas8838@gmail.com'

    u=User.objects.filter(id=request.user.id)       #email should go to authenticated user only 
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],               #list beacause we can send mail to multiple emails-ids
        fail_silently=False
    )
    return render(request, 'paymentsuccess.html')






#`````````````  ADMIN RELATED LOGIC     ``````````````````


# Admin Login 
def adminLogin(request):
    print(User.objects.filter(username='admin@gmail.com'))
    context = {}
    if request.method == 'GET':
        return render(request, 'adminLogin.html', context)
    
    e = request.POST.get('ue')  # retrieve username
    p = request.POST.get('upass')  # retrieve password
    
    user = authenticate(username=e, password=p)  # Authenticate user
    if user:
        if user.is_staff:  # Check for staff privileges
            login(request, user)
            return redirect('/dashboard')  # Redirect to admin dashboard
        context['errormsg'] = "You don't have Admin access"
    else:
        context['errormsg'] = 'Invalid Admin Credentials'
    return render(request, 'adminLogin.html', context)  # Render the login page with error message



# Dashboard Page for Admin
def dashboard(request):
    # Fetch orders with related user and address data
    orders = Order.objects.select_related('uid').prefetch_related(
        'uid__address_set'
    )
    context = {
        'data': orders,
    }
    return render(request, 'dashboard.html', context)
# demo :
# def dashboard(request):
#     context={}
#     o=Order.objects.all()
#     for i in o:
#         # print(i.uid)
#         a=Address.objects.filter(uid=i.uid)
#         print(a)
#     context['data']=o
#     context['address']=a
#     return render(request,'dashboard.html',context)



# Track Order Page for Admin
def trackorder(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'trackorder.html')
    else:
        tid = request.POST.get('trackingid')  # Use .get() to avoid KeyError
        
        if not tid:
            context['errormsg'] = 'Please Enter Tracking ID'
            return render(request, 'trackorder.html', context)
        else:
            o = Order.objects.filter(id=tid)
            if o.exists(): 
                context['data'] = o 
            else:
                context['errormsg'] = 'Tracking ID Not Found'  

        return render(request, 'trackorderOutput.html', context)

    

    # return render(request, 'trackorder.html', context)

# View Order Page for Admin
def vieworder(request,oid):
    context={}
    order_detail=Order.objects.filter(id=oid)
    context['data']=order_detail
    print(order_detail)
    return render(request, 'vieworder.html', context)