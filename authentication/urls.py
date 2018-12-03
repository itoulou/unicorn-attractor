from django.conf.urls import url, include
from authentication.views import login, register, logout

urlpatterns = [
        url(r'login/', login, name="login"),
        url(r'logout/', logout, name="logout"),
        url(r'register/', register, name="register"),
    ]