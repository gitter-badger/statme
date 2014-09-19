__author__ = 'noahlutz'

import tweepy
import sys

consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class HashtagListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.user.screen_name
        print 'location: ' + status.place.full_name
        for hashtag in status.entities['hashtags']:
            if hashtag['text'] == 'statme':
                print "Someone Tweeted #statme"

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered Error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

    def on_direct_message(self, status):
        print status


def main():
    listen = HashtagListener()
    stream = tweepy.Stream(auth, listen)

    print 'Stream Started...'
    stream.userstream()


if __name__ == '__main__':
    main()