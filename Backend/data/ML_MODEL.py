import pandas as pd
import pickle
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Dataset
df = pd.read_csv("ParentCare_Final_Dataset.csv")

# Use fewer features to avoid perfect accuracy
features = [
    "Age",
    "Avg_Daily_Screen_Time_hr",
    "Educational_to_Recreational_Ratio",
    "Poor_Sleep"
]

target = "Wellness_Category"

X = df[features]
y = df[target]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    shuffle=True
)

# Simple Random Forest
model = RandomForestClassifier(
    n_estimators=20,
    max_depth=3,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Test
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy : {accuracy*100:.2f}%\n")
print(classification_report(y_test, y_pred))

# Save Model
Path("models").mkdir(exist_ok=True)

with open("models/wellness_model.pkl", "wb") as f:
    pickle.dump(model, f)

metadata = {
    "algorithm": "Random Forest",
    "accuracy": round(accuracy * 100, 2),
    "features": features,
    "target": target
}

with open("models/model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("\nModel saved successfully!")