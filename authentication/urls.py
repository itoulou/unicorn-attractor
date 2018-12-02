from django.conf.urls import url, include
from authentication.views import login

urlpatterns = [
        url(r'login/', login, name="login"),
    ]