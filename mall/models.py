from django.db import models
from django.contrib.auth.models import User

class Mall(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mall_images/', null=True, blank=True)


    def __str__(self):
        return self.name