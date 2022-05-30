from itertools import product
from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
State_Choices = (
    ('Punjab','Lahore'),
    ('Islamabad','Islamabad'),
    ('Sindh','Karachi'),
    ('Balochistan','Quetta'),
    ('KPK','Peshawer'),
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
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    Rating = models.FloatField()
    Sold = models.IntegerField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=Category_Choice, max_length=1)
    product_image = models.ImageField(upload_to='productimg')

def __str__(str):
    return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

def __str__(self):
    return str(self.id)

Status_Choice = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=State_Choices, default='Pending')

def __str__(self):
    return str(self.id)
# Create your models here.