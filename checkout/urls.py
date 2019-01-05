from django.conf.urls import url
from checkout.views import single_payment_checkout#, get_feature_id

urlpatterns = [
        # url(r'^$', single_payment_checkout, name="single_payment_checkout"),
        url(r'^(?P<pk>\d+)/$', single_payment_checkout, name="single_payment_checkout"),
    ]