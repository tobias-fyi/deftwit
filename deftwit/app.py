"""
:: Def Twit :: def twit() :: deft wit :: 

A simple Flask application for analyzing and predicting tweets.
"""

from decouple import config
from flask import Flask, render_template

from deftwit.models import DB, User, Tweet
from deftwit.twitter import TWITTER, DeftTwit
from deftwit.forms import GetUserForm, CompareForm


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

    # Set up the secret key
    app.config["SECRET_KEY"] = config("FLASK_SECRET_KEY")

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

        # TODO: add form to capture user input / parameters
        form = GetUserForm()

        # Display list of users already in the database
        users = User.query.all()

        return render_template("home.html", title="Home", users=users, form=form)

    @app.route("/user", methods=["POST"])  # Uses the form
    @app.route("/user/<handle>", methods=["GET"])  # Uses the parameter
    def user(handle=None, message=""):
        """
        Returns a list of a user's tweets.
        
        Parameters
        ----------
        handle : string
            The Twitter handle of the user; default is None.
        message : string
            The message to display on the page, default is empty string.
        
        Returns
        -------
        html/jinja2 template
            Returns 'user.html', inheriting from 'base.html'.
        """

        # TODO: include a button to save to database

        try:
            # When user uses the form
            if request.method == "POST":
                # Instantiate the twitter handle as a DeftTwit object
                dftw = DeftTwit(handle)
                # Get the DeftTwit's tweets via class method
                tweets = dftw.tweet_list()
                message = f"User @{handle} succussfully added."
            tweets = 
        except Exception as e:
            raise e
            tweets = []

        return render_template(
            "user.html", 
            title=f"{handle}", 
            handle=handle, 
            tweets=tweets, 
            message=message
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

        return render_template("about.html", title="About")

    return app
