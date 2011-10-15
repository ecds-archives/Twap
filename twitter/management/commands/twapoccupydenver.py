import datetime
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import Count

from twap.twitter.models import Tweet
from twap.csvunicode import UnicodeWriter

class Command(BaseCommand):
    help = 'Generates some special aggregation to analyze the occupydenver hashtag.'
    args = ''

    def handle(self, **options):
        """
        Prints out a count of number of tweets by screen_name for occupydenver.
        """
        # Get current datetime as a string to append to the file.
        # This should allow us to know when it was run and keep from overwriting.
        now = datetime.datetime.now().strftime('%Y%m%d%H%M')

        # Create a CSV fiile counting tweets by users
        f = open('ODhashtag_users_%s.txt' % now, 'wb')
	csv_writer = UnicodeWriter(f)
	csv_writer.writerow(['Screen Name', 'Num od Tweets'])

        tweets = Tweet.objects.filter(tags__name='occupydenver').order_by('twitter_user')        

	tweeters = defaultdict(int)

        for tweet in tweets:
	    tweeters[tweet.twitter_user.screen_name] += 1

        for user, count in tweeters.items():
            csv_writer.writerow([user.encode('utf-8'), '%s' % count])
 
