"""
:: Def Twit :: def twit() :: deft wit :: 

A simple Flask application for analyzing and predicting tweets.
"""

from decouple import config
from flask import Flask, render_template

from deftwit.models import DB, User, Tweet
from deftwit.twitter import TWITTER, add_tweets_to_db, tweet_list


def create_app():
    """
    App factory.
    
    Returns
    -------
    app
        Flask app.
    """

    # Define the application
    app = Flask(__name__)

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize DB-app connection
    DB.init_app(app)

    @app.route("/")
    def home():
        """
        Home page route.
        
        Returns
        -------
        html/jinja2 template
            Returns 'home.html', inheriting from 'base.html'.
        """

        # Set the tweets variable using query object
        users = User.query.all()

        return render_template("home.html", title="Home", users=users)

    @app.route("/user/<handle>")
    def user(handle):
        """
        Returns a list of a user's tweets.
        
        Parameters
        ----------
        handle : string
            The Twitter handle of the user, passed in via the URL route.
        
        Returns
        -------
        html/jinja2 template
            Returns 'user.html', inheriting from 'base.html'.
        """

        # # Get the user object
        # twitter_user = TWITTER.get_user(handle)

        # # Filter the user object for the tweets
        # tweets = twitter_user.timeline(
        #     count=200, exclude_replies=True, include_rts=False, mode="extended",
        # )

        tweets = tweet_list(handle)

        return render_template(
            "user.html", title=f"def twit({handle})", handle=handle, tweets=tweets
        )

    # Route to reset the database
    @app.route("/reset")
    def reset():
        """
        Reset database route; drops and recreates the database.
        
        Returns
        -------
        html/jinja2 template
            Returns 'home.html', inheriting from 'base.html'.
        """

        # Reset the database
        DB.drop_all()
        DB.create_all()

        return render_template("home.html", title="Home (Reset)")

    @app.route("/about")
    def about():
        """
        About page route.
        
        Returns
        -------
        html/jinja2 template
            Returns 'about.html', inheriting from 'base.html'.
        """

        # Set the tweets variable using query object
        tweets = Tweet.query.all()

        return render_template("about.html", title="About", tweets=tweets)

    return app
