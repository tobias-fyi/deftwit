"""
:: Def Twit :: def twit() :: deft wit :: 

A simple Flask application for analyzing and predicting tweets.
"""

from flask import Flask, render_template
from .models import DB


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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    # Initialize DB-app connection
    DB.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html", title="Home")

    @app.route("/about")
    def about():
        return render_template("about.html", title="About")

    return app
