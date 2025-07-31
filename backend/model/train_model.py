import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Example: Load dataset
df = pd.read_csv("dataset.csv")
x = df.drop("label", axis=1)
y = df["label"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(x_train, y_train)

print("Accuracy:", accuracy_score(y_test, model.predict(x_test)))
joblib.dump(model, "phishing_model.pkl")