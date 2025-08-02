"""
Retrain RandomForest with the updated feature extractor.
Run from inside backend/ai_model:  python train_model.py
"""

import os
import joblib, pandas as pd
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from features import extract_features   # local import

tqdm.pandas()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET = os.path.join(SCRIPT_DIR, "dataset.csv")
MODEL_OUT  = os.path.join(SCRIPT_DIR, "phishing_model.pkl")

# -----------------------------------------------------------------
print(f"📑  Loading dataset: {DATASET}")
df = pd.read_csv(DATASET)        # must contain 'url' & 'label' columns

# Feature-engineering
print("🔬  Extracting features (this takes a moment on first run)…")
X = df["url"].progress_apply(extract_features).apply(pd.Series)
y = df["label"].astype(int)

# Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

# Model training
clf = RandomForestClassifier(
    n_estimators=300, max_depth=None,
    class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# Evaluation
print("\n✅  Test-set performance:")
print(classification_report(y_test, clf.predict(X_test)))


print("\n✅  Test-set performance:")
print(classification_report(y_test, clf.predict(X_test)))

# ============= NEW: visual validation ==========
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
import matplotlib.pyplot as plt
import os

PLOTS_DIR = os.path.join(SCRIPT_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Confusion Matrix
ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test)
plt.title("Test-set Confusion Matrix")
plt.tight_layout()
cm_path = os.path.join(PLOTS_DIR, "confusion_matrix.png")
plt.savefig(cm_path)
plt.close()

# ROC Curve
RocCurveDisplay.from_estimator(clf, X_test, y_test)
plt.title("ROC Curve")
plt.tight_layout()
roc_path = os.path.join(PLOTS_DIR, "roc_curve.png")
plt.savefig(roc_path)
plt.close()

print(f"🖼️  Plots saved → {cm_path} / {roc_path}")

# -----------------------------------------------
# Persist
joblib.dump((clf, list(X.columns)), MODEL_OUT)
print(f"\n💾  Model saved →  {MODEL_OUT}")
