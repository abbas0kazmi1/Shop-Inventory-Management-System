
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/', views.product_view, name='product_view'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),

    path('customers/', views.customers, name='customers'),
    path('customers/add/', views.customer_add, name='customer_add'),

    path('sales/', views.sales, name='sales'),
    path('sales/add/', views.sale_add, name='sale_add'),

    path('purchases/', views.purchases, name='purchases'),
    path('purchases/add/', views.purchase_add, name='purchase_add'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
     path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
