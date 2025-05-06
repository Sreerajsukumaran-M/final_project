from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages


def mall_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mall_dashboard')  # Redirect to mall dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'malls/mall_login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Store
from store.forms import StoreForm

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import Store

@login_required
def mall_dashboard(request):
    mall = request.user.mall  # Assuming a OneToOneField between User and Mall
    stores = Store.objects.filter(mall=mall)
    return render(request, 'malls/mall_dashboard.html', {'mall': mall, 'stores': stores})

def mall_logout(request):
    logout(request)
    return redirect('index_dashboard')


from django.shortcuts import render
from .models import Mall

def mall_list(request):
    location = request.GET.get('location')  # Get the selected location from the dropdown
    if location:
        malls = Mall.objects.filter(location=location)  # Filter malls by location
    else:
        malls = Mall.objects.all()  # Show all malls if no location is selected

    # Get unique locations for the dropdown
    locations = Mall.objects.values_list('location', flat=True).distinct()

    return render(request, 'malls/mall_list.html', {'malls': malls, 'locations': locations})


