from django.db import models
from django.utils import timezone
from store.models import Store

class Offer(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    offer_image = models.ImageField(upload_to='offer_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.store.name}"

    def save(self, *args, **kwargs):
        # Auto-deactivate expired offers
        if self.end_date < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

    @property
    def is_current(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active

    class Meta:
        ordering = ['-start_date']