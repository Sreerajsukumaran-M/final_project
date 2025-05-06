from django.db import models
from store.models import Store

class Product(models.Model):
    name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Ensure this line exists
    product_img = models.ImageField(upload_to='product_images/')
    category = models.CharField(max_length=100, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name