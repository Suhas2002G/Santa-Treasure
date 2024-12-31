from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
from django.contrib.auth.models import User        
from django.contrib.auth import authenticate       
from django.contrib.auth import login,logout
from myapp.models import Gifts,Cart,Address,Order,OTP
from django.db.models import Q     
import razorpay 
from django.core.mail import send_mail    
import random 
import os
import requests
import logging
from dotenv import load_dotenv
from django.db.models import Count
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



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


# My Profile Page for User
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



# Add address page
def addaddress(request):
    # Load the Google Maps API key from environment variables
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    context = {
        'google_maps_api_key': api_key  # Pass the API key to the frontend
    }

    if request.method == 'POST':
        # Get the form data (manual input or from suggestion)
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone', '')
        suggested_address = request.POST.get('suggested_address', '')

        # If the address was entered manually
        if street_address and city and state and postal_code:
            full_address = f"{street_address}, {city}, {state}, {postal_code}"
        # If the address was selected from the suggestions
        elif suggested_address:
            full_address = suggested_address
        else:
            context['errormsg'] = "Please provide a valid address."
            return render(request, 'addaddress.html', context)

        latitude = None
        longitude = None

        # Fetch the latitude and longitude using Google Geocoding API
        try:
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={full_address}&key={api_key}"
            response = requests.get(geocode_url)
            geocode_data = response.json()

            if response.status_code == 200 and geocode_data.get('status') == 'OK':
                location = geocode_data['results'][0]['geometry']['location']
                latitude = location['lat']
                longitude = location['lng']
            else:
                context['errormsg'] = f"Error fetching location: {geocode_data.get('status')}"
                return render(request, 'addaddress.html', context)

        except Exception as e:
            context['errormsg'] = f"An error occurred: {e}"
            return render(request, 'addaddress.html', context)

        # Save to database
        if request.user.is_authenticated:
            try:
                Address.objects.create(
                    uid=request.user,
                    street_address=street_address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    phone=phone,
                    latitude=latitude,
                    longitude=longitude
                )
            except Exception as e:
                context['errormsg'] = f"Error while saving address: {e}"
                return render(request, 'addaddress.html', context)

            return redirect('/myprofile')
        else:
            return redirect('/login')  # Redirect to login if not authenticated

    return render(request, 'addaddress.html', context)



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


# Display product acc to category
def catfilter(request,cv):      
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Gifts.objects.filter(q1 & q2)     # when we want to use two conditions in filter 
    d={}
    d['data']=p
    return render(request,'gifts.html',d)


# it is used to filter based on min max values
def pricefilter(request):
    min=request.GET['min']    
    max=request.GET['max']
    # print(min)
    # print(max)
    
    q1=Q(price__gte = min)
    q2=Q(price__lte = max)
    p=Gifts.objects.filter(q1 & q2)
    d={}
    d['data']=p
    return render(request,'gifts.html',d)



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


# Place Order Page
def place_order(request):
    c = Cart.objects.filter(uid=request.user.id)  # Fetch all cart items for the user
    a = Address.objects.filter(uid=request.user.id).first()  # Fetch the first address for the user

    if not a:  # If no address is found
        # messages.error(request, "Please add an address before placing an order.")
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
    # os.environ.get['razorpay_api'] = Your Razorpay API
    # os.environ.get['razorpay_api_key'] = Your Razorpay API Password
    client = razorpay.Client(auth=(os.environ.get['razorpay_api'], os.environ.get['razorpay_api_key']))

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
    frm='santa.treasure2024@gmail.com'

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
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    in_transit_orders = Order.objects.filter(status='In-Transit').count()
    
    # Initialize the query to fetch all orders
    orders = Order.objects.select_related('uid').prefetch_related('uid__address_set').order_by('-created_at')

    # Apply filters based on the request parameters
    order_id = request.GET.get('order_id')
    city = request.GET.get('city')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Apply filters if parameters are provided
    if order_id:
        orders = orders.filter(id=order_id)
    
    if city:
        orders = orders.filter(uid__address__city__icontains=city)
    
    if start_date:
        # Ensure the start date is converted to a datetime object
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        orders = orders.filter(created_at__gte=start_date_obj)

    if end_date:
        # Ensure the end date is converted to a datetime object
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the time to the last moment of the end date (23:59:59.999999)
        end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
        orders = orders.filter(created_at__lte=end_date_obj)

    context = {
        'data': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'in_transit_orders':in_transit_orders,
    }
    return render(request, 'dashboard.html', context)



