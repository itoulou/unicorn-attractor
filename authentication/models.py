from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#  Create your models here.
class UserProfile(models.Model):
    """
    User profile
    """
    user = models.OneToOneField(User, null=True, blank=False)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
    
post_save.connect(create_profile, sender=User)    
    