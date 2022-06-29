from django.contrib import messages
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django import forms
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price','discounted_price' ,'description','Rating','Sold','brand', 'category']
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Wrong type of file has been uploaded')
                return HttpResponseRedirect(request.path_info)
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            for x in csv_data:
                fields = x.split(",")
                created = Product.objects.update_or_create(
                    id = fields[0],
                    title = fields[1],
                    selling_price = fields[2],
                    discounted_price = fields[3],
                    description = fields[4],
                    Rating = fields[5],
                    Sold = fields[6],
                    brand = fields[7],
                    category = fields[8],
                    #product_image = fields[7]
                )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form":form}
        return render(request, "admin/csv_upload.html", data)

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product','quantity', 'ordered_date', 'status']