# Filter based on delivery status
def filter_status(request,sid):
    context={}
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    in_transit_orders = Order.objects.filter(status='In-Transit').count()
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'in_transit_orders':in_transit_orders,
    }
    if sid == '1':
        o=Order.objects.all().order_by('-created_at')
        context['data']=o
        return render(request, 'dashboard.html', context)
    elif sid == '2' :
        o=Order.objects.filter(status='Pending').order_by('-created_at')
        context['data']=o
        print(o)
        return render(request, 'dashboard.html', context)
    elif sid == '3':
        o=Order.objects.filter(status='Delivered').order_by('-created_at')
        context['data']=o
        return render(request, 'dashboard.html', context)
    elif sid == '4':
        o=Order.objects.filter(status='In-Transit').order_by('-created_at')
        context['data']=o
        return render(request, 'dashboard.html', context)

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

 

def search_location(request):
    s = request.GET.get('srchloc', '')  # Use .get() to avoid MultiValueDictKeyError
    if not s:  # Check if search term is empty
        context = {'errmsg': 'Please enter a location to search.'}
        return render(request, 'dashboard.html', context)

    # Filter orders based on the location (city and state)
    p = Order.objects.filter(aid__city__icontains=s)
    p1 = Order.objects.filter(aid__state__icontains=s)

    output = p.union(p1)

    # Prepare context to pass to the template
    context = {}
    if output.exists():
        context['data'] = output
    else:
        context['errmsg'] = 'Order Not Found'

    return render(request, 'dashboard.html', context)



def vieworder(request, oid):
    # Fetch the order detail using the given order ID (oid)
    order_detail = Order.objects.get(id=oid)
    
    # Get the customer's address related to the order
    address = order_detail.aid
    customer_lat = address.latitude
    customer_lng = address.longitude
    
    # Coordinates for office  (fixed coordinates)
    office_lat = 18.5960313106708  # Latitude for Itvedant Pimpri Branch
    office_lng = 73.78822641307697  # Longitude for Itvedant Pimpri Branch
    
    load_dotenv()  # This loads the .env file into environment variables

    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    context = {
        'order': order_detail,
        'customer_lat': customer_lat,
        'customer_lng': customer_lng,
        'office_lat': office_lat,
        'office_lng': office_lng,
        'google_maps_api_key': google_maps_api_key,
    }
    
    # Render the order details page
    return render(request, 'vieworder.html', context)



