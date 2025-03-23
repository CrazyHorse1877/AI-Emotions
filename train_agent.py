import json
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load action log
with open("agent_log.json", "r") as f:
    log = json.load(f)

# Prepare dataset
X = []
y = []

for entry in log:
    state = entry["state"]
    action = entry["action"]

    X.append([
        state["hunger"],
        state["energy"],
        state["health"],
        state["stimulation"],
        state["fear_level"]
    ])
    y.append(action)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
print("🧠 Model Performance:")
print(classification_report(y_test, clf.predict(X_test)))

# Save model
with open("policy_model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("✅ Trained model saved to 'policy_model.pkl'")
