from django.contrib import admin
from issue_tracker.models import Issue, Comment

# Register your models here.
admin.site.register(Issue)
admin.site.register(Comment)

