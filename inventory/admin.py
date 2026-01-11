# Register your models here.
from django.contrib import admin
from .models import Supplier, Customer, Product, Sale, Purchase, ContactMessage

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id','name','contact','email')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','selling_price','stock','supplier')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id','product','customer','quantity','amount','date')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'supplier', 'quantity', 'total_price', 'date')
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','email','submitted_at')
    readonly_fields = ('submitted_at',)
