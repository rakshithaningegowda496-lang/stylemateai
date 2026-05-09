import pickle

# Load saved model
model = pickle.load(open("core/model.pkl", "rb"))
vectorizer = pickle.load(open("core/vectorizer.pkl", "rb"))

def predict_outfit(occasion, mood, weather="normal"):
    text = occasion + " " + mood + " " + weather
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]