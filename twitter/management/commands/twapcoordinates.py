import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count

from twap.twitter.models import TwitterCoordinate

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
        f = open('tweetcoordinates_%s.csv' % now, 'wb')
        writer = UnicodeWriter(f)
        writer.writerow(['Username', 'Tweet', 'TweetID', 'DateTweeted', 'Coordinates(lat/long)'])
	coordtweets = TwitterCoordinate.objects.all()

        for coordtweet in coordtweets:
            tweetdate = coordtweet.tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
	    location = "%s, %s" % (coordtweet.longitude, coordtweet.latitude)
	    writer.writerow([
		coordtweet.tweet.twitter_user.screen_name,
		coordtweet.tweet.text,
		coordtweet.tweet.tweet_id,
		tweetdate,
		location,
		])
