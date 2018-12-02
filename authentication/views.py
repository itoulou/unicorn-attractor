from django.shortcuts import render
from authentication.forms import loginForm

# Create your views here.
def index(request):
    """
    render homepage page
    """
    return render(request, 'index.html')

def login(request):
    """
    user login page
    """
    login_form = loginForm()
    return render(request, 'login.html', {"login_form": login_form})