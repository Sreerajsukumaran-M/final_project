from django.urls import path
from . import views

urlpatterns = [
    path('booking/<int:product_id>/create/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/pay/', views.initiate_payment, name='initiate_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('shop/bookings/', views.shop_bookings, name='shop_bookings'),
]
