from django.contrib import admin
from twap.twitter.models import TwitterUser, Tweet, RawTweet

class TwitterUserAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'location')
    readonly_fields = ('screen_name', 'twitter_id', 'location')
    # not useful?
    #list_filter = ('location',)


admin.site.register(TwitterUser, TwitterUserAdmin)

class RawTweetInline(admin.StackedInline):
    model = RawTweet
    extra = 0
    readonly_fields = ('json',)

class TweetAdmin(admin.ModelAdmin):
    list_display = ('twitter_user', 'text', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('text', 'twitter_user', 'tweet_id', 'created_at', 'tags')

    inlines = [
        RawTweetInline,
        ]

admin.site.register(Tweet, TweetAdmin)
