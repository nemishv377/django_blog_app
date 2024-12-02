from django import forms
from django.forms import ModelForm
from .models import Author
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

def validate_date_of_birth(value):
  if value > timezone.now().date():
    raise ValidationError("Date of birth cannot be in the future.")
      
class AuthorSignupForm(UserCreationForm):
  email = forms.EmailField(
    required=True, 
    error_messages={'required': 'Email is required'},
    widget=forms.TextInput(attrs={'size': '40'})
  )
  first_name = forms.CharField(
    required=True, 
    error_messages={'required': 'First Name is required'},
    widget=forms.TextInput(attrs={'size': '40'})
  )
  last_name = forms.CharField(
    required=True, 
    error_messages={'required': 'Last Name is required'},
    widget=forms.TextInput(attrs={'size': '40'})
  )
  username = forms.CharField(
    required=True, 
    error_messages={'required': 'username is required'},
    widget=forms.TextInput(attrs={'size': '40'})
  )
  password1 = forms.CharField(
    widget=forms.PasswordInput(attrs={'size': '40'}),
    label=_("Password"),
    min_length=8,
    error_messages={'required': 'Password is required.'},
  )
  password2 = forms.CharField(
    widget=forms.PasswordInput(attrs={'size': '40'}),
    label=_("Password confirmation"),
    min_length=8,
    error_messages={'required': 'Password confirmation is required.'},
  )
  date_of_birth = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}), 
    validators=[validate_date_of_birth], 
    error_messages={'required': 'Date of Birth is required'}
  )
  gender = forms.ChoiceField(
    choices=Author.GENDER_CHOICES, 
    required=True, 
    error_messages={'required': 'Gender is required'},
    widget=forms.RadioSelect()
  )
  state = forms.CharField(
    max_length=30,
    error_messages={'required': 'State is required'},
    widget=forms.TextInput(attrs={'size': '40'})
  )
  city = forms.CharField(
    max_length=30, 
    min_length=1, 
    error_messages={'required': 'City is required'},
    widget=forms.TextInput(attrs={'size': '40'})
  )
  
  class Meta:
    model = Author
    fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2', 'date_of_birth', 'gender', 'state', 'city']
    
  def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    user.date_of_birth = self.cleaned_data['date_of_birth']
    user.gender = self.cleaned_data['gender']
    user.state = self.cleaned_data['state']
    user.city = self.cleaned_data['city']
    
    if commit:
      user.save()
    return user

