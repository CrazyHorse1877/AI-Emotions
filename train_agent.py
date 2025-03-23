import json
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from collections import Counter

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

# Reward histogram
rewards = [entry["reward"] for entry in log]
plt.figure(figsize=(10, 4))
plt.hist(rewards, bins=20, color='skyblue', edgecolor='black')
plt.title("Reward Distribution")
plt.xlabel("Reward")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()

# Action distribution
action_counts = Counter(y)
plt.figure(figsize=(8, 4))
plt.bar(action_counts.keys(), action_counts.values(), color='orange')
plt.title("Action Label Distribution")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Feature importance (if tree-based model)
if hasattr(clf, "feature_importances_"):
    features = ["hunger", "energy", "health", "stimulation", "fear"]
    importances = clf.feature_importances_
    plt.figure(figsize=(8, 4))
    plt.bar(features, importances, color='green')
    plt.title("Feature Importance")
    plt.ylabel("Importance")
    plt.tight_layout()
    plt.show()