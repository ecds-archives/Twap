import json
from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from twap.twitter.models import Tweet

class Command(BaseCommand):
    help = 'Dumps Tweets to a json file.'

    def handle(self, *args, **options):
        for month in range(1, 13):
            year = 2012
            if month < 9:
                year = 2011
            self._write_month(month, year)

    def _write_month(self, month, year):
        tweets = Tweet.objects.filter(created_at__month=month, created_at__year=year).prefetch_related()
        outfile = open('../twap_dump_%s_%s.json' % (month, year), 'wb')
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
            outfile.write("%s\n" % json.dumps(data))
