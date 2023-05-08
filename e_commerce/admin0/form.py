from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
         model = Category
         fields = ['category_name','description', 'cat_image',]
        
    def _init_(self, *args, **kwargs):
        super(CategoryForm,self)._init_(*args, **kwargs)
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



#regitration

class CreateUserForm(UserCreationForm):
   password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password',                                            'class':'form-control',
                                         'style':'max-width:300px;  margin-left:115px'}))
   password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password',                                            'class':'form-control',
                                         'style':'max-width:300px;  margin-left:115px'}))
   class Meta:
        model = Customer
        fields = ['username', 'email','password1', 'password2']
        widgets = { 
            'username': forms.TextInput(attrs=
                                        {'placeholder': 'First Name',
                                         'class':'form-control',
                                         'style':'max-width:300px; margin-left:115px'
                                         
                                         }),
            'email': forms.TextInput(attrs={'placeholder': 'Email',
                                            'class':'form-control',
                                         'style':'max-width:300px;  margin-left:115px'}),
        }