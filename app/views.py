from itertools import product
from unicodedata import category, name
from django.shortcuts import render
from .models import Product
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


class ProductView(View):
    def get(self, request):
        sold = Product.objects.all()
        rating = Product.objects.all()
        return render(request,'app/home.html', {'rating':rating, 'sold':sold})

class ProductDetailView(View):
    def get(self, request, pk):
       product = Product.objects.get(pk=pk)
       return render(request, 'app/productdetail.html', {'product':product}) 


def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

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

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            Name = form.cleaned_data['name']
            Locality = form.cleaned_data['locality']
            City = form.cleaned_data['city']
            State = form.cleaned_data['state']
            Zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = usr, name=Name, locality=Locality,city = City, state=State, zipcode=Zipcode)
            reg.save()
            messages.success(request, 'Congratulations, Your Profile has been Updated Successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})