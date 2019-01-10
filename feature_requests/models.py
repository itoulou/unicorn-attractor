from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from authentication.models import UserProfile
from django.conf import settings

# Create your models here.
class FeatureRequest(models.Model):
    """
    A single Issue
    """
    author = models.ForeignKey('auth.User', null=True, blank=False)
    title = models.CharField(max_length=400)
    content = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now())
    total_votes = models.IntegerField(default=0)
    vote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="feature_votes")
    tag = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    done = models.BooleanField(default=False)
    comment_number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    A single comment object specific to issue
    """
    feature_request = models.ForeignKey(FeatureRequest)
    user_logged_in = models.ForeignKey('auth.User', null=True, blank=False, related_name="user_logged_in")
    image = models.ImageField(null=True, blank=True)
    content = models.TextField(max_length=100, null=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now())
    tag = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.feature_request
