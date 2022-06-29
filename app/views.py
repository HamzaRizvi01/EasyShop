from itertools import product
from multiprocessing.sharedctypes import Value
from unicodedata import category, name
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        totalitem = 0
        sold = Product.objects.all()
        rating = Product.objects.all()
        Website = Product.objects.all()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html', {'rating':rating, 'sold':sold, 'totalitem':totalitem, 'Website':Website})

class ProductDetailView(View):
    def get(self, request, pk):
       totalitem = 0
       product = Product.objects.get(pk=pk)
       item_already_in_cart = False
       if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
       return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem}) 

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 
 print(product)
 return redirect('/cart')

def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 500.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                
                if amount <= 10000.0:
                    totalamount = amount + shipping_amount
                    
                elif amount > 10000.0:
                    totalamount = amount
                    shipping_amount = 0.0
                    
        totalamount = round(totalamount, 2)
        shipping_amount = round(shipping_amount, 2)
        amount = round(amount, 2)
        return render(request, 'app/addtocart.html', {'carts':cart,'totalitem':totalitem, 'totalamount':totalamount, 'amount':amount, 'shipping_amount':shipping_amount})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 400.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            if amount <= 10000.0:
                totalamount = amount + shipping_amount
            elif amount > 10000.0:
                totalamount = amount
                shipping_amount = 0.0
        totalamount = round(totalamount, 2)
        shipping_amount = round(shipping_amount, 2)
        amount = round(amount, 2)
        data = {
          'quantity':c.quantity,
          'amount':amount,
          'totalamount':totalamount
        }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    
        c.quantity-=1
        c.save()
   
        amount = 0.0
        shipping_amount = 400.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            if amount <= 10000.0:
                totalamount = amount + shipping_amount
            elif amount > 10000.0:
                totalamount = amount
                shipping_amount = 0.0
        totalamount = round(totalamount, 2)
        shipping_amount = round(shipping_amount, 2)
        amount = round(amount, 2)
        data = {
          'quantity':c.quantity,
          'amount':amount,
          'totalamount':totalamount
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print(c.id)
        c.delete()
        print(c.id)
        amount = 0.0
        totalamount = 0.0
        shipping_amount = 400.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            if amount <= 10000.0:
                totalamount = amount + shipping_amount
            elif amount > 10000.0:
                totalamount = amount
                shipping_amount = 0.0
        totalamount = round(totalamount, 2)
        shipping_amount = round(shipping_amount, 2)
        amount = round(amount, 2)
        data = {
          'amount':amount,
          'totalamount':totalamount
        }
    return JsonResponse(data)

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
 totalitem = 0
 add = Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html', {'add':add, 'totalitem':totalitem,'active':'btn-primary'})

@login_required
def orders(request):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':totalitem})


#def mobile(request, data=None):
 #if data == None:
  #   mobiles = Product.objects.filter(category='M')
# elif data == 'Apple' or data == 'Samsung' or 'Oppo':
  #   mobiles = Product.objects.filter(category='M').filter(brand=data)
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

def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        product = Product.objects.all()
        post = Product.objects.filter(title__contains=search)
        return render(request,'app/search.html',{'post':post, 'product':product})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    totalitem = 0
    amount = 0.0
    totalamount = 0.0
    shipping_amount = 400.0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            if amount <= 10000.0:
                totalamount = amount + shipping_amount
            elif amount > 10000.0:
                totalamount = amount
                shipping_amount = 0.0
    totalamount = round(totalamount, 2)
    shipping_amount = round(shipping_amount, 2)
    amount = round(amount, 2)    
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem':totalitem})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            totalitem = 0
            usr = request.user
            Name = form.cleaned_data['name']
            Locality = form.cleaned_data['locality']
            City = form.cleaned_data['city']
            State = form.cleaned_data['state']
            Zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = usr, name=Name, locality=Locality,city = City, state=State, zipcode=Zipcode)
            reg.save()
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
            messages.success(request, 'Congratulations, Your Profile has been Updated Successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
