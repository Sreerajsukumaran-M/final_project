from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product
from .forms import BookingForm, BookingStatusForm
from .models import Booking
from store.models import Store

@login_required
def create_booking(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    shop = product.store  # Get the store from the product
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.product = product
            booking.shop = shop.user  # Assuming store has a user field
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'booking/create_booking.html', {
        'form': form,
        'product': product,
        'shop': shop  # Make sure to pass the shop to the template
    })


@login_required
def booking_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    is_shop_owner = request.user == booking.shop
    
    if request.method == 'POST' and is_shop_owner:
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking status updated!')
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = BookingStatusForm(instance=booking)
    
    return render(request, 'booking/details.html', {
        'booking': booking,
        'form': form,
        'is_shop_owner': is_shop_owner
    })

@login_required
def shop_bookings(request):
    if not hasattr(request.user, 'store'):
        messages.error(request, "You don't have a shop")
        return redirect('index')
    
    bookings = Booking.objects.filter(shop=request.user).order_by('-booking_date')
    return render(request, 'booking/shop_bookings.html', {'bookings': bookings})