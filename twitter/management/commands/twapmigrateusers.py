from django.core.management.base import BaseCommand

from twap.twitter.streamreader import StreamHarvest
from twap.twitter.models import TwitterUser, Tweet

class Command(BaseCommand):
    help = 'Migrates users from the old data scructure to the new.  Use to migration from v0.2 to v0.3'
    args = ''

    def handle(self, **options):
        tweets = Tweet.objects.all()
        for tweet in tweets:
            tuser, created = TwitterUser.objects.get_or_create(screen_name=tweet.screen_name)
            tuser.twitter_id = tweet.user_id
            tuser.save()
            tweet.twitter_user = tuser
            tweet.save()