from django.conf.urls import url, include
from authentication.views import login, register, logout, profile
from authentication import url_resets

urlpatterns = [
        url(r'^login/', login, name="login"),
        url(r'^logout/', logout, name="logout"),
        url(r'^register/', register, name="register"),
        url(r'^profile/', profile, name="profile"),
        url(r'^password-reset/', include(url_resets)),
    ]