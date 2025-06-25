import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

# Load dataset
career = pd.read_csv('dataset9000.data', header=None)
career.columns = [
    "Database Fundamentals", "Computer Architecture", "Distributed Computing Systems",
    "Cyber Security", "Networking", "Development", "Programming Skills", "Project Management",
    "Computer Forensics Fundamentals", "Technical Communication", "AI ML", "Software Engineering",
    "Business Analysis", "Communication skills", "Data Science", "Troubleshooting skills",
    "Graphics Designing", "Roles"
]

# Remove rows that are completely empty
career.dropna(how='all', inplace=True)

# Features and labels
X = np.array(career.iloc[:, :-1])
y = np.array(career.iloc[:, -1])

# Optional: Add noise to avoid overfitting (only if needed)
# X = X + np.random.normal(0, 0.1, X.shape)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize Decision Tree with restricted complexity to avoid overfitting
model = DecisionTreeClassifier(
    random_state=42,
    max_depth=14,             # Limits depth of tree
    min_samples_split=10,    # Minimum samples needed to split a node
    min_samples_leaf=5       # Minimum samples per leaf
)

# Train and evaluate
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Decision Tree Accuracy: {acc * 100:.2f}%")
