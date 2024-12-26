from django.db import models
from django.contrib.auth.models import User     #imported for cart functinality

# Create your models here.
class Gifts(models.Model):
    CAT=((1,'Statue'),(2,'Tree'),(3,'Decorations'),(4,'Cloths'))
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    cat=models.IntegerField(verbose_name='category',choices=CAT)
    pdetails=models.CharField(max_length=100, verbose_name='Product Detail')
    is_active=models.BooleanField(default=True)
    image=models.ImageField(upload_to='image')

class Cart(models.Model):
    uid=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='uid')    #since user table is part auth_user, we have to import it
    pid=models.ForeignKey('Gifts',on_delete=models.CASCADE, db_column='pid')       #Gift is part of same model file 
    qty=models.IntegerField(default=1)


class Order(models.Model):
    uid=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='uid')    #since user table is part auth_user, we have to import it
    pid=models.ForeignKey('Gifts',on_delete=models.CASCADE, db_column='pid')       #Product is part of same model file 
    qty=models.IntegerField(default=1)
    totalamt=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    aid=models.ForeignKey('Address',on_delete=models.CASCADE, db_column='aid', null=True)




class Address(models.Model):
    uid=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='uid')
    street_address = models.TextField()  # Street address
    city = models.CharField(max_length=50)  # City
    state = models.CharField(max_length=50)  # State
    postal_code = models.CharField(max_length=10)  # Postal/ZIP code
    phone = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

class OTP(models.Model):
    oid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='oid')
    otp = models.CharField(max_length=4)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class DeliveryStatus(models.Model):
    oid = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='delivery_status')  # Foreign key to Order model
    status = models.CharField(max_length=50)  # Delivery status (In Progress, Delivered, Cancelled, etc.)
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the status was updated
