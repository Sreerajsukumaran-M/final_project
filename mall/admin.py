from django.contrib import admin
from .models import Mall

@admin.register(Mall)
class MallAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'user')