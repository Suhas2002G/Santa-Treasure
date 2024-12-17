from django.contrib import admin
from myapp.models import Gifts  #import model class from models.py
# Register your models here.
# username : Admin 
# password : Admin@123



class GiftsAdmin(admin.ModelAdmin):
    list_display=['id','name','cat','price','pdetails','is_active']
    list_filter=['is_active','cat']

admin.site.register(Gifts,GiftsAdmin) 
