import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count

from taggit.models import Tag

from twap.csvunicode import UnicodeWriter

class Command(BaseCommand):
    help = 'Dumps a simple csv file listing the hashtag and number of occurances.'
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
        f = open('hashtagcount_%s.csv' % now, 'wb')
        writer = UnicodeWriter(f)
        writer.writerow(['HashTag', 'Count'])

        tag_list = Tag.objects.annotate(count=Count('taggit_taggeditem_items')).order_by('-count')
        for tag in tag_list:
            writer.writerow([tag.name, '%s' % tag.count])
            
            