import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from features import extract_features

# ✅ Enable tqdm for progress tracking
tqdm.pandas()

# ✅ Load dataset
script_dir = os.path.dirname(__file__)
dataset_path = os.path.join(script_dir, "dataset.csv")
df = pd.read_csv(dataset_path)

# ✅ Extract features
features_df = df["url"].progress_apply(extract_features).apply(pd.Series)

# ✅ Convert booleans to integers
features_df = features_df.astype(int)

X = features_df
y = df["label"]

# ✅ Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# ✅ Train the model
print("🤖 Training model...")
model = RandomForestClassifier()
model.fit(X_train, y_train)

# ✅ Evaluate accuracy
accuracy = model.score(X_test, y_test)
print("✅ Model trained. Accuracy:", accuracy)

# ✅ Save model
model_path = os.path.join(script_dir, "phishing_model.pkl")
joblib.dump((model, list(X.columns)), model_path)
print("✅ phishing_model.pkl saved with trusted_tld feature!")
