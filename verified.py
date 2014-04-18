import os
import tweepy
import json
from config import Config
from tweepy.parsers import RawParser
import pickle

keys = file('config.cfg')
cfg = Config(keys)

consumer_key= cfg.consumer_key
consumer_secret= cfg.consumer_secret

access_token= cfg.access_token
access_token_secret= cfg.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,parser=RawParser(), wait_on_rate_limit=True)

def process_user(user):

    #create necessary directories
    directory = './verified/'+user.screen_name+'/'
    if not os.path.exists(directory):
      os.makedirs(directory)

    #save user info
    file_name = './verified/'+user.screen_name+'/'+user.screen_name+'_info.txt'
    with open(file_name, 'w') as f:
      json.dump(user, f)

    #save tweets
    file_name = './verified/'+user.screen_name+'/'+user.screen_name+'_tweets.txt'
    with open(file_name, 'a') as f:
      for tweet in api.user_timeline(id=user.screen_name):
        json.dump(tweet, f)

for friend in tweepy.Cursor(api.friends, id="verified").iteritems(1):
  process_user(friend)
