# random_forest.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load your dataset
career =pd.read_csv('dataset9000.data', header=None)

# Convert features to float to avoid dtype warning
career.iloc[:, :-1] = career.iloc[:, :-1].astype(float)

# Optional: Add Gaussian noise for slight randomization
career.iloc[:, :-1] += np.random.normal(0, 0.3, size=career.iloc[:, :-1].shape)

# Splitting dataset
X = career.iloc[:, :-1]
y = career.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of Random Forest: {accuracy:.2f}")

# Save the model
joblib.dump(model, "random_forest_model.pkl")
