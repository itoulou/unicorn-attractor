from django import forms
from checkout.models import Payment


class AddressForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('full_name', 'phone_number', 'country', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county')