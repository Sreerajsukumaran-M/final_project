# store/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Store

class StoreForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Store
        fields = [
            'name', 'category', 'mobile_number', 'email',
            'username', 'password', 'shop_image', 'description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            if not (self.instance and self.instance.user and self.instance.user.username == username):
                raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        store = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if store.user:
            user = store.user
            user.username = username
            if password:
                user.set_password(password)
            user.save()
        else:
            user = User.objects.create_user(username=username, password=password)
            store.user = user

        if commit:
            store.save()
        return store
