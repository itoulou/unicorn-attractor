from django import forms
from issue_tracker.models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'content', 'image', 'tag', 'published_date')
        