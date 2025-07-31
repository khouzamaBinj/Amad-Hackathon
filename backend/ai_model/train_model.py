import pandas as pd
import joblib
from features import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

print("🔍 Extracting features...")

# Load dataset
script_dir = os.path.dirname(__file__)
dataset_path = os.path.join(script_dir, "dataset.csv")
df = pd.read_csv(dataset_path)

# Extract only numeric features
features_df = df["url"].apply(extract_features).apply(pd.Series)

# Convert bools to integers
features_df = features_df.astype(int)

X = features_df
y = df["label"]

print("🤖 Training model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("✅ Model trained. Accuracy:", accuracy)

joblib.dump((model, list(X.columns)), os.path.join(script_dir, "phishing_model.pkl"))
print("✅ phishing_model.pkl saved")
