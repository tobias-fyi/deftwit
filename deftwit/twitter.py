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


def tweet_list(handle):
    """
    Get a list of a user's tweets.
    
    Parameters
    ----------
    handle : string
        User's Twitter handle.
    """

    # Get the user object
    twitter_user = TWITTER.get_user(handle)

    # Filter the user object for the tweets
    tweets = twitter_user.timeline(
        count=200, exclude_replies=True, include_rts=False, tweet_mode="extended",
    )

    return tweets


# Define functions to use inside the routes
def add_tweets_to_db(handle, count=200, replies=False, retweets=False, mode="extended"):
    """
    Adds to the database 200 tweets from a user's Twitter timeline.
    
    Parameters
    ----------
    handle : string
        The user's Twitter handle, without the '@'.
    count : int, optional
        Number of tweets to retrieve, by default 200
    replies : bool, optional
        Include the user's replies, by default False
    retweets : bool, optional
        Include the user's retweets, by default False
    mode : str, optional
        Include the full or short text, by default "extended"
    """

    # Get the user object
    twitter_user = TWITTER.get_user(handle)

    # Filter the user object for the tweets
    tweets = twitter_user.timeline(
        count=count,
        exclude_replies=(replies == False),
        include_rts=retweets,
        mode=mode,
    )

    # Define the user as instance of User
    db_user = User(
        id=twitter_user.id,
        handle=twitter_user.screen_name,
        newest_tweet_id=tweets[0].id,
    )

    for tweet in tweets:
        # Send tweet to Basilica to request embedding
        embedding = BASILICA.embed_sentence(tweet.full_text, model="twitter")
        # Create instance of Tweet data model
        db_tweet = Tweet(id=tweet.id, body=tweet.full_text[:500], embedding=embedding)
        DB.session.add(db_tweet)  # Add instance to database session
        # Append this tweet to the list of this user's tweets
        db_user.tweets.append(db_tweet)

    DB.session.add(db_user)  # Add the user to the database session

    DB.session.commit()  # Commit the database session to the database


def save_tweets(tweets):
    """
    Request Basilica embed and add that and the tweets to DB session.
    
    Parameters
    ----------
    tweets : list
        List of user's tweets to commit to the database.
    """

    for tweet in tweets:
        # Send tweet to Basilica to request embedding
        embedding = BASILICA.embed_sentence(tweet.full_text, model="twitter")
        # Create instance of Tweet data model
        db_tweet = Tweet(id=tweet.id, body=tweet.full_text[:500], embedding=embedding)
        DB.session.add(db_tweet)  # Add instance to database session
        # Append this tweet to the list of this user's tweets
        db_user.tweets.append(db_tweet)

    DB.session.add(db_user)  # Add the user to the database session

    DB.session.commit()  # Commit the database session to the database

