"""
deftwit :: Definition of the deftwit database models.
"""

from flask_sqlalchemy import SQLAlchemy

# Import the database
DB = SQLAlchemy()


class User(DB.Model):
    """General class for the Twitter user to be analyzed."""

    id = DB.Column(DB.BigInteger, primary_key=True)
    handle = DB.Column(DB.String(32), nullable=False)
    intro = DB.Column(DB.String(500), nullable=True)
    newest_tweet_id = DB.Column(DB.BigInteger, nullable=True)
    # Look for other useful info to include

    def __repr__(self):
        return f"<User @{self.name}>"


class Tweet(DB.Model):
    """A general class for a user's tweets, gathered from Twitter."""

    id = DB.Column(DB.BigInteger, primary_key=True)
    body = DB.Column(DB.Unicode(500))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))
    # TODO: add a date_posted field

    embedding = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return f"<Tweet '{self.body}'>"
