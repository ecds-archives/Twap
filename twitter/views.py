from datetime import datetime, timedelta

from django.db.models import Count, Avg, Max
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from taggit.models import Tag
from twap.twitter.models import Tweet, TwitterUser


@login_required
def tag_counts(request, filter=None, exclude=None):
    # tags & number of time they have been used, optionally with a filter
    tag_counts = Tag.objects.distinct()
    if filter is not None:
        tag_counts = tag_counts.filter(name__icontains=filter)
    tag_counts = tag_counts.annotate(count=Count('taggit_taggeditem_items')).order_by('-count')
    return render(request, 'twitter/tags.html',
                  {'tags': tag_counts, 'max': tag_counts[0].count, 'filter': filter})


@login_required
def tweet_counts_by_user(request):
    # count tweets per user
    tweet_counts = TwitterUser.objects.annotate(count=Count('tweet')).order_by('-count')
    return render(request, 'twitter/tweets_per_user.html',
                  {'users': tweet_counts, 'max': tweet_counts[0].count})


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
    
