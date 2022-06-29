from itertools import product
from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
State_Choices = (
    ('Punjab','Punjab'),
    ('Islamabad','ICT'),
    ('Sindh','Sindh'),
    ('Balochistan','Balochistan'),
    ('KPK','KPK'),
)
Status_Choice = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=State_Choices, max_length=50)

def __str__(str):
    return str(self.id)

Category_Choice = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),  
)

class Product(models.Model):
    #id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    product_image = models.ImageField(upload_to='productimg')
    title = models.CharField(max_length=100)
    Sold = models.IntegerField()
    Rating = models.FloatField()
    selling_price = models.FloatField()
    sentiment = models.CharField(max_length=10, default='NULL')
    website = models.CharField(max_length=10, default='NULL')
    
    

def __str__(str):
    return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price



class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=Status_Choice, default='Pending')

    def __str__(self):
     return str(self.id)

     
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price


# Create your models here.