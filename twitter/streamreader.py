import time
from datetime import datetime

import tweetstream

from twap.twitter.models import Tweet, TwitterUser, TwitterCoordinate, TwitterGeo

class StreamHarvest(object):
    # Simple hack to grab twitter stuff.

    def __init__(self, username, password, track):
        """
        Acts on the twitter streaming api to query for tweets fitting a particular track filter.

        :param username:  Twitter username to query the API
        :param password:  Twitter users password to query API
        :param track: list of strings to filter tweets for.
        """

        self.username = username
        self.password = password
        self.track = track

    def listen(self):
        # slopppy way to keep it running and reconnecting if it hits a bump.
        # @NOTE you MUST kill the process to get this to stop because of this hack.  I know.... I suck, deal with it..
        while True:  # Keeps it going and reconnecting if it crashes.  See 'sloppy' above.
            try:
                with tweetstream.FilterStream(self.username, self.password, track=self.track) as stream:
                    for tweet in stream:
                        try:
                            tuser = self.handle_user(tweet)
                            obj = Tweet(twitter_user=tuser)
                            obj.text = tweet["text"].encode('utf-8')
                            obj.tweet_id = tweet["id_str"]
                            obj.created_at = self.make_datetime(tweet["created_at"])
                            obj.save()
                            for tag in self.hashtags(tweet):
                                obj.tags.add(tag)
                            if tweet["geo"]:
                                self.handle_geo(obj, tweet["geo"])
                            if tweet["coordinates"]:
                                self.handle_coordinates(obj, tweet["coordinates"])
                            print "%s - %s" % (stream.count, self.hashtags(tweet))
                        except:
                            print "Error Reading Record, skipping."
            except:
                print "Error on connection. Attempting reconnect in 30 seconds."
                time.sleep(30)

    def hashtags(self, tweet):
        """
        Turns hashtags into a list so it's easier to act on later.
        """
        try:
            return [hashtag["text"].encode('utf-8').lower() for hashtag in tweet["entities"]["hashtags"]]
        except KeyError:
            pass

    def make_datetime(self, str_date):
        """
        Convienence method to turn the twittter date string into a python datetime object.

        :param str_date:  String to convernt to a datetime object.
        """
        # Sat Sep 10 22:23:38 +0000 2011
        return datetime.strptime(str_date, "%a %b %d %H:%M:%S +0000 %Y")

    def handle_user(self, tweet):
        """
        User information from tweets are split into a seperate table for querying and to save
        tablespace.

        :param tweet:  raw tweet data
        """
        tuser, created = TwitterUser.objects.get_or_create(screen_name=tweet["user"]["screen_name"].encode('utf-8'))
        if created:
            tuser.twitter_id = tweet["user"]["id_str"]
            if tweet['user']['location']:
                tuser.location = tweet["user"]["location"].encode('utf-8')
            tuser.save()
        return tuser

    def handle_geo(self, tweet, geo):
        """
        Grabs information about and from the geo field from the JSON return.

        :param tweet: a Tweet Model Object
        :param geo:  data from the raw tweet geo field.
        """
        try:
            tg = TwitterGeo(tweet=tweet)
            tg.type = geo["type"]
            tg.latitude = geo["coordinates"][0]
            tg.longitude = geo["coordinates"][1]
            tg.save()
        except:
            print "Error handling geo" # Just keep going if I have an error.

    def handle_coordinates(self, tweet, coord):
        """
        Grabs information about and from the coordinates field from the JSON return.

        :param tweet:  a Tweet Model Object
        :param coord:  data from the raw tweet coordinates field.
        """
        try:
            tg = TwitterCoordinate(tweet=tweet)
            tg.type = coord["type"]
            tg.latitude = coord["coordinates"][0]
            tg.longitude = coord["coordinates"][1]
            tg.save()
        except:
            print "Error handling coordinates" # Just keep going if I have an error.

