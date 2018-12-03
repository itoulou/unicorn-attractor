from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class loginForm(forms.Form):
    """
    login form for previous users
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
 
class registerForm(UserCreationForm):
    """
    Register form for new users
    """
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
       model = User
       fields = ['email', 'username', 'password1', 'password2']