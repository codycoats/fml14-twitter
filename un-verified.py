import os
import tweepy
import json
from config import Config
from tweepy.parsers import RawParser
import cPickle as pickle

keys = file('configu.cfg')
cfg = Config(keys)

consumer_key= cfg.consumer_key
consumer_secret= cfg.consumer_secret

access_token= cfg.access_token
access_token_secret= cfg.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def process_user(user):

    #check if data already collected
    user_directory = './unverified/'+user.screen_name+'/'
    if os.path.exists(user_directory) and os.listdir(user_directory):
      print 'User '+user.screen_name+'s info has already been collected.'
      return

    #create necessary directories
    if not os.path.exists(user_directory):
      os.makedirs(user_directory)

    #save user info
    file_name = './unverified/'+user.screen_name+'/'+user.screen_name+'_info.pickle'
    with open(file_name, 'w') as f:
      pickler = pickle.Pickler(f, -1)
      pickler.dump(user)

    #save tweets
    file_name = './unverified/'+user.screen_name+'/'+user.screen_name+'_tweets.pickle'
    with open(file_name, 'a') as f:
      pickler = pickle.Pickler(f, -1)
      for tweet in tweepy.Cursor(api.user_timeline,screen_name=user.screen_name).items(200):
        pickler.dump(tweet)

class StreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        if not tweet.user.verified:
          process_user(tweet.user)

l = StreamListener()
streamer = tweepy.Stream(auth=auth, listener=l)
streamer.sample()
