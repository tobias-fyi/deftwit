"""
deftwit :: Definition of the deftwit database models.
"""

from flask_sqlalchemy import SQLAlchemy

# Import the database
DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users to be analyzed."""

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(32), nullable=False)


class Tweet(DB.Model):
    """The user's tweets gathered from Twitter."""

    id = DB.Column(DB.Integer, primary_key=True)
    body = DB.Column(DB.Unicode(240))

