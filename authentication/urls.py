from django.conf.urls import url, include
from authentication.views import login, register, logout, profile, remove_profile_img, cancel_subscription
from authentication import url_reset, url_profile

urlpatterns = [
        url(r'^login/', login, name="login"),
        url(r'^logout/', logout, name="logout"),
        url(r'^register/', register, name="register"),
        url(r'cancel-subscription/', cancel_subscription, name="cancel_subscription"),
        url(r'^profile/', include(url_profile)),
        url(r'^remove-profile-image/', remove_profile_img, name="remove_profile_img"),
        url(r'^password-reset/', include(url_reset)),
    ]