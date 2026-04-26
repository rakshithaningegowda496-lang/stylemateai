import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
df = pd.read_csv("core/dataset/outfits.csv")

# Combine features
df["input"] = df["occasion"] + " " + df["mood"] + " " + df["weather"]

X = df["input"]
y = df["outfit"]

# Better vectorizer
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X_vec, y)

# Save model
pickle.dump(model, open("core/model.pkl", "wb"))
pickle.dump(vectorizer, open("core/vectorizer.pkl", "wb"))
df = pd.read_csv("core/dataset/outfits.csv")   # ✅ use your file

print("✅ Model trained successfully")