from django.db.models import Count, Avg, Max
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
    
    
def summary(request):
    total_tweets = Tweet.objects.count()
    total_users = TwitterUser.objects.count()
    retweets = Tweet.objects.filter(text__contains='RT').count()

    # maximum, average tweets per user
    user_max_avg = TwitterUser.objects.annotate(count=Count('tweet')).aggregate(avg=Avg('count'),
                                                                               max=Max('count'))
    return render(request, 'twitter/summary.html',
                  {'total_tweets': total_tweets, 'total_users': total_users,
                   'retweets': retweets,
                   'max_per_user': user_max_avg['max'],
                   'avg_per_user': user_max_avg['avg']})
    
