from django.core.management.base import BaseCommand

from twap.twitter.streamreader import StreamHarvest
from twap.settings import TWITTER_USER, TWITTER_PASSWORD, SEARCHLIST

class Command(BaseCommand):
    help = 'Begins harvesting tweets with based on the seachlist criteria in localsettings.SEARCHLIST'
    args = ''

    def handle(self, **options):
        reader = StreamHarvest(TWITTER_USER, TWITTER_PASSWORD, SEARCHLIST)
        reader.listen()