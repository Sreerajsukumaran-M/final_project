from django.db import models
from django.conf import settings
from product.models import Product

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('delivered', 'deliverd'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_bookings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shop_bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    # 🔽 Payment-related fields
    payment_status = models.CharField(max_length=20, default='pending')  # pending, paid, failed
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.product.name}"

    class Meta:
        ordering = ['-booking_date']
