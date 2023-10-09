from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser  # Import your custom user model

class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'gender', 'college']

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser