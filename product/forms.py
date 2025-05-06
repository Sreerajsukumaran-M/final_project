from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'product_img', 'category', 'count']

    def __init__(self, *args, **kwargs):
        # Pop the 'store' argument from kwargs before calling the parent's __init__
        self.store = kwargs.pop('store', None)
        super(ProductForm, self).__init__(*args, **kwargs)

        # Make 'category' and 'count' fields optional
        self.fields['category'].required = False
        self.fields['count'].required = False