def mark_as_deliver(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    customer_email = order.uid.email
    
    # Generate a random 4-digit OTP
    otp = str(random.randint(1000, 9999))

    # Save OTP to the database
    OTP.objects.create(
        oid=order,
        otp=otp,
        email=customer_email,
    )
    
    # Send OTP to customer email
    send_mail(
        'Your Order OTP',
        f'Your OTP for order is {otp}. Kindly share it at the time of delivery.',
        'santa.treasure2024@gmail.com',
        [customer_email],
        fail_silently=False,
    )
    return redirect('verify_otp', order_id=order.id)


# OTP verification 
def verify_otp(request, order_id):
    context = {}
    if request.method == 'POST':
        input_otp = request.POST['otp']
        try:
            # otp_entry = OTP.objects.get(oid=order_id)
            otp_entry = OTP.objects.filter(oid=order_id).order_by('-created_at').first()


            # Check if the OTP is correct
            if input_otp == otp_entry.otp:
                # Update the order status to "Delivered"
                order = otp_entry.oid  # Fetch the actual order object here
                order.status = 'Delivered'
                order.save()

                context['success_message'] = 'Order delivered successfully!'
                context['redirect'] = True  # Flag to trigger JavaScript redirect
            else:
                context['error_message'] = 'Incorrect OTP. Please try again.'
        
        except OTP.DoesNotExist:
            return redirect('/trackorder')  # Or any appropriate redirect
    
    # Pass the order_id and any messages to the template
    return render(request, 'verify_otp.html', {'order_id': order_id, **context})




# Generate Shipping Label
def generatelabel(request, order_id):
    # Fetch the order details
    order = get_object_or_404(Order, id=order_id)
    # Fetch the associated address
    address = order.aid

    # If 'download_pdf' is in the query parameters, update the order status and generate PDF
    if request.GET.get('download_pdf'):
        if order.status != 'Delivered':
            order.status = 'In-Transit'  # Change the order status to 'In-Transit'
            order.save()  # Save the updated order status

        # Create the PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="shipping_label_{order.id}.pdf"'

        # Create PDF using ReportLab
        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setFont("Helvetica", 12)

        # Add header
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(200, 750, "Shipping Label")
        pdf_canvas.setFont("Helvetica", 12)
        
        # Order Details (aligned left)
        pdf_canvas.drawString(100, 710, f"Order ID: {order.id}")
        pdf_canvas.drawString(100, 690, f"Tracking ID: {f'OD-{order.id}-{order.created_at.strftime('%Y%m%d')}'}")
        pdf_canvas.drawString(100, 670, f"Customer Name: {order.uid.first_name}")
        pdf_canvas.drawString(100, 650, f"Product Name: {order.pid.name}")
        pdf_canvas.drawString(100, 630, f"Quantity: {order.qty}")
        pdf_canvas.drawString(100, 610, f"Total Amount: Rs. {order.totalamt}")

        # Shipping Address (aligned left)
        pdf_canvas.drawString(100, 590, "Shipping Address:")
        pdf_canvas.drawString(100, 570, f"Street: {address.street_address}")
        pdf_canvas.drawString(100, 550, f"City: {address.city}, State: {address.state} - {address.postal_code}")
        pdf_canvas.drawString(100, 530, f"Phone: {address.phone}")

        # Footer (aligned center)
        pdf_canvas.setFont("Helvetica-Oblique", 10)
        pdf_canvas.drawString(200, 50, "Thank you for choosing Santa's Treasure Pvt Ltd.")

        # Save the PDF
        pdf_canvas.showPage()
        pdf_canvas.save()

        return response

    # Otherwise, render the label template for display
    context = {
        'order_id': order.id,
        'user_name': order.uid.first_name,
        'product_name': order.pid.name,
        'product_qty': order.qty,
        'total_amount': order.totalamt,
        'address': address,
        'shipper_name': "SANTA'S TREASURE PVT LTD",
        'tracking_id': f"OD-{order.id}-{order.created_at.strftime('%Y%m%d')}",
    }

    return render(request, 'labeltemplate.html', context)




# Report Page [Pie chart & Bar Code]
def order_report(request):
    # Count orders by status
    pending = Order.objects.filter(status='Pending').count()
    in_transit = Order.objects.filter(status='In-Transit').count()
    delivered = Order.objects.filter(status='Delivered').count()

    # Count orders by city 
    city_order_counts = Order.objects.values('aid__city').annotate(order_count=Count('aid')).order_by('aid__city')

    # Prepare the data to be passed to the template
    order_status_data = {
        'pending': pending,
        'in_transit': in_transit,
        'delivered': delivered,
    }

    # Extract city names and order counts from the query
    cities = [item['aid__city'] for item in city_order_counts]
    order_counts = [item['order_count'] for item in city_order_counts]

    return render(request, 'order_report.html', {
        'order_status_data': order_status_data,
        'cities': cities,
        'order_counts': order_counts
    })