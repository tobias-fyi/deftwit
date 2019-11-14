"""
Prediction of users based on Basilica tweet embeddings.
"""

import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

from deftwit.models import User
from deftwit.twitter import BASILICA


def predict_which_user(user1_handle, user2_handle, tweet_text, cache=None):
    """
    Determines which user is more likely to tweet a given phrase.
    
    Parameters
    ----------
    user1_handle : str
        First user's Twitter handle.
    user2_handle : str
        Second user's Twitter handle.
    tweet_text : str
        The phrase to use in prediction.
    """

    user_set = pickle.dumps((user1_handle, user2_handle))
    if cache and cache.exists(user_set):
        log_reg = pickle.loads(cache.get(user_set))
    else:
        # Get the users from the database
        user1 = User.query.filter(User.handle == user1_handle).one()
        user2 = User.query.filter(User.handle == user2_handle).one()

        # Get the embeddings for the users' tweets
        user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
        user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])

        # Put embeddings into a vertical array
        embeddings = np.vstack([user1_embeddings, user2_embeddings])
        labels = np.concatenate(
            [np.ones(len(user1.tweets)), np.zeros(len(user2.tweets))]
        )

        # Fit the regression model
        log_reg = LogisticRegression().fit(embeddings, labels)
        cache and cache.set(user_set, pickle.dumps(log_reg))

    # Test out the new / input tweet
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model="twitter")

    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
