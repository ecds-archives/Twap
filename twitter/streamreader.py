import tweetstream
from datetime import datetime

from twap.twitter.models import Tweet, TwitterUser, TwitterCoordinate, TwitterGeo

class StreamHarvest(object):
    # Simple hack to grab twitter stuff.

    def __init__(self, username, password, track):

        self.username = username
        self.password = password
        self.track = track

    def listen(self):
        # slopppy way to keep it running and reconnecting if it hits a bump.
        # @NOTE you MUST kill the process to get this to stop because of this hack.  I know.... I suck, deal with it..
        while True:
            try:
                with tweetstream.FilterStream(self.username, self.password, track=self.track) as stream:
                    for tweet in stream:
                        try:
                            tuser = self.handle_user(tweet)
                            obj = Tweet(twitter_user=tuser)
                            obj.text = tweet["text"]
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
               print "Error on connection. Reconnecting."

    def hashtags(self, tweet):
        try:
            return [hashtag["text"].lower() for hashtag in tweet["entities"]["hashtags"]]
        except KeyError:
            pass

    def make_datetime(self, str_date):
        # Sat Sep 10 22:23:38 +0000 2011
        return datetime.strptime(str_date, "%a %b %d %H:%M:%S +0000 %Y")

    def handle_user(self, tweet):
        """
        Creates pulls the user information if needed to a seperate table.
        """
        tuser, created = TwitterUser.objects.get_or_create(screen_name=tweet["user"]["screen_name"])
        if created:
            tuser.twitter_id = tweet["user"]["id_str"]
            tuser.location = tweet["user"]["location"]
            tuser.save()
        return tuser

    def handle_geo(self, tweet, geo):
        """
        Grabs information about and from the geo field from the JSON return.

        :param tweet: a Tweet object
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
        """
        try:
            tg = TwitterCoordinate(tweet=tweet)
            tg.type = coord["type"]
            tg.latitude = coord["coordinates"][0]
            tg.longitude = coord["coordinates"][1]
            tg.save()
        except:
            print "Error handling coordinates" # Just keep going if I have an error.

