import tweepy
import os
from config import Config

keys = file('config.cfg')
cfg = Config(keys)

consumer_key= cfg.consumer_key
consumer_secret= cfg.consumer_secret

access_token= cfg.access_token
access_token_secret= cfg.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

def process_user(user):
    file_name = './verified/'+user.screen_name+'.txt'
    with open(file_name, 'w') as f:
      s = user.screen_name + " " + str(user.verified)

      f.write(s)
      f.close()

for friend in tweepy.Cursor(api.friends, id="verified").items(1):
  process_user(friend)
