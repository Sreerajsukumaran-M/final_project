from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from store.models import Store

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from store.models import Store

def add_product(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        # Pass the 'store' argument to the form
        form = ProductForm(request.POST, request.FILES, store=store)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store  # Assign the store to the product
            product.save()
            return redirect('product_list', store_id=store.id)
    else:
        # Pass the 'store' argument to the form
        form = ProductForm(store=store)
    return render(request, 'products/add_product.html', {'form': form, 'store': store})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list', store_id=product.store.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    store_id = product.store.id
    product.delete()
    return redirect('product_list', store_id=store_id)

def product_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    return render(request, 'products/product_list.html', {'store': store, 'products': products})