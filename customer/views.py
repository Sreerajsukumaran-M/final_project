from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

from booking.models import Booking
from .forms import CustomerRegistrationForm  # Import your custom form

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('customer_login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customers/customer_register.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')  # Redirect to customer dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'customers/customer_login.html')

from django.contrib.auth.decorators import login_required

@login_required
def customer_dashboard(request):
    recent_bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')[:3]
    return render(request, 'customers/customer_dashboard.html', {
        'recent_bookings': recent_bookings
    })


def customer_logout(request):
    logout(request)
    return redirect('index_dashboard')


@login_required
def customer_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'booking/customer_bookings.html', {'bookings': bookings})