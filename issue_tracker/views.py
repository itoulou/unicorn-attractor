from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from issue_tracker.models import Issue, Comment
from issue_tracker.forms import IssueForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile


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
    comments = Comment.objects.filter(issue=issue).order_by("-id")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(issue=issue,
                                             user_logged_in=request.user,
                                             content=content)
            comment.save()
            return redirect(single_issue, issue.pk)
        
    else:
        comment_form = CommentForm()
    
    if request.method == "POST" and 'votes' in request.POST:
        issue.votes += 1
        issue.save()
        
    comments_with_images = []
    for comment in comments:
        try:
            image = UserProfile.objects.get(user=comment.user_logged_in).image
            comments_with_images.append({"image": image, "comment": comment})
        except:
            comments_with_images.append({"image": None, "comment": comment})
    comment_count = comments.count()
    # import pdb;pdb.set_trace()
    return render(request, "viewissue.html", {"issue": issue,
                                              "comments_with_images": comments_with_images,
                                              "comment_count": comment_count,
                                              "comment_form": comment_form,
                                              })

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

def votes(request, pk):
    """
    User can vote on the issue
    """
    
        