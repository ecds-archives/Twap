from django.core.management.base import BaseCommand

from twap.twitter.streamreader import StreamHarvest
from twap.twitter.models import TwitterUser, Tweet

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
        users = TwitterUser.objects.all()
        for user in users:
            tweet_count = user.tweet_set.all().count()
            
            