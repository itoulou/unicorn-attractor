from django import forms
from feature_requests.models import FeatureRequest, Comment

class FeatureForm(forms.ModelForm):
    class Meta:
        model = FeatureRequest
        fields = ('title', 'content', 'tag', 'published_date')
        
class CommentForm(forms.ModelForm) :
    class Meta:
        model = Comment
        fields = ('content', 'tag')
        