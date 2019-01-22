from django.conf.urls import url
from authentication.views import profile, user_features

urlpatterns = [
        url(r'^$', profile, name="profile"),
        # url(r'^my-issues/', user_issues, name="user_issues"),
        url(r'^my-features/', user_features, name="user_features"),
    ]