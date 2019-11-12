"""
:: Def Twit :: def twit() :: deft wit :: 

A simple Flask application for analyzing and predicting tweets.
"""

from decouple import config
from flask import Flask, render_template
from deftwit.models import DB, User, Tweet


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

    @app.route("/about")
    def about():
        """
        About page route.
        
        Returns
        -------
        html/jinja2 template
            Returns 'about.html', inheriting from 'about.html'.
        """

        # Set the tweets variable using query object
        tweets = Tweet.query.all()

        return render_template("about.html", title="About", tweets=tweets)

    # Route to reset the database
    @app.route("/reset")
    def reset():
        """
        Reset database route; drops and recreates the database.
        
        Returns
        -------
        html/jinja2 template
            Returns 'about.html', inheriting from 'about.html'.
        """

        # Reset the database
        DB.drop_all()
        DB.create_all()

        return render_template("reset.html", title="Reset")

    return app
