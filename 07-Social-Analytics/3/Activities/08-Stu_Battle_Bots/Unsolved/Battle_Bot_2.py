# Dependencies
import numpy as np
import pandas as pd
import tweepy
import time
import json

# Twitter API Keys
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Twitter Credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Target Term
my_username = ""
conversation_partner = ""

# @TODO: Create a list of Response Lines
raise NotImplementedError()

# @TODO: Create converse function

#     # @TODO: Find the latest tweet from conversation_partner

#         # @TODO: Respond to the tweet with one of the response lines

# @TODO: Set timer to run every minute
raise NotImplementedError()
