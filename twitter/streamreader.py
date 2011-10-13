import tweetstream
from datetime import datetime

from twap.twitter.models import Tweet

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
                            obj = Tweet()
                            obj.text = tweet["text"]
                            obj.user_id = tweet["user"]["id_str"]
                            obj.tweet_id = tweet["id_str"]
                            obj.screen_name = tweet["user"]["screen_name"]
                            obj.created_at = self.make_datetime(tweet["created_at"])
                            obj.save()
                            for tag in self.hashtags(tweet):
                                obj.tags.add(tag)
                            print "%s - %s" % (stream.count, self.hashtags(tweet))
                        except:
                            pass # Just keep going if error.
            except:
                pass # Keep it running, no matter what.

    def hashtags(self, tweet):
        try:
            return [hashtag["text"].lower() for hashtag in tweet["entities"]["hashtags"]]
        except KeyError:
            pass

    def make_datetime(self, str_date):
        # Sat Sep 10 22:23:38 +0000 2011
        return datetime.strptime(str_date, "%a %b %d %H:%M:%S +0000 %Y")

