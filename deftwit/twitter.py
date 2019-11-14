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


class DeftTwit:
    """A general class for manipulating users and their tweets."""

    def __init__(self, handle: str):
        self.handle = handle

        try:
            # Initialize instance with user object
            self.twitter_user = TWITTER.get_user(self.handle)
        except tweepy.TweepError as tweep_error:
            raise tweep_error

    def tweet_list(
        self,
        count: int = 200,
        replies: bool = False,
        retweets: bool = False,
        mode: str = "extended",
    ):
        """
        Get a list of a user's tweets.
        
        Parameters
        ----------
        count : int, optional
            Number of tweets to retrieve, by default 200
        replies : bool, optional
            Include the user's replies, by default False
        retweets : bool, optional
            Include the user's retweets, by default False
        mode : str, optional
            Include the full or short text, by default "extended"

        Returns
        -------
        tweets : list
            Returns a list of the user's tweets.
        """

        # Otherwise, filter the user object for the tweets
        tweets = self.twitter_user.timeline(
            count=count,
            exclude_replies=(replies == False),
            include_rts=retweets,
            tweet_mode=mode,
        )

        return tweets

    def tweet_list_from_db(self):
        """
        Get a list of a user's tweets.

        Returns
        -------
        tweets : list
            Returns a list of the user's tweets.
        """

        try:
            if len(User.query.filter(User.handle == self.handle).first().tweets) > 0:
                tweets = User.query.filter(User.handle == self.handle).first().tweets
        except Exception as e:
            raise e

        return tweets

    def update_db(self):
        """
        Adds to the database 200 tweets from a user's Twitter timeline.

        Returns
        -------
        tweets : list
            Returns a list of the user's tweets.
        """

        try:
            # Get the tweets object from the API
            tweets = self.tweet_list(self.handle, True)

            # Get the user from the db
            # If not added yet, define as instance of User
            db_user = User.query.get(self.twitter_user.id) or User(
                id=self.twitter_user.id,
                handle=self.twitter_user.screen_name,
                intro=self.twitter_user.description,
            )

            DB.session.add(db_user)  # Add the User to the database session

            if tweets:  # Confirm that the user has a first tweet to use
                db_user.newest_tweet_id = tweets[0].id

            for tweet in tweets:
                # Send tweet to Basilica to request embedding
                embedding = BASILICA.embed_sentence(tweet.full_text, model="twitter")
                # Create instance of Tweet data model
                db_tweet = Tweet(
                    id=tweet.id, body=tweet.full_text[:500], embedding=embedding
                )
                # Append this tweet to the list of this user's tweets
                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)  # Add instance to database session

        except Exception as e:
            print(f"Error processing {self.twitter_user}: {e}")
            raise e
        else:
            DB.session.commit()  # Commit the database session to the database

        return tweets

    def __str__(self):
        """Define the string conversion of the class instance."""
        return f"<@{self.handle}>"

    def __repr__(self):
        """Define the detailed string conversion of the class instance."""
        return f"{self.__class__.__name__}('{self.handle}')"
