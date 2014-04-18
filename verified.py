import tweepy
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
    print user.screen_name + " " + str(user.verified)

for friend in tweepy.Cursor(api.friends, id="verified").items():
  process_user(friend)
