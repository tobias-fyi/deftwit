"""
deftwit.twitter :: Utilities for connecting to Twitter and Basilica APIs.
"""

from decouple import config

import basilica
import tweepy

from deftwit.models import DB, Tweet, User


# Set up twitter authorization and connection
TWITTER_AUTH = tweepy.OAuthHandler(
    config("TWITTER_API_KEY"), config("TWITTER_API_KEY_SECRET"),
)

TWITTER_AUTH.set_access_token(
    config("TWITTER_TOKEN"), config("TWITTER_TOKEN_SECRET"),
)

TWITTER = tweepy.API(TWITTER_AUTH)

# Set up Basilica connection
BASILICA = basilica.Connection(config("BASILICA_KEY"))

