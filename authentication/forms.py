from django import forms

class loginForm(forms.Form):
    """
    login form
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
 