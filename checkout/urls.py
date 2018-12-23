from django.conf.urls import url
from checkout.views import single_payment_checkout

urlpatterns = [
        url(r'^$', single_payment_checkout, name="single_payment_checkout"),
    ]