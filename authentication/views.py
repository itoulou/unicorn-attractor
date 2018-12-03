from django.shortcuts import render, reverse, redirect
from django.contrib import auth, messages
from authentication.forms import loginForm, registerForm
from django.contrib.auth.decorators import login_required

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
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = loginForm(request.POST)
        
        if login_form.is_valid():
            user_logged_in = auth.authenticate(username=request.POST['username'],
                                               password=request.POST['password'])
            
            if user_logged_in:
                auth.login(user=user_logged_in, request=request)
                messages.success(request, "Logged in as ")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "username or password is incorrect")
    else:
        login_form = loginForm
    return render(request, 'login.html', {"login_form": login_form})

def logout(request):
    """
    user logout
    """
    auth.logout(request)
    messages.success(request, "Thank you for using Unicorn Attractor")
    return redirect(reverse('index'))
    

def register(request):
    """
    register user page
    """
    register_form = registerForm()
    return render(request, 'register.html', {"register_form": register_form})