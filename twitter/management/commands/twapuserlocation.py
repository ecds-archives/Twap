import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count

from twap.twitter.models import TwitterUser 

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
        f = open('userlocations_%s.csv' % now, 'wb')
        writer = UnicodeWriter(f)
        writer.writerow(['Name', 'Location', 'Tweet Count'])

        user_list = TwitterUser.objects.annotate(tweetcount=Count('tweet'))
        for user in user_list:
            if user.location:
                writer.writerow([user.screen_name, user.location, '%s' % user.tweetcount])
            
            
