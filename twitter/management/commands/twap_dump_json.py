import json
from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from twap.twitter.models import Tweet

class Command(BaseCommand):
    help = 'Dumps Tweets to a json file.'

    def handle(self, *args, **options):
        tweets = Tweet.objects.all()
        big_tweets = []
        for tweet in tweets:
            data = {
                'tweet': tweet.text,
                'user': {'screenname': tweet.twitter_user.screen_name, 'location': tweet.twitter_user.location},
                'date_created': tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'geo': None,
                'coordinate': None,
                }
            geo = tweet.twittergeo_set.all()
            if geo:
                data['geo'] = {'lat': geo[0].latitude, 'long': geo[0].longitude}
            coord = tweet.twittercoordinate_set.all()
            if coord:
                data['coordinate'] = {'lat': coord[0].latitude, 'long': coord[0].longitude}
            big_tweets.append(data)
        with open('../twap_dump.json', 'wb') as f:
            for chunk in json.JSONEncoder().iterencode(big_tweets):
                f.write(chunk)
