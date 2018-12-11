from django import forms
from issue_tracker.models import Issue, Comment

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'content', 'tag', 'published_date')
        
class CommentForm(forms.ModelForm) :
    class Meta:
        model = Comment
        fields = ('content', 'tag')
        