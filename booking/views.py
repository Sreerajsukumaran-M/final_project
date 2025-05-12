from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from .forms import BookingForm, BookingStatusForm
from .models import Booking
from store.models import Store
import razorpay

@login_required
def create_booking(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    shop = product.store

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.product = product
            booking.shop = shop.user
            booking.save()
            return redirect('initiate_payment', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'booking/create_booking.html', {
        'form': form,
        'product': product,
        'shop': shop
    })

@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    DATA = {
        "amount": int(booking.product.price * 100),  # price in paise
        "currency": "INR",
        "receipt": f"booking_rcptid_{booking.id}",
        "payment_capture": 1
    }

    order = client.order.create(data=DATA)
    booking.razorpay_order_id = order['id']
    booking.save()

    return render(request, 'booking/payment.html', {
        'booking': booking,
        'order': order,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    })

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        booking_id = data.get("booking_id")

        try:
            booking = Booking.objects.get(id=booking_id)
            booking.razorpay_payment_id = data.get('razorpay_payment_id')
            booking.razorpay_signature = data.get('razorpay_signature')
            booking.payment_status = 'paid'
            booking.save()
            messages.success(request, "Payment successful!")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")

        return redirect('booking_details', booking_id=booking_id)

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

    # Only show bookings that are NOT delivered
    bookings = Booking.objects.filter(shop=request.user).exclude(status='delivered').order_by('-booking_date')
    
    return render(request, 'booking/shop_bookings.html', {'bookings': bookings})
