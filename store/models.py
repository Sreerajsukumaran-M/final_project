from django.db import models
from django.contrib.auth.models import User
from mall.models import Mall

class Store(models.Model):
    name = models.CharField(max_length=255)
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # New fields
    shop_image = models.ImageField(upload_to='shop_images/', null=True, blank=True)  # Shop image
    description = models.TextField(null=True, blank=True)  # Description about the shop

    def __str__(self):
        return self.name