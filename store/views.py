from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from mall.models import Mall
from .models import Store
from .forms import StoreForm

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from product.models import Product
from django.shortcuts import render, get_object_or_404
from mall.models import Mall
from .models import Store


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import default_storage
from mall.models import Mall
from .models import Store
from .forms import StoreForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Store
from .forms import StoreForm

def create_store(request, mall_id):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            # Create the Store and link it to the User and Mall
            store = form.save(commit=False)
            store.mall_id = mall_id
            store.save()
            messages.success(request, 'Store created successfully!')
            return redirect('mall_dashboard')  # Redirect to mall dashboard
    else:
        form = StoreForm()
    return render(request, 'stores/create_store.html', {'form': form})



# List all stores for a specific mall
@login_required
def store_list(request, mall_id):
    mall = get_object_or_404(Mall, id=mall_id)
    stores = Store.objects.filter(mall=mall)
    return render(request, 'stores/store_list.html', {'mall': mall, 'stores': stores})

# Update a store
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Store
from .forms import StoreForm

@login_required
def update_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated successfully!')
            return redirect('mall_dashboard')  # Redirect to mall dashboard
    else:
        form = StoreForm(instance=store)
    return render(request, 'stores/update_store.html', {'form': form, 'store': store})

# Delete a store
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.contrib import messages
from .models import Store

@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        # Delete the shop image if it exists
        if store.shop_image:
            default_storage.delete(store.shop_image.path)
        
        # Delete the associated user
        if store.user:
            store.user.delete()  # Delete the User object
        
        # Delete the store
        store.delete()
        
        messages.success(request, 'Store deleted successfully!')
        return redirect('mall_dashboard')  # Redirect to mall dashboard
    return render(request, 'stores/confirm_delete.html', {'store': store})

# Shop login
def shop_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'store'):  # Check if the user is a shop
            login(request, user)
            return redirect('shop_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'stores/shop_login.html')

# Shop dashboard
from django.shortcuts import render
from store.models import Store

def shop_dashboard(request):
    # Ensure the user is associated with a store
    if not hasattr(request.user, 'store'):
        return render(request, 'stores/error.html', {'message': 'You are not associated with any store.'})

    store = request.user.store
    products = Product.objects.filter(store=store)
    total_sales = sum(product.price for product in products)  # Example calculation
    recent_activity = "No recent activity"  # Replace with actual logic

    context = {
        'store': store,
        'products': products,
        'total_sales': total_sales,
        'recent_activity': recent_activity,
    }
    return render(request, 'stores/shop_dashboard.html', context)


# Logout
def store_logout(request):
    logout(request)
    return redirect('index_dashboard')

# List all shops for a specific mall
def shop_list(request, mall_id):
    mall = get_object_or_404(Mall, id=mall_id)  # Get the selected mall
    shops = Store.objects.filter(mall=mall)  # Get shops for the selected mall
    return render(request, 'stores/shop_list.html', {'mall': mall, 'shops': shops})

from product.models import Product

def customer_product_list(request, shop_id):
    shop = get_object_or_404(Store, id=shop_id)
    products = Product.objects.filter(store=shop)
    return render(request, 'stores/product_list.html', {
        'shop': shop,
        'products': products,
        'mall': shop.mall  # Add this line to pass the mall to the template
    })