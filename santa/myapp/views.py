from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User        #imported by me, for authentication
from django.contrib.auth import authenticate         #imported by me, for authentication
from django.contrib.auth import login,logout
from myapp.models import Gifts,Cart
from django.db.models import Q          #Q class


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
    u=User.objects.filter(id=request.user.id)   # Fetch details of Authenticated User
    context['data']=u
    return render(request,'profile.html',context)

# Gifts/Product Page
def gifts(request):
    context={}
    g=Gifts.objects.filter(is_active=True) # Filter and Display only those data which are active
    context['data']=g
    return render(request,'gifts.html',context)

# Add to Cart Functionality
# def addtocart(request,pid):
#     context={}
#     if request.user.is_authenticated :  #check whether is login or not (if not then reddirect to login page)
#         # print('User is logged in')
#         u=User.objects.filter(id=request.user.id)       #used to get id of authenticated user id
#         # print(u)
#         p=Gifts.objects.filter(id=pid)
        
#         q1=Q(uid=u[0])
#         q2=Q(pid=p[0])
#         c=Cart.objects.create(uid=q1,pid=q2)
#         n=len(c)
#         if n==0:
#             c=Cart.objects.create(pid=p[0],uid=u[0])         #import cart
#             c.save()
#             context['success']='Product Added Successfully...!'
#         else:
#             context['errormsg']='Product Already Exist in Cart..!'
  
#         context['data']=p
#         return render(request,'gifts.html',context)
    
#     else:
#         return redirect('/login')
    
























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