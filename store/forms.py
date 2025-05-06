from django import forms
from django.contrib.auth.models import User
from .models import Store

class StoreForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)  # Optional password

    class Meta:
        model = Store
        fields = ['name', 'category', 'username', 'password', 'shop_image', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill the username field if the store already has an associated user
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            # If the username belongs to the current store's user, allow it
            if not (self.instance and self.instance.user and self.instance.user.username == username):
                raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def save(self, commit=True):
        store = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # Handle the associated User object
        if store.user:  # If the store already has a user, update the user
            user = store.user
            user.username = username
            if password:  # Only update the password if a new one is provided
                user.set_password(password)
            user.save()
        else:  # If the store doesn't have a user, create a new one
            user = User.objects.create_user(username=username, password=password)
            store.user = user

        if commit:
            store.save()  # Save the store instance to the database
        return store