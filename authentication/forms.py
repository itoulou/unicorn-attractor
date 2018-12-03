from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

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
    
    def clean_email(self):
        """
        Check to see if email is in the database already
        If it is then return an error else return the email
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address is already in use')
        return email
    
    def clean_password2(self):
        """
        Check to see if new user's passwords aren't none and
        check if password 1 == password 2
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # check if passwords are none
        if not password1 or not password2:
            raise forms.ValidationError('Please enter your password')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2