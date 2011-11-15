import operator
from datetime import datetime, timedelta

from django.db.models import Count, Avg, Max, Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from taggit.models import Tag
from twap.twitter.models import Tweet, TwitterUser
from twap.twitter.forms import TagForm, UserSearchForm


@login_required
def tag_counts(request, filter=None, exclude=None):
    # tags & number of time they have been used, optionally with a filter
    tag_counts = Tag.objects.distinct()
    if filter is not None:
        tag_counts = tag_counts.filter(name__icontains=filter)
    tag_counts = tag_counts.annotate(count=Count('taggit_taggeditem_items')).order_by('-count')
    return render(request, 'twitter/tag_list.html',
                  {'tags': tag_counts, 'max': tag_counts[0].count, 'filter': filter})


@login_required
def tag_list(request):
    """
    Shows a list of tags ordered by their use count.  Includes the ability to
    provide an search filter or exclude filter on tags.
    """
    tag_list = Tag.objects.distinct()
    title = "Hashtags used"

    form = TagForm(request.POST or None)
    form_action = reverse('twitter:tag_list')
    if form.is_valid():
        exclude_cleaned = form.cleaned_data['exclude'].strip()
        if exclude_cleaned:
            exclude_words = [word.strip() for word in exclude_cleaned.split(',')] # conpensates if user submits spaces as a search.
            for word in exclude_words:
                tag_list = tag_list.exclude(name__icontains=word.strip())
        search_cleaned = form.cleaned_data['search'].strip()
        if search_cleaned: # Was going to do custom is_valid but this is more explicit.
            search_words = [word.strip() for word in search_cleaned.split(',')]
            if search_words:
                q_list = Q()
                for word in search_words:
                    q_list.add(Q(name__icontains=word.strip()), Q.OR)
                tag_list = tag_list.filter(q_list)

    tag_list = tag_list.annotate(count=Count('taggit_taggeditem_items')).order_by('-count')

    return render(request, 'twitter/tag_list.html', {
        'tag_list': tag_list,
        'max': tag_list.count(),
        'form': form,
        'title': title,
        'form_action': form_action,
        'form_legend': 'Filter Hashtags',
    })

@login_required
def tag_view(request, tag_slug):
    """
    View details on a specific hashtag.

    :param tag_slug:  Slug for the tag desired.
    """
    tag = get_object_or_404(Tag, slug=tag_slug) # Tag object itself
    # Num of users using this tag.
    # Num of tweets tagged with this.
    tweet_list = Tweet.objects.filter(tags__slug=tag_slug)
    tweet_count = tweet_list.count()
    user_list = TwitterUser.objects.filter(tweet__tags=tag).annotate(count=Count('tweet')).aggregate(avg=Avg('count'),
                                                                               max=Max('count'))
    return render(request, 'tag_detail.html', {
        'tag': tag,
        'tweet_list': tweet_list,
        'tweet_count': tweet_count,
    })

@login_required
def user_list(request):
    """
    Lists users and the number of tweets archived here and provides basic
    searching and filtering by username.
    """
    title = 'Twitter users and tweet count'
    users = TwitterUser.objects.all()
    form = UserSearchForm(request.POST or None)
    form_action = reverse('twitter:user_list')
    if form.is_valid():
        search = form.cleaned_data['search']
        users = users.filter(screen_name__icontains=search)
    users = users.annotate(count=Count('tweet')).order_by('-count')
    return render(request, 'twitter/user_list.html', {
        'form': form,
        'form_action': form_action,
        'form_legend': 'Search Screen Names',
        'users': users,
        'max': users[0].count,
        'title': title,
    })

@login_required
def user_view(request, screen_name):
    """
    Pulls back some information on and individual twitter username.

    :param screen_name: twitter username
    """
    user = Twitter.objects.get(screen_name=screen_name)
    tweets = Tweet.objects.filter(twitter_user=user)
    return render(request, 'twitter/user_view.html', {
        'user': user,
        'tweet_count': tweets.count(),
        'tweet_list': tweets,
    })

@login_required
def summary(request):
    tweet_count = Tweet.objects.count()
    user_count = TwitterUser.objects.count()
    tag_count = Tag.objects.count()

    now = datetime.now()
    then = now - timedelta(hours=2)
    volume_count = Tweet.objects.filter(created_at__range=(then, now)).count()

    # maximum, average tweets per user
    user_max_avg = TwitterUser.objects.annotate(count=Count('tweet')).aggregate(avg=Avg('count'),
                                                                               max=Max('count'))
    return render(request, 'twitter/summary.html',
                  {'tweet_count': tweet_count,
                   'user_count': user_count,
                   'tag_count': tag_count,
                   'volume_count': volume_count,
                   'max_per_user': user_max_avg['max'],
                   'avg_per_user': user_max_avg['avg']})
    
