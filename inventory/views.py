from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from datetime import date, timedelta
from .models import Product, Supplier, Customer, Sale, Purchase, ContactMessage
from .forms import ProductForm, ContactForm, SupplierForm, CustomerForm, SaleForm, PurchaseForm
from decimal import Decimal
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"

    return render(request, 'auth/login.html', {'error': error})



def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    products = Product.objects.all()[:6]

    low_stock = Product.objects.filter(stock__lt=5).count()
    soon_expiring = Product.objects.filter(
        expiry_date__lte=date.today() + timedelta(days=7)
    ).count()

    return render(request, "inventory/home.html", {
        "products": products,
        "low_stock": low_stock,
        "soon_expiring": soon_expiring,
    })



@login_required
def dashboard(request):
    total_products = Product.objects.filter(user=request.user).count()
    total_suppliers = Supplier.objects.filter(user=request.user).count()
    total_customers = Customer.objects.filter(user=request.user).count()

    total_sales = (
        Sale.objects.filter(user=request.user)
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    last_7_days_sales = (
        Sale.objects.filter(
            user=request.user,
            date__gte=date.today() - timedelta(days=7)
        )
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    predicted_next_week = round(last_7_days_sales * Decimal('1.10'))

    return render(request, "inventory/dashboard.html", {
        "total_products": total_products,
        "total_suppliers": total_suppliers,
        "total_customers": total_customers,
        "total_sales": total_sales,
        "predicted_next_week": predicted_next_week,
    })




@login_required
def products(request):
    products = Product.objects.filter(user=request.user)
    suppliers = Supplier.objects.filter(user=request.user)
    form = ProductForm()

    today = date.today()
    next_7 = today + timedelta(days=7)

    for p in products:
        if p.expiry_date:
            if p.expiry_date < today:
                p.expiry_status = "expired"
            elif today <= p.expiry_date <= next_7:
                p.expiry_status = "near"
            else:
                p.expiry_status = "good"
        else:
            p.expiry_status = None

    return render(request, 'inventory/products.html', {
        'products': products,
        'form': form,
        'suppliers': suppliers,
    })



def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    today = date.today()
    next_7 = today + timedelta(days=7)

    # EXPIRY STATUS
    if product.expiry_date:
        if product.expiry_date < today:
            product.expiry_status = "expired"
        elif today <= product.expiry_date <= next_7:
            product.expiry_status = "near"
        else:
            product.expiry_status = "good"
    else:
        product.expiry_status = None

    # SALES PREDICTION LOGIC
    last_10_sales = (
        Sale.objects.filter(product=product)
        .order_by('-date')[:10]
        .values_list('quantity', flat=True)
    )

    if last_10_sales:
        avg_sales = sum(last_10_sales) / len(last_10_sales)
        expected_sales = round(avg_sales)
    else:
        expected_sales = 0

    expected_profit = expected_sales * (product.selling_price - product.cost_price)
    future_stock = product.stock - expected_sales

    return render(request, 'inventory/product_view.html', {
        'product': product,
        'expected_sales': expected_sales,
        'expected_profit': expected_profit,
        'future_stock': future_stock,
    })



def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/product_edit.html', {'form': form, 'product': product})



def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
    return redirect('products')



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'inventory/contact.html', {'form': form})



@login_required
def suppliers(request):
    suppliers = Supplier.objects.filter(user=request.user)
    form = SupplierForm()
    return render(request, 'inventory/suppliers.html', {
        'suppliers': suppliers,
        'form': form
    })





@login_required
def customers(request):
    customers = Customer.objects.filter(user=request.user)
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request, "Customer added successfully!")
            return redirect('customers')

    return render(request, 'inventory/customers.html', {
        'form': form,
        'customers': customers
    })


def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added.')
    return redirect('customers')



@login_required
def sales(request):
    sales = Sale.objects.filter(user=request.user)
    form = SaleForm(user=request.user)
    return render(request, 'inventory/sales.html', {
        'sales': sales,
        'form': form
    })








@login_required
def purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    form = PurchaseForm()
    return render(request, 'inventory/purchases.html', {
        'form': form,
        'purchases': purchases
    })


@login_required
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, "Product added successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return redirect('products')

@login_required
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.save()
            messages.success(request, 'Supplier added successfully.')
        else:
            messages.error(request, "Error adding supplier. Please check fields.")
    return redirect('suppliers')

@login_required
def sale_add(request):
    if request.method == 'POST':
        form = SaleForm(request.POST, user=request.user)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            
            # Stock Check Logic
            product = sale.product
            if product.stock >= sale.quantity:
                sale.save()
                product.stock -= sale.quantity
                product.save()
                messages.success(request, 'Sale recorded and stock updated!')
            else:
                messages.error(request, f"Insufficient stock! Only {product.stock} left.")
        else:
            messages.error(request, "Invalid sale data.")
    return redirect('sales')

@login_required
def purchase_add(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()

            # Update stock based on product name
            try:
                prod = Product.objects.get(name=purchase.product_name, user=request.user)
                prod.stock += purchase.quantity
                prod.save()
                messages.success(request, 'Purchase recorded and stock increased!')
            except Product.DoesNotExist:
                messages.warning(request, 'Purchase saved, but no matching product name found to update stock.')
        else:
            messages.error(request, "Invalid purchase data.")
    return redirect('purchases')