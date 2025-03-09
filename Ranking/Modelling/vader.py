import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
import pickle

# Ensure VADER lexicon is downloaded
nltk.download('vader_lexicon')

class VaderSentimentModel(BaseEstimator, ClassifierMixin):
    def __init__(self, threshold=0.05):
        self.threshold = threshold
        self.sia = SentimentIntensityAnalyzer()

    def fit(self, X, y=None):
        # No training needed for rule-based model
        return self

    def predict(self, X):
        preds = []
        for text in X:
            score = self.sia.polarity_scores(str(text))['compound']
            label = 1 if score > self.threshold else 0  # Positive = 1, Negative = 0
            preds.append(label)
        return np.array(preds)


model = VaderSentimentModel()
model.fit(None)  # Not needed, but for API consistency


with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)
    print(loaded_model)

print("Model loaded successfully:", loaded_model)