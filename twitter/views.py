from django.db.models import Count
from django.shortcuts import render
from taggit.models import Tag
from twap.twitter.models import Tweet, TwitterUser


def tag_counts(request, filter=None):
    # tags & number of time they have been used, optionally with a filter
    tag_counts = Tag.objects.distinct()
    if filter is not None:
        tag_counts = tag_counts.filter(name__icontains=filter)
    tag_counts = tag_counts.annotate(count=Count('taggit_taggeditem_items')).order_by('-count')
    return render(request, 'twitter/tags.html',
                  {'tags': tag_counts, 'max': tag_counts[0].count, 'filter': filter})

def tweet_counts(request):
    # count tweets per user
    tweet_counts = TwitterUser.objects.annotate(count=Count('tweet')).order_by('-count')
    return render(request, 'twitter/tweets_per_user.html',
                  {'users': tweet_counts, 'max': tweet_counts[0].count})
    
    
    
