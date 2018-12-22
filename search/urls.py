from django.conf.urls import url
from search.views import do_search_issues, do_search_features

urlpatterns = [
        url(r'^search-issues/$', do_search_issues, name="search-issues"),
        url(r'^search-features/$', do_search_features, name="search-features")
    ]