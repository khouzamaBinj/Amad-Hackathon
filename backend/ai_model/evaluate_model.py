import pandas as pd, joblib, os
from features import extract_features           # نفس المستخرج الذي درّبت به
from sklearn.metrics import accuracy_score, confusion_matrix

# المسارات
MODEL_PATH = os.path.join(os.path.dirname(__file__), "phishing_model.pkl")
DATA_PATH  = os.path.join(os.path.dirname(__file__), "dataset.csv")

# حمّل الموديل والبيانات
model, feat_cols = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# استخرج الميزات بالترتيب الصحيح
X = df["url"].apply(lambda u: [extract_features(u)[k] for k in feat_cols]).tolist()
y_true = df["label"].values
y_pred = model.predict(X)

# احسب الدقّة والمصفوفة
acc = accuracy_score(y_true, y_pred)
cm  = confusion_matrix(y_true, y_pred)

print(f"Accuracy on 300 URLs: {acc:.2%}")
print("Confusion Matrix [tn fp; fn tp]:\n", cm)
