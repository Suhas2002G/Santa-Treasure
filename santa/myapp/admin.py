from django.contrib import admin
from myapp.models import Gifts,OTP,Address,Order  #import model class from models.py
# Register your models here.
# username : Admin 
# password : Admin@123



class GiftAdmin(admin.ModelAdmin):
    list_display=['id','name','cat','price','pdetails','is_active']
    list_filter=['is_active','cat']

class AddressAdmin(admin.ModelAdmin):
    list_display=['id','street_address','city','state','postal_code']
    list_filter=['city','state']

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','pid','uid','aid','qty','totalamt','status']
    list_filter=['status']

class OTPAdmin(admin.ModelAdmin):
    list_display=['id','oid','email','otp',]
    list_filter=['email',]

admin.site.register(Gifts,GiftAdmin) 
admin.site.register(Address,AddressAdmin) 
admin.site.register(Order,OrderAdmin) 
admin.site.register(OTP,OTPAdmin) 
