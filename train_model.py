"""
Run once before starting the API:
    python train_model.py
"""
import pickle, json, sys
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE  = Path(__file__).resolve().parent
DATA  = BASE / "data" / "ParentCare_Final_Dataset.csv"
MDIR  = BASE / "models"

if not DATA.exists():
    print(f"ERROR: {DATA} not found. Put ParentCare_Final_Dataset.csv in data/ folder.")
    sys.exit(1)

print("Loading ParentCare_Final_Dataset.csv ...")
df = pd.read_csv(DATA)
print(f"Loaded {len(df)} records, {len(df.columns)} columns.")

FEATURES = ["Age","Avg_Daily_Screen_Time_hr","Educational_to_Recreational_Ratio",
            "Poor_Sleep","Eye_Strain","Anxiety","Obesity_Risk"]
TARGET   = "Wellness_Category"

X = df[FEATURES].copy()
for c in ["Poor_Sleep","Eye_Strain","Anxiety","Obesity_Risk"]:
    X[c] = X[c].astype(int)
y = df[TARGET]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

print("Training Random Forest ...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
clf.fit(X_train, y_train)

y_pred  = clf.predict(X_test)
acc     = round(accuracy_score(y_test, y_pred)*100, 1)
print(f"\nAccuracy: {acc}%")
print(classification_report(y_test, y_pred))

print("Feature Importances:")
for f,i in sorted(zip(FEATURES,clf.feature_importances_),key=lambda x:-x[1]):
    print(f"  {f:<42} {i*100:.1f}%  {'█'*int(i*40)}")

MDIR.mkdir(parents=True, exist_ok=True)
with open(MDIR/"wellness_model.pkl","wb") as f: pickle.dump(clf,f)

meta = {
    "algorithm": "Random Forest Classifier",
    "total_records": len(df), "training_records": len(X_train),
    "test_records": len(X_test), "accuracy": acc,
    "features_used": len(FEATURES), "target": TARGET,
    "classes": list(clf.classes_),
    "feature_importances": {f:round(i*100,1) for f,i in zip(FEATURES,clf.feature_importances_)}
}
with open(MDIR/"model_metadata.json","w") as f: json.dump(meta,f,indent=2)

print(f"\nSaved: models/wellness_model.pkl + models/model_metadata.json")
print("Now run:  uvicorn app.main:app --reload")
