"""
:: deftwit.forms ::

A source of truthyness for deftwit wtforms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from deftwit.models import DB, User, Tweet


class GetUserForm(FlaskForm):
    """
    A general class for a Twitter handle input form.

    Inherits from flask_wtf.FlaskForm.
        Flask-specific subclass of WTForms :class:`~wtforms.form.Form`.
    """

    # Text field for user to input target Twitter handle
    handle = StringField(
        "Twitter Handle", validators=[DataRequired(), Length(min=2, max=15)]
    )
    # Submit button to add the user to the db
    submit = SubmitField("Add User")


class PredictForm(FlaskForm):
    """
    A general class for selecting two Twitter users and comparing them
    based on a text input field.
    
    Inherits from flask_wtf.FlaskForm.
        Flask-specific subclass of WTForms :class:`~wtforms.form.Form`.
    """

    # Get list of choices (users) from database
    users = User.query.all()

    # Create the selection fields - choice tuples defined using list comprehension
    user_1 = SelectField(
        "Twit #1", choices=[(user.handle, user.handle) for user in users],
    )
    user_2 = SelectField(
        "Twit #2", choices=[(user.handle, user.handle) for user in users],
    )

    # TODO: create function that generates a random tweet
    tweet_text = StringField(
        "Tweet text", validators=[DataRequired(), Length(min=1, max=240)]
    )

    submit = SubmitField("Predict")

