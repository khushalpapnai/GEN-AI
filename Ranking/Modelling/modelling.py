import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
import pickle
import re

nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

data = pd.read_csv(r"..\Data\amazon_alexa.tsv", delimiter = '\t', quoting = 3)

data.dropna(inplace=True)

corpus = []
stemmer = PorterStemmer()
for i in range(0, data.shape[0]):
  review = re.sub('[^a-zA-Z]', ' ', data.iloc[i]['verified_reviews'])
  review = review.lower().split()
  review = [stemmer.stem(word) for word in review if not word in STOPWORDS]
  review = ' '.join(review)
  corpus.append(review)

cv = CountVectorizer(max_features = 2500)

#Storing independent and dependent variables in X and y
X = cv.fit_transform(corpus).toarray()
y = data['feedback'].values

pickle.dump(cv, open('../Models/countVectorizer.pkl', 'wb'))

scaler = MinMaxScaler()

X_train_scl = scaler.fit_transform(X_train)
X_test_scl = scaler.transform(X_test)

pickle.dump(scaler, open('../Models/scaler.pkl', 'wb'))

model_xgb = XGBClassifier()
model_xgb.fit(X_train_scl, y_train)

#Accuracy of the model on training and testing data
print("Training Accuracy :", model_xgb.score(X_train_scl, y_train))
print("Testing Accuracy :", model_xgb.score(X_test_scl, y_test))

y_preds = model_xgb.predict(X_test)

#Confusion Matrix
cm = confusion_matrix(y_test, y_preds)

#Saving the XGBoost classifier
pickle.dump(model_xgb, open('../Models/model_xgb.pkl', 'wb'))