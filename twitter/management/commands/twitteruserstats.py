from django.core.management.base import BaseCommand

from twap.twitter.streamreader import StreamHarvest
from twap.twitter.models import TwitterUser, Tweet

class Command(BaseCommand):
    help = 'dumps a simple csv file with tweet count for each user with some more userinfo.'
    args = ''

    def handle(self, **options):
        pass