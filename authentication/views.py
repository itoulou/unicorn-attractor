from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
import stripe

from authentication.models import UserProfile
from authentication.forms import loginForm, registerForm, userProfileForm

from issue_tracker.models import Issue

from feature_requests.models import FeatureRequest

from subscription.models import SubscriptionPayment
from subscription.forms import subscriptionPaymentForm, subscriptionAddressForm

from unicorn_attractor.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
from boto3.session import Session
import boto3


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

def index(request):
    """
    render homepage page
    User can subscribe on the homepage in order to have unlimited feature
    votes (only if they're logged in)
    """
    if request.method == "POST":
        address_form = subscriptionAddressForm(request.POST)
        card_form = subscriptionPaymentForm(request.POST)
        
        if address_form.is_valid() and card_form.is_valid():
            subscription = address_form.save(commit=False)
            subscription.date = timezone.now()
            subscription.user = request.user
            subscription.save()
            
            try:
                customer = stripe.Charge.create(
                    amount = int(13.99 * 100),
                    currency = "GBP",
                    description = request.user.email,
                    card = card_form.cleaned_data['stripe_id'],
                    )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined")
                return redirect('index')
                
            if customer.paid:
                user_subscribed = UserProfile.objects.get(user=request.user)
                user_subscribed.subscribed = True
                user_subscribed.save()
                messages.error(request, "You have successfully subscribed")
                return redirect('index')
            else:
                messages.error(request, "Unable to take payment")
                return redirect('index')
        else:
            print(card_form.errors)
            messages.error(request, "We were unable to take a payment with that card")
            return redirect('index')
    else:
        if request.user.is_authenticated:
            user_subscribed = UserProfile.objects.get(user=request.user).subscribed
            logged_in = True
        else:
            user_subscribed = False
            logged_in = False
        card_form = subscriptionPaymentForm()
        address_form = subscriptionAddressForm()
    return render(request, 'index.html', {
                                         "user_subscribed": user_subscribed,
                                         "logged_in": logged_in,
                                         "card_form": card_form,
                                         "address_form":address_form,
                                         "publishable": settings.STRIPE_PUBLISHABLE,
                                         })
                                         
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
                user = str(user_logged_in.username.title())
                messages.success(request, "Logged in as " + user)
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
                user = str(user_registered.username.title())
                messages.success(request, "Welcome to Unicorn Attractor " + user)
                return redirect(reverse('index'))
            else:
                messages.error(request, 'A problem occured, please try to register again')
    else:    
        register_form = registerForm()
    return render(request, 'register.html', {"register_form": register_form})

@csrf_exempt
def profile(request):
    """
    user can access own profile page.
    If user has created issues/features, the they will display on their profile page
    user can upload a profile image or change it
    """
    try:
        if request.method == "POST":
            picture_form = request.FILES.get('image')
            profile = UserProfile.objects.get(user=request.user)
            profile.image = picture_form
            profile.save()
            picture_name = picture_form.name
            session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            s3 = session.resource('s3')
            s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=picture_name, Body=profile.image)
            return redirect('profile')
        
        else:
            picture_form =  userProfileForm()
    except:
        picture_form =  userProfileForm()
        
    all_issues = Issue.objects.filter(author=request.user).order_by("-published_date")
    issues_no_pages = Issue.objects.filter(author=request.user).order_by("-published_date")
    my_features_clicked = False
    paginator = Paginator(all_issues, 3)
    page = request.GET.get('page-issues')
    print(page)
    try:
        all_issues = paginator.page(page)
    except PageNotAnInteger:
        all_issues = paginator.page(1)
    except EmptyPage:
        all_issues = paginator.page(paginator.num_pages)
        paginator.page(paginator.num_pages) 
        
    
    all_features = FeatureRequest.objects.filter(author=request.user).order_by("-published_date")
    features_no_pages = FeatureRequest.objects.filter(author=request.user).order_by("-published_date")
    return render(request, "profile.html", {
                                        "all_issues": all_issues,
                                        "all_features": all_features,
                                        "issues": issues_no_pages,
                                        "features": features_no_pages,
                                        "picture_form": picture_form,
                                        "my_features_clicked": my_features_clicked,
                                        })
def remove_profile_img(request):
    """
    if user wishes to remove their image all together
    """
    profile = UserProfile.objects.get(user=request.user)
    if profile.image:
        UserProfile.objects.filter(user=request.user).update(image=None)
    return redirect('profile')

def cancel_subscription(request):
    """
    User can cancel their subscription
    """
    if request.method == "POST":
        user_subscription_payment = SubscriptionPayment.objects.get(user=request.user)
        user_subscription_payment.delete()
        
        user_subscribed = UserProfile.objects.get(user=request.user)
        user_subscribed.subscribed = False
        user_subscribed.save()
    return redirect(reverse('index'))

def user_features(request):
    """
    function that renders same page as profile function just with
    user's features rendered as opposed to the issues
    """
    all_features = FeatureRequest.objects.filter(author=request.user).order_by("-published_date")
    picture_form = userProfileForm()
    my_features_clicked = True
    paginator = Paginator(all_features, 3)
    page = request.GET.get('page-features')
    try:
        all_features= paginator.page(page)
    except PageNotAnInteger:
        all_features = paginator.page(1)
    except EmptyPage:
        all_features = paginator.page(paginator.num_pages)
        paginator.page(paginator.num_pages)
    return render(request, "profile.html", {
                                        "all_features": all_features,
                                        "picture_form": picture_form,
                                        "my_features_clicked": my_features_clicked,
                                        })    
