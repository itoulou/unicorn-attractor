from django.conf.urls import url
from feature_requests.views import get_all_features, single_feature, create_or_edit_feature, delete_feature, vote, done

urlpatterns = [
        url(r'^all-features/', get_all_features, name="all_features"),
        url(r'^(?P<pk>\d+)/$', single_feature, name="view_feature"),
        url(r'^create-feature/$', create_or_edit_feature, name="create_feature"),
        url(r'^(?P<pk>\d+)/edit/$', create_or_edit_feature, name="edit_feature"),
        url(r'^(?P<pk>\d+)/delete/$', delete_feature, name="delete_feature"),
        url(r'^(?P<pk>\d+)/vote/$', vote, name="feature-vote"),
        url(r'^(?P<pk>\d+)/done/$', done, name="feature-done"),
    ]