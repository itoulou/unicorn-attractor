from django import forms
from checkout.models import SinglePayment


class singlePaymentForm(forms.Form):
    """
    Card details form
    """
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2017, 2036)]
    
    credit_card_number = forms.CharField(label="Card number", required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label="Year", choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)

class singlePaymentAddressForm(forms.ModelForm):
    class Meta:
        model = SinglePayment
        fields = ('full_name', 'phone_number', 'country', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county')