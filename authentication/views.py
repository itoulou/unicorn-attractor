from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import auth, messages
from authentication.forms import loginForm, registerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authentication.models import UserProfile
from authentication.forms import userProfileForm
from issue_tracker.models import Issue
from feature_requests.models import FeatureRequest
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


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
        login_form = loginForm()
    return render(request, 'login.html', {"login_form": login_form})

@login_required
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
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            user_registered = auth.authenticate(username=request.POST['username'],
                                               password=request.POST['password1'])
            if user_registered:
                auth.login(user=user_registered, request=request)
                messages.success(request, "Welcome to Unicorn Attractor ")
                return redirect(reverse('index'))
            else:
                messages.error(request, 'A problem occured, please try to register again')
    else:    
        register_form = registerForm()
        # profile_picture_form = profilePictureForm()
    return render(request, 'register.html', {"register_form": register_form})

@csrf_exempt
def profile(request, pk=None):
    """
    user can access own profile page.
    If user has created issues, the issues will display on their profile page
    """
    picture_form = userProfileForm(request.FILES)
    all_issues = Issue.objects.filter(author=request.user).order_by("-published_date")
    paginator = Paginator(all_issues, 2)
    page = request.GET.get('page-issues')
    # page = request.POST.get('page-issues')
    print(page)
    try:
        all_issues = paginator.page(page)
        print(all_issues)
    except PageNotAnInteger:
        all_issues = paginator.page(1)
    except EmptyPage:
        all_issues = paginator.page(paginator.num_pages)
        paginator.page(paginator.num_pages) 
    
    all_features = FeatureRequest.objects.filter(author=request.user).order_by("-published_date")
    paginator = Paginator(all_features, 2)
    page = request.GET.get('page-features')
    try:
        all_features= paginator.page(page)
        print(all_issues)
    except PageNotAnInteger:
        all_features = paginator.page(1)
    except EmptyPage:
        all_features = paginator.page(paginator.num_pages)
        paginator.page(paginator.num_pages)
        
    return render(request, "profile.html", {"all_issues": all_issues,
                                        "all_features": all_features,
                                        "picture_form": picture_form,
                                        })

    # else:
    #     picture_form = userProfileForm(request.FILES)
    # return render(request, 'profile.html', {"picture_form": picture_form})

