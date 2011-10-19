import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count

from twap.twitter.models import TwitterGeo 

from twap.csvunicode import UnicodeWriter

class Command(BaseCommand):
    help = 'Dumps a simple csv file listing username and location'
    args = ''

    def handle(self, **options):
        """
        """
        # Get current datetime as a string to append to the file.
        # This should allow us to know when it was run and keep from overwriting.
        now = datetime.datetime.now().strftime('%Y%m%d%H%M')

        # Create a CSV fiile counting tweets by users
        f = open('usergeo_%s.csv' % now, 'wb')
        writer = UnicodeWriter(f)
        writer.writerow(['Username', 'Tweet', 'DateTweeted', 'Coordinates(lat/long)'])
	geotweets = TwitterGeo.objects.all()

        for geotweet in geotweets:
            tweetdate = geotweet.tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
	    location = "%s, %s" % (geotweet.latitude, geotweet.longitude)
	    writer.writerow([
		geotweet.tweet.twitter_user.screen_name,
		geotweet.tweet.text,
		tweetdate,
		location,
		])
