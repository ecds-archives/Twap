import json
from datetime import datetime, timedelta
from optparse import make_option
from os import path

from django.core.management.base import BaseCommand, CommandError

from twap.twitter.models import RawTweet

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
        )
    ) # add a silent option to skip raw input.

    def handle(self, *args, **options):
        raw_date = options.get('date', None)
        raw_purge = options.get('purge', False)

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

        # promp user if this file already exists.
        dumpfilename = 'tweetdump_%s.json' % raw_date

        path_feedback = """
        File %s already exists, if you continue all data in that file will be LOST!!!
        Type 'yes' if you wish to continue, or 'no' if you wish to abort.
        """ % dumpfilename
        if path.isfile(dumpfilename):
            if raw_input(path_feedback) != 'yes':
                raise CommandError('Aborting - File already exists!')

            # Dump list as json to file but raise error if it already exists.
        with open(dumpfilename, 'wb') as f:
            f.write(json.dumps(tweet_list)) # Write it all out to file..

        # If PURGE is true then ask the user again to confirm, then delete all raw tweets in range.
        raw_feedback = """Are you sure you wish to PURGE raw tweets from that database
            for %s? type 'yes' to confirm or 'no' to skip.""" % raw_date
        if raw_purge and raw_input(raw_feedback) == 'yes':
            rawtweet_list.delete()
            