from django.shortcuts import render, get_object_or_404, redirect, reverse
from checkout.models import SinglePayment, SinglePaymentLineItem
from checkout.forms import singlePaymentAddressForm, singlePaymentForm
from authentication.models import UserProfile
from feature_requests.models import FeatureRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET


@login_required
def single_payment_checkout(request, pk):
    """
    User can make a single payment
    """
    print(pk)
    if request.method == "POST":
        address_form = singlePaymentAddressForm(request.POST)
        card_form = singlePaymentForm(request.POST)
        
        if address_form.is_valid() and card_form.is_valid():
            order = address_form.save(commit=False)
            order.date = timezone.now()
            order.save()
           
            feature_request = FeatureRequest.objects.get(id=pk)
            single_payment_line_item = SinglePaymentLineItem(
                single_payment = order,
                feature_request=feature_request
                )
            single_payment_line_item.save()
            
            try:
                customer = stripe.Charge.create(
                    amount = int(5.99 * 100),
                    currency = "GBP",
                    description = request.user.email,
                    card = card_form.cleaned_data['stripe_id'],
                    )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined")
                
            if customer.paid:
                messages.error(request, "You have successfully paid")
                return redirect('view_feature', pk)
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(card_form.errors)
            messages.error(request, "We were unable to take a payment with that card")
    else:
        card_form = singlePaymentForm()
        address_form = singlePaymentAddressForm()
    return render(request, 'checkout.html', {"card_form": card_form,
                                             "address_form":address_form,
                                             "publishable": settings.STRIPE_PUBLISHABLE,
                                             "pk": pk})