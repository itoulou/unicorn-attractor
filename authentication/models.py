from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from checkout.models import Payment

#  Create your models here.
class UserProfile(models.Model):
    """
    User profile
    """
    user = models.OneToOneField(User, null=True, blank=False)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    subscribed = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50, blank=False, null=True)
    phone_number = models.CharField(max_length=20, blank=False, null=True)
    country = models.CharField(max_length=40, blank=False, null=True)
    postcode = models.CharField(max_length=15, blank=False, null=True)
    town_or_city = models.CharField(max_length=30, blank=False, null=True)
    street_address1 = models.CharField(max_length=40, blank=False, null=True)
    street_address2 = models.CharField(max_length=40, blank=False, null=True)
    county = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(null=True)
    
    def __str__(self):
        return self.user.username
    
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
    
post_save.connect(create_profile, sender=User) 