from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from issue_tracker.models import Issue
from issue_tracker.forms import IssueForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def get_all_issues(request):
    """
    Create a view that will return all the Issues from all Users
    that were published prior to now and render them all to issues.html
    template
    """ 
    all_issues = Issue.objects.filter(published_date__lte=timezone.now()).order_by("-votes")
    return render(request, "issues.html", {"all_issues": all_issues})
    
def single_issue(request, pk):
    """
    Create a view that returns an issue based on the issue id (pk)
    and render it to viewissue.html or return 404 error if issue is not found
    """
    issue = get_object_or_404(Issue, pk=pk)
    return render(request, "viewissue.html", {"issue": issue})

@login_required    
def create_or_edit_issue(request, pk=None):
    """
    Create a view that allows the user to create or edit
    an issue depending if the issue ID is null or not
    """
    issue = get_object_or_404(Issue, pk=pk) if pk else None
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():
            issue = form.save()
            issue.author = request.user
            issue.save()
            return redirect(single_issue, issue.pk)
    else:
        form = IssueForm(instance=issue)
    return render(request, "issueform.html", {"form": form})    
    

def delete_issue(request, pk):
    """
    author of issue can delete their posted issue
    """
    issue = get_object_or_404(Issue, pk=pk)
    issue.delete()
    
    return redirect(get_all_issues)