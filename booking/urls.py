from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:product_id>/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('shop/bookings/', views.shop_bookings, name='shop_bookings'),
]