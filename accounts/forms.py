from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=13, required=True, label='Phone Number')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

class CustomAuthForm(AuthenticationForm):

    error_messages = {
        'invalid_login': "Invalid username or password."
    }

