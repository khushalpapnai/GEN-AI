import pickle
import numpy as np

# Global model instance
sentiment_model = None

def getModel():
    global sentiment_model  # make sure to modify the global variable
    if sentiment_model is None:
        with open("model.pkl", "rb") as f:
            sentiment_model = pickle.load(f)
    return sentiment_model

def predict_sentiment(comments):
    """
    Predicts sentiment using a singleton model instance.
    """
    model = getModel()  # ensures it's loaded only once
    return np.array(model.predict(comments))
