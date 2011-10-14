from django.core.management.base import BaseCommand
from optparse import make_option

try:
    from progressbar import ProgressBar, Bar, Percentage
except ImportError:
    ProgressBar = None


from twap.twitter.models import Tweet
from twap.entities import extract_named_entities, show_named_entities

class Command(BaseCommand):
    '''Extract named entities from the text of all tweets in the
database, using standard NLTK parts of speech & named entity
extraction, and aggregate counts across all tweets.

NOTE: requires NLTK; install progressbar to view percent complete'''
    help = __doc__
    option_list = BaseCommand.option_list + (
        make_option('--threshold', '-t',
            type='int',
            default=3,
            help='Only show entities that occur at least the specified '
                    'number of times [default: %default]'),
        )
    
    v_normal = 1
    def handle(self, verbosity=1, threshold=3, **options):

        total = Tweet.objects.count()
        if verbosity >= self.v_normal:
            print 'Extracting named entities from %d tweets' % total

        if ProgressBar:
            pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=total).start()
        else:
            pbar = None
        
        entities = None
        i = 0
        # iterate through all the tweets and analyze the text
        for t in Tweet.objects.all():
            if entities is None:
                # first time - generate new entity dictionary
                entities = extract_named_entities(t.text)
            else:
                # subsequent time: add counts to what has already been found
                entities =  extract_named_entities(t.text, entities)
            i += 1
            if pbar:
                pbar.update(i)
                
        pbar.finish()

        # display whatever was found
        show_named_entities(entities, threshold)

            
        
