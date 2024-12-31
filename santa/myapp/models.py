import os
from django.db import models
from django.contrib.auth.models import User
import requests    

# Product Table
class Gifts(models.Model):
    CAT=((1,'Statue'),(2,'Tree'),(3,'Decorations'),(4,'Cloths'))
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    cat=models.IntegerField(verbose_name='category',choices=CAT)
    pdetails=models.CharField(max_length=100, verbose_name='Product Detail')
    is_active=models.BooleanField(default=True)
    image=models.ImageField(upload_to='image')

# Cart Table
class Cart(models.Model):
    uid=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='uid')    
    pid=models.ForeignKey('Gifts',on_delete=models.CASCADE, db_column='pid')   
    qty=models.IntegerField(default=1)


# Order Table
class Order(models.Model):
    uid=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='uid')    
    pid=models.ForeignKey('Gifts', on_delete=models.CASCADE, db_column='pid')      
    qty=models.IntegerField(default=1)
    totalamt=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    aid=models.ForeignKey('Address', on_delete=models.CASCADE, db_column='aid', null=True)
    status=models.CharField(max_length=50, default='Pending')

# Address table
class Address(models.Model):
    uid=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='uid')
    street_address = models.TextField()  
    city = models.CharField(max_length=50)  
    state = models.CharField(max_length=50)  
    postal_code = models.CharField(max_length=10)  
    phone = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    
# OTP table for delivery
class OTP(models.Model):
    oid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='oid')
    otp = models.CharField(max_length=4)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
