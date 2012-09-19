import json, re
from pprint import pprint
from time import strptime
from datetime import datetime

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from twap.twitter.models import RawTweet, Tweet, TwitterUser

class Command(BaseCommand):
    help = 'Imports a JSON file dump of tweets into the database.'
    option_list = BaseCommand.option_list + (
            make_option('--filename',
                dest = 'importfilename',
                default = None,
                help='Name of JSON file with tweets to be imported.'
            ),
            make_option('-j', '--storejson',
                dest = 'storejson',
                action = 'store_true',
                default = False,
                help='Store the JSON in the database of the whole tweet.'
            )
        ) # add a silent option to skip raw input.

    def handle(self, *args, **options):
        filename = options.get('importfilename', None)
        if not filename:
            raise CommandError("Must provide a json filename to import.")
        try:
            data = json.load(open(filename, 'rb'))
        except IOError:
            raise CommandError("Unable to open file %s" % filename)

        for raw_tweet in data:
            tweet = self._handle_tweet(raw_tweet)
            if tweet and options.get('storejson'):
                jsontweet = RawTweet(
                    tweet = tweet,
                    json = json.dumps(raw_tweet)
                ).save()



    def _handle_tweet(self, tweet_data):
        """
        Bases raw tweet data into various django models.

        :param tweet_data:
        :return:
        """
        try:
            tweet = Tweet.objects.get(tweet_id=tweet_data['id'])
            return None # Already exists, skip it.
        except Tweet.DoesNotExist:
            tweet = Tweet(
                twitter_user = self._handle_user(tweet_data),
                created_at = self._parse_datetime(tweet_data['created_at']),
                text = tweet_data['text']
            )
            tweet.save()
            hashtags = self._parse_hashtags(tweet_data['text'])
            if hashtags:
                tweet.tags.add(*hashtags)
            return tweet

    def _parse_datetime(self, raw_date):
        """
        Parses a datetime object from a raw date string.

        :param raw_date:
        :return: datetime object
        """
        # has format 'Sun, 16 Sep 2012 21:11:41 +0000'
        fmt = '%a, %d %b %Y %H:%M:%S +0000'
        return datetime(*strptime(raw_date, fmt)[:6])

    def _handle_user(self, tweet_data):
        """
        Parses information about a Twitter User as needed.

        :param raw_user:
        :return: TwitterUser object
        """
        user, created = TwitterUser.objects.get_or_create(
            screen_name=tweet_data['from_user'],
            twitter_id=tweet_data['from_user_id'])
        return user

    def _parse_hashtags(self, tweet):
        """
        Parses Hashtags from the body of a tweet.
        :param tweet:
        :return: list of string hashtags.
        """
        # Used pattern from good stackoverflow reply
        # http://granades.com/2009/04/06/using-regular-expressions-to-match-twitter-users-and-hashtags/
        ptrn = '(\A|\s)#(\w+)'
        hashtags =[result[1].lower() for result in re.findall(ptrn, tweet)]
        return list(set(hashtags))

# Example of the tweet structure returned
#{u'created_at': u'Sun, 16 Sep 2012 21:11:41 +0000',
# u'from_user': u'EmoryCuts',
# u'from_user_id': 827732868,
# u'from_user_id_str': u'827732868',
# u'from_user_name': u'Emory Cuts',
# u'geo': None,
# u'id': 247442659155779585,
# u'id_str': u'247442659155779585',
# u'iso_language_code': u'en',
# u'metadata': {u'result_type': u'recent'},
# u'profile_image_url': u'http://a0.twimg.com/profile_images/2617508592/emory_cuts_normal.jpg',
# u'profile_image_url_https': u'https://si0.twimg.com/profile_images/2617508592/emory_cuts_normal.jpg',
# u'source': u'&lt;a href=&quot;http://twitter.com/&quot;&gt;web&lt;/a&gt;',
# u'text': u"The Quad at noon tomorrow. Bring everyone. We're plotting a path forward together. #EmoryCuts",
# u'to_user': None,
# u'to_user_id': 0,
# u'to_user_id_str': u'0',
# u'to_user_name': None}