"""
:: Def Twit :: def twit() :: deft wit :: 

A simple Flask application for analyzing and predicting tweets.
"""

from decouple import config
from flask import Flask, render_template, url_for, flash, redirect, request

from deftwit.twitter import TWITTER, DeftTwit
from deftwit.models import DB, User, Tweet
from deftwit.predict import predict_which_user

from dotenv import load_dotenv

load_dotenv()


def create_app():
    """Flask app factory - sets the application context."""

    # Define the application
    app = Flask(__name__)

    # Set up the secret key
    app.config["SECRET_KEY"] = config("FLASK_SECRET_KEY")

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize DB-app connection
    DB.init_app(app)

    @app.route("/", methods=["GET", "POST"])
    def home():
        """Home page route."""

        # Display list of users already in the database
        users = User.query.all()

        from deftwit.forms import GetUserForm

        form = GetUserForm()  # Instantiate the GetUserForm

        if form.validate_on_submit():
            # Instantiate the twitter handle as a DeftTwit object
            dftw = DeftTwit(form.handle.data)
            # Get the DeftTwit's tweets and update db via class method
            tweets = dftw.update_db()
            # Create success message
            flash(f"User @{form.handle.data} added to database", "success")
            return redirect(url_for("user", handle=form.handle.data))

        return render_template("home.html", title="Home", users=users, form=form)

    @app.route("/user/<handle>", methods=["GET", "POST"])
    def user(handle=None):
        """
        Returns a list of a user's tweets, with a form to add another user.
        
        Parameters
        ----------
        handle : string
            The Twitter handle of the user; default is None.
        """
        # Display list of users already in the database
        users = User.query.all()

        from deftwit.forms import GetUserForm

        form = GetUserForm()

        # TODO: include a button to save to database
        tweets = []

        try:
            if request.method == "POST":
                if form.validate_on_submit():
                    # Instantiate the twitter handle as a DeftTwit object
                    dftw = DeftTwit(form.handle.data)
                    # Get the DeftTwit's tweets and update db via class method
                    tweets = dftw.update_db()
                    # Create success message
                    flash(f"User @{form.handle.data} added to database", "success")
                    return redirect(url_for("user", handle=form.handle.data))
            else:
                dftw = DeftTwit(handle)
                tweets = dftw.tweet_list_from_db()

        except Exception as e:
            raise e

        return render_template(
            "user.html", title=f"{handle}", form=form, tweets=tweets, users=users
        )

    @app.route("/predict", methods=["GET", "POST"])
    def predict():
        """
        Predict by which user the tweet is more likely to be tweeted.
        """
        from deftwit.forms import PredictForm

        form = PredictForm()

        if form.validate_on_submit():
            user_1, user_2 = sorted([form.user_1.data, form.user_2.data])

            if user_1 == user_2:
                flash(
                    f"""T'would be lame to compare {form.user_1.data} 
                    against {form.user_2.data}. Try again""",
                    "danger",
                )
                return redirect(url_for("predict", handle=form.handle.data))
            else:
                prediction = predict_which_user(
                    form.user_1.data, form.user_1.data, form.tweet_text.data,
                )
                flash(
                    f"""`{form.tweet_text.data}`
                is more likely to be said by {user_1 if prediction else user_2}""",
                    "shade1",
                )

        return render_template("predict.html", title="Predict", form=form)

    # Route to reset the database
    @app.route("/reset")
    def reset():
        """Reset database route; drops and recreates the database."""

        # Reset the database
        DB.drop_all()
        DB.create_all()

        return render_template("reset.html", title="Reset")

    return app
