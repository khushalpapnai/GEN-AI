import pickle
from Modelling.vader import VaderSentimentModel

with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

print("Model loaded successfully:", loaded_model)

sample_texts = [
    "This is a fantastic product!",
    "I hate this, it's terrible."
]

predictions = loaded_model.predict(sample_texts)
print(predictions)  # [1, 0]

