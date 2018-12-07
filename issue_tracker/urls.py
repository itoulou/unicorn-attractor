from django.conf.urls import url
from issue_tracker.views import get_all_issues, single_issue, create_or_edit_issue

urlpatterns = [
        url(r'^all-issues/', get_all_issues, name="all_issues"),
        url(r'^(?P<pk>\d+)/$', single_issue, name="view_issue"),
        url(r'^create-issue/$', create_or_edit_issue, name="create_issue"),
        url(r'^(?P<pk>\d+)/edit/$', create_or_edit_issue, name="edit_issue"),
    ]