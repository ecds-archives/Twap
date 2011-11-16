from django.db import models
from taggit.managers import TaggableManager

# These models are created to capture some information from the Twitter streaming
# API data return detailed at
# https://dev.twitter.com/docs/api/1/get/statuses/show/%3Aid
# the corresponding return field from the JSON return is noted by the appropriate field.

class TwitterUser(models.Model):
    """
    User information from individual tweets.
    """
    screen_name = models.CharField(max_length=25, db_index=True) # user.screen_name
    twitter_id = models.CharField(max_length=25) # user.id_str
    location = models.CharField(max_length=50, null=True) # user.location

    def __unicode__(self):
        return '@%s' % self.screen_name

class Tweet(models.Model):
    """
    Basic model for data on invidual tweets.
    """

    text = models.CharField(max_length=160) # text
    twitter_user = models.ForeignKey(TwitterUser)
    tweet_id = models.CharField(max_length=25) # id_str
    created_at = models.DateTimeField(db_index=True) # created_at

    tags = TaggableManager()

    class Meta:
        ordering = ['-created_at']
        get_latest_by = 'created_at'

class TwitterGeo(models.Model):
    """
    Geo coordinate information entered about individual tweets.

    Going with char fields on the lat/longs for expediency.
    """
    tweet = models.ForeignKey(Tweet)
    type = models.CharField(max_length=25) # geo.type
    latitude = models.CharField(max_length=25) # geo.coordinates[0]
    longitude = models.CharField(max_length=25) # geo.coordinates[1]

class TwitterCoordinate(models.Model):
    """
    Captures data from the coordinates filed in the twitter JSON return.
    """
    tweet = models.ForeignKey(Tweet)
    type = models.CharField(max_length=25) # coordinates.type
    latitude = models.CharField(max_length=25) # coordinates.coordinates[0]
    longitude = models.CharField(max_length=25) # coordinates.coordinates[1]

