from typing import Any, Mapping
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, Account
from django import forms
class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type":'date'}))
    address = forms.CharField(max_length=254)
    city = forms.CharField(max_length=254)
    country = forms.CharField(max_length=254)
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone',
            'birth_date',  'address', 'city', 'country', 'password1', 'password2',
        ]

    def save(self, commit=True):
        new_user = super().save(commit=False)
        if commit:
            new_user.save()
            address = self.cleaned_data.get('address')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')

            Account.objects.create(
                user = new_user,
                address = address,
                city =city,
                country = country
            )

        return new_user

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type":'date'}))
    address = forms.CharField(max_length=254)
    city = forms.CharField(max_length=254)
    country = forms.CharField(max_length=254)
    class Meta:
        model = User
        fields = [
            'profile_pic', 'username', 'first_name', 'last_name', 'email', 'phone',
            'birth_date', 'bio',  'address', 'city', 'country',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account = self.instance.account
            except Account.DoesNotExist:
                user_account = None
                
            if user_account:
                self.fields['address'].initial = user_account.address
                self.fields['city'].initial = user_account.city
                self.fields['country'].initial = user_account.country
                
                
class DepositeForm(forms.Form):
    deposite_amount = forms.DecimalField()
    
    def clean_deposite_amount(self):
        min_deposit_amount = 50
        amount = self.cleaned_data.get('deposite_amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least ${min_deposit_amount}'
            )
        return amount
        
        