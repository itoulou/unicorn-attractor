from django.contrib import admin
from feature_requests.models import FeatureRequest, Comment

# Register your models here.
admin.site.register(FeatureRequest)
admin.site.register(Comment)
