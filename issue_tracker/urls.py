from django.conf.urls import url
from issue_tracker.views import get_all_issues, single_issue, create_or_edit_issue, delete_issue, vote, done

urlpatterns = [
        url(r'^all-issues/', get_all_issues, name="all_issues"),
        url(r'^(?P<pk>\d+)/$', single_issue, name="view_issue"),
        url(r'^create-issue/$', create_or_edit_issue, name="create_issue"),
        url(r'^(?P<pk>\d+)/edit/$', create_or_edit_issue, name="edit_issue"),
        url(r'^(?P<pk>\d+)/delete/$', delete_issue, name="delete_issue"),
        url(r'^(?P<pk>\d+)/vote/$', vote, name="vote"),
        url(r'^(?P<pk>\d+)/done/$', done, name="done"),
    ]