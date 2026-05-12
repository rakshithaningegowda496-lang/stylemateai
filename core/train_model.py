import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# ── Load Skin Type Dataset ──────────────────────
df = pd.read_csv("core/dataset/Skin_Type_OG.csv")

# Encode categorical columns
le_gender = LabelEncoder()
le_hydration = LabelEncoder()
le_oil = LabelEncoder()
le_sensitivity = LabelEncoder()
le_target = LabelEncoder()

df["Gender"]          = le_gender.fit_transform(df["Gender"])
df["Hydration_Level"] = le_hydration.fit_transform(df["Hydration_Level"])
df["Oil_Level"]       = le_oil.fit_transform(df["Oil_Level"])
df["Sensitivity"]     = le_sensitivity.fit_transform(df["Sensitivity"])
df["Skin_Type"]       = le_target.fit_transform(df["Skin_Type"])

# Features and target
X = df[["Age","Gender","Hydration_Level","Oil_Level","Sensitivity","Humidity","Temperature"]]
y = df["Skin_Type"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Quick check
train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc  = accuracy_score(y_test,  model.predict(X_test))
print(f"Train Accuracy: {train_acc:.2f}")
print(f"Test  Accuracy: {test_acc:.2f}")

# Save model + encoders
pickle.dump(model,         open("core/model.pkl",         "wb"))
pickle.dump(le_target,     open("core/label_encoder.pkl", "wb"))
pickle.dump(le_gender,     open("core/le_gender.pkl",     "wb"))
pickle.dump(le_hydration,  open("core/le_hydration.pkl",  "wb"))
pickle.dump(le_oil,        open("core/le_oil.pkl",        "wb"))
pickle.dump(le_sensitivity,open("core/le_sensitivity.pkl","wb"))

print("✅ Model trained and saved!")
print("Classes:", list(le_target.classes_))

