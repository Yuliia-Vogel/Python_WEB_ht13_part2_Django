from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, 
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
