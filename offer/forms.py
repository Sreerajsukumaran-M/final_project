from django import forms
from .models import Offer
from django.utils import timezone

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'discount_percentage', 'discount_amount', 
                 'start_date', 'end_date', 'offer_image']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date")
        
        if end_date and end_date < timezone.now():
            raise forms.ValidationError("End date cannot be in the past")
        
        discount_percentage = cleaned_data.get('discount_percentage')
        discount_amount = cleaned_data.get('discount_amount')
        
        if not discount_percentage and not discount_amount:
            raise forms.ValidationError("You must specify either discount percentage or discount amount")
        
        if discount_percentage and discount_amount:
            raise forms.ValidationError("You can only specify either discount percentage or discount amount, not both")
        
        return cleaned_data