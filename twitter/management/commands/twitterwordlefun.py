import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count

from taggit.models import Tag

class Command(BaseCommand):
    help = 'Dumps text file of most used hashtags for a wordle file. Excludes occupy'
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
        f = open('wordlehashtags_%s.txt' % now, 'wb')

        tag_list = Tag.objects.exclude(name__contains=("occupy")).annotate(count=Count('taggit_taggeditem_items')).order_by('-count')
        for tag in tag_list[:200]:
            f.write('%s:%s\n' % (tag.name.encode("utf-8"), tag.count))
        f.close()
   
	f = open('occupy_wordle_%s.txt' % now, 'wb') 
	occupy_list = Tag.objects.filter(name__contains=("occupy")).annotate(count=Count('taggit_taggeditem_items')).order_by('-count')
	for tag in occupy_list[:200]:
	    f.write('%s:%s\n' % (tag.name.encode("utf-8"), tag.count))
        f.close()            
