from django.shortcuts import render
from checkout.models import Payment
from checkout.forms import AddressForm
from authentication.models import UserProfile
from authentication.forms import PaymentForm
from feature_requests.models import FeatureRequest

# Create your views here.
def single_payment_checkout(request):
    """
    User can make a single payment
    """
    # user = request.user
    # user_subscribed = UserProfile.objects.get(user=user).subscribed
    # if user_subscribed == True:
    card_form = PaymentForm()
    address_form = AddressForm()
    return render(request, 'checkout.html', {"card_form": card_form,
                                             "address_form":address_form})