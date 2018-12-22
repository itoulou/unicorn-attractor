from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from issue_tracker.models import Issue
from feature_requests.models import FeatureRequest


# Create your views here.
def do_search_issues(request):
    """
    Search for an issue
    """
    all_issues = Issue.objects.filter(title__icontains=request.GET.get('issue-search', False))
    if not all_issues:
        messages.error(request, "Unfortunately your search didn't find anything")
        all_issues = Issue.objects.filter(published_date__lte=timezone.now()).order_by("-total_votes")
        paginator = Paginator(all_issues, 2)
        page = request.GET.get('page-issues')
        try:
            all_issues = paginator.page(page)
        except PageNotAnInteger:
            all_issues = paginator.page(1)
        except EmptyPage:
            all_issues = paginator.page(paginator.num_pages)
        paginator.page(paginator.num_pages)  
    return render(request, 'issues.html', {"all_issues": all_issues})

def do_search_features(request):
    """
    Search for a request
    """
    all_features = FeatureRequest.objects.filter(title__icontains=request.GET.get('feature-search', False))
    if not all_features:
        messages.error(request, "Unfortunately your search didn't find anything")
        all_features = FeatureRequest.objects.filter(published_date__lte=timezone.now()).order_by("-total_votes")
        paginator = Paginator(all_features, 2)
        page = request.GET.get('page-features')
        try:
            all_features = paginator.page(page)
        except PageNotAnInteger:
            all_features = paginator.page(1)
        except EmptyPage:
            all_features = paginator.page(paginator.num_pages)
        paginator.page(paginator.num_pages)  
    return render(request, 'features.html', {"all_features": all_features})    