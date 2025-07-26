from django.db import models
from django.contrib.auth.models import User
import datetime 
import os

def getFileName(instance, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{now_time}_{filename}"
    return os.path.join('uploads/', new_filename)

class Category(models.Model):

    name = models.CharField(max_length=200,null=False,blank=False)
    image = models.ImageField(upload_to =getFileName,null=True,blank=True)
    description = models.TextField(max_length=300,null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0-show,1-Hidden')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
class Product(models.Model):
    catagory = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=300, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, help_text='0-show, 1-Hidden')

    def __str__(self):
        return self.name

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    customer_detail = models.ForeignKey('CustomerDetail', null=True, blank=True, on_delete=models.SET_NULL)  # Temporarily allow null
    status = models.CharField(max_length=20, default='Pending')  # You can define status as needed
     
    @property
    def total_cost(self):
        return self.product_qty * self.product.price
    
class Favourite(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CustomerDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses",null=False,blank=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    # Address details
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default="India")  # Change default as per your region

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Payment(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.IntegerField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending')
)

class OrderPlaced(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerDetail,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False) 
    ordered_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default="Pending")
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default='')

    @property
    def total_cost(self):
        return self.product_qty * self.product.price
