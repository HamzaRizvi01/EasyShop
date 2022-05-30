from itertools import product
from unicodedata import category
from django.shortcuts import render
from .models import Product
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages


class ProductView(View):
    def get(self, request):
        laptop = Product.objects.filter(category='L')
        mobile = Product.objects.filter(category='M')
        return render(request,'app/home.html', {'mobile':mobile, 'laptop':laptop})

#def product_detail(request):
 #return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
       product = Product.objects.get(pk=pk)
       return render(request, 'app/productdetail.html', {'product':product}) 


def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')


def mobile(request, data=None):
 if data == None:
     mobiles = Product.objects.filter(category='M')
 elif data == 'Apple' or data == 'Samsung' or 'Oppo':
     mobiles = Product.objects.filter(category='M').filter(brand=data)
 #elif data == 'below':
  #  mobiles = Product.objects.filter(category='M').filter(discounted_price__lte=200000.0)
 #elif data == 'above':
  #   mobiles = Product.objects.filter(category='M').filter(discounted_price__gte=200000.0)
 return render(request, 'app/mobile.html', {'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html', {'form':form} )
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'You Have Successfully Registered')
            form.save()
        return render(request,'app/customerregistration.html', {'form':form} )

def checkout(request):
 return render(request, 'app/checkout.html')

