import math
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from authentication.models import UserProfile
from feature_requests.models import FeatureRequest, Comment
from feature_requests.forms import FeatureForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def get_all_features(request):
    """
    Create a view that will return all the feature requests from all Users
    that were published prior to now and render them all to features.html
    template
    """ 
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
    return render(request, "features.html", {"all_features": all_features,
                                        #   "comments": comments,
                                        #   "comment_count": comment_count,
                                            })

def single_feature(request, pk):
    """
    Create a view that returns an feature based on the feature id (pk)
    and render it to viewfeature.html or return 404 error if feature is not found
    """
    feature = get_object_or_404(FeatureRequest, pk=pk)
    comments = Comment.objects.filter(feature_request=feature).order_by("-id")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(feature_request=feature,
                                             user_logged_in=request.user,
                                             content=content)
            comment.save()
            feature.comment_number += 1
            feature.save()
            return redirect(single_feature, feature.pk)
    else:
        comment_form = CommentForm()
    
    author_image = []
    try:
        image = UserProfile.objects.get(user=feature.author).image
        author_image.append({"image": image})
    except:
        author_image.append({"image": None})
    
    comments_with_images = []
    for comment in comments:
        try:
            image = UserProfile.objects.get(user=comment.user_logged_in).image
            comments_with_images.append({"image": image, "comment": comment})
        except:
            comments_with_images.append({"image": None, "comment": comment})
    comment_count = comments.count()
    first_three_comments = comments_with_images[:3]
    return render(request, "viewfeature.html", {"author_image": author_image,
                                              "feature": feature,
                                              "comments_with_images": comments_with_images,
                                              "comment_count": comment_count,
                                              "comment_form": comment_form,
                                              "first_three_comments": first_three_comments,
                                              })

def create_or_edit_feature(request, pk=None):
    """
    Create a view that allows the user to create or edit
    an feature depending if the feature ID is null or not
    """
    feature = get_object_or_404(FeatureRequest, pk=pk) if pk else None
    if request.method == "POST":
        form = FeatureForm(request.POST, request.FILES, instance=feature)
        if form.is_valid():
            feature = form.save()
            feature.author = request.user
            feature.save()
            return redirect(single_feature, feature.pk)
    else:
        form = FeatureForm(instance=feature)
    return render(request, "featureform.html", {"form": form})

def delete_feature(request, pk):
    """
    author of feature can delete their posted feature
    """
    feature = get_object_or_404(FeatureRequest, pk=pk)
    feature.delete()
    
    return redirect(get_all_features)

@csrf_exempt   
def vote(request, pk):
    """
    User in session can vote for an feature if it's helped them
    """
    feature = get_object_or_404(FeatureRequest, pk=pk)
    user = request.user
    user_subscribed = UserProfile.objects.get(user=user).subscribed
    vote_number = feature.total_votes
    # print(user_subscribed)
    if user_subscribed:
        if user.is_authenticated():
            if user in feature.vote.all():
                feature.vote.remove(user)
                up_vote = False
                vote_number -= 1
            else:
                feature.vote.add(user)
                up_vote = True
                vote_number += 1
        feature.total_votes = feature.vote.count()
        feature.save()
        print(up_vote)
        print(vote_number)
        data = {
            "up_vote": up_vote,
            "vote_number": vote_number
        }
        return JsonResponse(data)
        
    
        

@csrf_exempt
def done(request, pk):
    """
    Author of feature can click button if 'admin' has fixed the feature in 
    their opinon
    """
    feature = get_object_or_404(FeatureRequest, pk=pk)
    data = {
        "is_done": feature.done
    }
    is_done = request.POST.get('is_done')
    if request.method == "POST":
        if str(is_done) == "true":
            feature.done = True;
            feature.save()
        else:
            feature.done = False;
            feature.save()
    return JsonResponse(data)

    
    