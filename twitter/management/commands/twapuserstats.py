import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count

from twap.twitter.models import TwitterUser
from twap.csvunicode import UnicodeWriter

class Command(BaseCommand):
    help = 'dumps a simple csv file with tweet count for each user with some more userinfo.'
    args = ''

    def handle(self, **options):
        """
        This is helps write some basic aggregation data about users and their tweets.

        It should accomplish 2 things.

            *  Save a list of individual users screen_name, location, # of tweets
            * Save a list of # of tweets, # of users with those number of tweets.

            Sandemous Highschool Football Rules!
        """
        # Get current datetime as a string to append to the file.
        # This should allow us to know when it was run and keep from overwriting.
        now = datetime.datetime.now().strftime('%Y%m%d%H%M')

        # Create a CSV fiile counting tweets by users
        by_user = open('tweetcount_by_user_%s.csv' % now, 'wb')
        by_user_writer = UnicodeWriter(by_user)
        by_user_writer.writerow(['screen_name', 'location', 'total tweets'])

        tweet_counter = {}
        users = TwitterUser.objects.annotate(tweetcount=Count('tweet'))
        for user in users:
            by_user_writer.writerow([user.screen_name, "%s" % user.location, "%s" % user.tweetcount])
            if user.tweetcount in tweet_counter: #Doing it this way so I don't have to do another DB query.
                tweet_counter[user.tweetcount] += 1 # increment it if it exists
            else:
                tweet_counter[user.tweetcount] = 1 # init it if it doesn't exist
        by_user.close()

        # Create a CSV file aggregating users by their number of tweets
        total_tweets = open('by_total_tweets_%s.csv' % now, 'wb')
        total_tweets_writer = UnicodeWriter(total_tweets)
        total_tweets_writer.writerow(['Tweet Count', 'Number of Users'])
        for tweetcount, users in tweet_counter.items():
            total_tweets_writer.writerow(['%s' % tweetcount, '%s' % users])
        total_tweets.close()
            
            