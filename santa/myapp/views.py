from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User        
from django.contrib.auth import authenticate       
from django.contrib.auth import login,logout
from myapp.models import Gifts,Cart,Address
from django.db.models import Q          


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
def myprofile(request):
    context={}
    a=User.objects.filter(id=request.user.id)    # Fetch details of Authenticated User

    context['data']=a
    return render(request,'profile.html',context)


# Add Address/Phone
def addaddress(request):
    if request.method == 'GET':
        return render(request, 'addaddress.html')
    else:       # Retrieve form data
        street_address = request.POST['street_address']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['postal_code']
        phone = request.POST.get('phone', '')

        # Ensure the user is authenticated
        if request.user.is_authenticated:
            # Create the address object and associate it with the user instance
            Address.objects.create(
                uid=request.user,  # Pass the User instance directly
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
    a=Address.objects.filter(uid=request.user.id) 

    amt=0
    for i in c:
        amt = amt + i.pid.price * i.qty
    
    # context['totalamt']=amt
    # context['data']=c
    # context['data1']=a
    context={
        'data': c,
        'data1': a,
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
    context={}
    return render(request,'dashboard.html',context)


# Track Order Page for Admin
def trackorder(request):
    context={}
    return render(request, 'trackorder.html', context)

# View Order Page for Admin
def vieworder(request):
    context={}
    return render(request, 'vieworder.html', context)