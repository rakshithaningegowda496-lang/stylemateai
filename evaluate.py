import pandas as pd
import pickle
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# ── Load dataset ────────────────────────────────
df = pd.read_csv("core/dataset/Skin_Type_OG.csv")

le_gender      = pickle.load(open("core/le_gender.pkl",      "rb"))
le_hydration   = pickle.load(open("core/le_hydration.pkl",   "rb"))
le_oil         = pickle.load(open("core/le_oil.pkl",         "rb"))
le_sensitivity = pickle.load(open("core/le_sensitivity.pkl", "rb"))
le_target      = pickle.load(open("core/label_encoder.pkl",  "rb"))
model          = pickle.load(open("core/model.pkl",          "rb"))

df["Gender"]          = le_gender.transform(df["Gender"])
df["Hydration_Level"] = le_hydration.transform(df["Hydration_Level"])
df["Oil_Level"]       = le_oil.transform(df["Oil_Level"])
df["Sensitivity"]     = le_sensitivity.transform(df["Sensitivity"])
df["Skin_Type"]       = le_target.transform(df["Skin_Type"])

X = df[["Age","Gender","Hydration_Level","Oil_Level","Sensitivity","Humidity","Temperature"]]
y = df["Skin_Type"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Evaluate ────────────────────────────────────
train_preds = model.predict(X_train)
test_preds  = model.predict(X_test)

print("=" * 40)
print(f"Train Accuracy : {accuracy_score(y_train, train_preds):.2f}")
print(f"Test  Accuracy : {accuracy_score(y_test,  test_preds):.2f}")
print("=" * 40)
print("\nClass Distribution in Predictions:")
pred_labels = le_target.inverse_transform(test_preds)
print(Counter(pred_labels))
print("\nDetailed Report:")
print(classification_report(y_test, test_preds,
      target_names=le_target.classes_))