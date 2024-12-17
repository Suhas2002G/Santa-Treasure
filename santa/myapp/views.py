from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User        #imported by me, for authentication
from django.contrib.auth import authenticate         #imported by me, for authentication
from django.contrib.auth import login,logout
from myapp.models import Gifts,Cart
from django.db.models import Q          #Q class


# Create your views here.
def home(request):
    return render(request,'home.html')

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
                u.set_password(p)  #set_password : it is used to convert password into encripted password
                u.save()
                context['success']='User Created Successfully'
            except Exception:
                context['errormsg']='User Already Exists'
        return render(request,'register.html',context)
    



def user_login(request):
    context={}
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        e=request.POST['ue']
        p=request.POST['upass']
        u=authenticate(username=e,password=p) #also import from auth
        if u is not None:
            login(request,u)        #also import from auth
            return redirect('/')
        else:
            context['errormsg']='Invalid Credential'
            return render(request,'login.html',context)


def user_logout(request):
    logout(request)
    return redirect('/')


def dashboard(request):
    return render(request,'dashboard.html')

def adminLogin(request):
    return render(request,'adminLogin.html')

def myprofile(request):
    return render(request,'profile.html')


def gifts(request):
    context={}
    g=Gifts.objects.filter(is_active=True) #filter and display only those data which are active
    context['data']=g
    return render(request,'gifts.html',context)

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
    