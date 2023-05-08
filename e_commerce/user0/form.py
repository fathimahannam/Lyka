from django import forms
from .models import *
class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressDetails
        fields = ('first_name', 'last_name', 'phone', 'email', 'order_address', 'city', 'state', 'country', 'zip_code')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter Your First Name','class':'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Your Last Name','class':'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Your Phone Number','class':'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter Your Address','class':'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter Your State','class':'form-control'}),
            'zip_code': forms.NumberInput(attrs={'placeholder': 'Enter Your Pincode','class':'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter Your City','class':'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter Your Email','class':'form-control'}),
            'order_address': forms.TextInput(attrs={'placeholder': 'Landmark','class':'form-control'}),
            
            
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['name', 'min_amount', 'discount_price', 'is_expired']        