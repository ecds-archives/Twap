import json
from datetime import datetime, timedelta
from optparse import make_option
from os import path

from django.core.management.base import BaseCommand, CommandError

from twap.twitter.models import RawTweet
from twap.settings import TWAP_SAVE_DIR

class Command(BaseCommand):
    args = '<date>'
    help = 'Writes all tweets for <date> to JSON outputs to a file.'
    option_list = BaseCommand.option_list + (
        make_option('-d', '--date',
            dest='date',
            default=False,
            help='Write tweets to json file for day <date> YYYY-MM-DD'
        ),
        make_option('-p', '--purge',
            action='store_true',
            dest='purge',
            default=False,
            help='aftering wrting to file delete raw tweets from that database (saves space)'
        ),
        make_option('--directory',
            dest='directory',
            default=TWAP_SAVE_DIR,
            help='Directory to write archive files, defaults to value of TWAP_SAVE_DIR in settings if not supplied.'
        )
    ) # add a silent option to skip raw input.

    def handle(self, *args, **options):
        raw_date = options.get('date', None)
        raw_purge = options.get('purge', False)

        filepath = self._make_dumpfilename(options.get('directory', None), raw_date)

        date_format = "%Y-%m-%d"

        try:
            start = datetime.strptime(raw_date, date_format)
            end = start + timedelta(seconds=86399) # seconds in a day minus 1
        except ValueError:
            raise CommandError("Improper date format '%s' please use YYYY-MM-DD" % raw_date)

        # Get our rawtweets in the daterange
        rawtweet_list =  RawTweet.objects.filter(tweet__created_at__range=(start, end))

        # Convert to python dicts and load into a list.
        tweet_list = [json.loads(tweet.json) for tweet in rawtweet_list]

        # Dump list as json to file but raise error if it already exists.
        with open(filepath, 'wb') as f:
            f.write(json.dumps(tweet_list)) # Write it all out to file..

    def _check_directory(self, dir):
        """
        Checks that the supplied directory exists or raises a command error if not.
        """
        if not path.isdir(dir):
            raise CommandError('Archive directory %s is not a valid directory!' % dir)
        return dir # return it if the directory is valid.

    def _make_dumpfilename(self, raw_dir, raw_date):
        """
        Creates the name of the dumpfile and if it already exists creates a numbered version of that filename instead.
        """
        base_name = 'tweetdump_%s' % raw_date
        archive_dir = "%s/" % self._check_directory(raw_dir)
        filepath = '%s%s.json' % (archive_dir, base_name)
        i = 1
        while path.isfile(filepath):
            base_name = 'tweetdump_%s_%s' % (raw_date, i)
            filepath = '%s%s.json' % (archive_dir, base_name)
            i += 1
        return filepath
            