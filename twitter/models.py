from django.db import models
from taggit.managers import TaggableManager

# Create your models here.

class Tweet(models.Model):

    text = models.CharField(max_length=141)
    screen_name = models.CharField(max_length=25)
    user_id = models.CharField(max_length=25)
    tweet_id = models.CharField(max_length=25)
    created_at = models.DateTimeField()

    tags = TaggableManager()

