import os
import json
import pickle
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

# Ensure base directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# ========== CONFIG ========== #
MODEL_TYPE = "DecisionTree"
MAX_DEPTH = 5
TEST_SPLIT = 0.2
RANDOM_SEED = 42
DATA_FILE = "agent_log.json"
FEATURE_NAMES = ["hunger", "energy", "health", "stimulation", "fear_level"]

# ========== LOAD DATA ========== #
with open(DATA_FILE, "r") as f:
    log = json.load(f)

X, y, rewards = [], [], []

for entry in log:
    state = entry["state"]
    X.append([state[f] for f in FEATURE_NAMES])
    y.append(entry["action"])
    rewards.append(entry["reward"])

# ========== SPLIT + TRAIN ========== #
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SPLIT, random_state=RANDOM_SEED
)

clf = DecisionTreeClassifier(max_depth=MAX_DEPTH, random_state=RANDOM_SEED)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
report = classification_report(y_test, y_pred, output_dict=False)

# ========== VERSION MANAGEMENT ========== #
def next_version(base_path):
    os.makedirs(base_path, exist_ok=True)  # ensure it exists first
    existing = [d for d in os.listdir(base_path) if d.startswith("v")]
    existing_versions = [int(d[1:]) for d in existing if d[1:].isdigit()]
    return f"v{max(existing_versions, default=0) + 1}"

model_version = next_version("models")
model_path = os.path.join("models", model_version)
plot_path = os.path.join("plots", model_version)

os.makedirs(model_path, exist_ok=True)
os.makedirs(plot_path, exist_ok=True)


# ========== SAVE MODEL & METADATA ========== #
with open(os.path.join(model_path, "policy_model.pkl"), "wb") as f:
    pickle.dump(clf, f)

with open(os.path.join(model_path, "config.json"), "w") as f:
    json.dump({
        "model_type": MODEL_TYPE,
        "max_depth": MAX_DEPTH,
        "test_split": TEST_SPLIT,
        "trained_on": len(X),
        "features": FEATURE_NAMES,
        "timestamp": datetime.now().isoformat(),
        "f1_macro": f1_score(y_test, y_pred, average="macro")
    }, f, indent=2)

with open(os.path.join(model_path, "report.txt"), "w") as f:
    f.write(report)

print(f"✅ Model saved to {model_path}")

# ========== PLOTS ========== #
# 1. Reward Distribution
plt.figure(figsize=(10, 4))
plt.hist(rewards, bins=20, color='skyblue', edgecolor='black')
plt.title("Reward Distribution")
plt.xlabel("Reward")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_path, "reward_distribution.png"))
plt.close()

# 2. Action Label Distribution
action_counts = Counter(y)
plt.figure(figsize=(8, 4))
plt.bar(action_counts.keys(), action_counts.values(), color='orange')
plt.title("Action Label Distribution")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(plot_path, "action_distribution.png"))
plt.close()

# 3. Feature Importance
if hasattr(clf, "feature_importances_"):
    importances = clf.feature_importances_
    plt.figure(figsize=(8, 4))
    plt.bar(FEATURE_NAMES, importances, color='green')
    plt.title("Feature Importance")
    plt.ylabel("Importance")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, "feature_importance.png"))
    plt.close()

print(f"🖼️ Plots saved to {plot_path}")

# ========== LEARNING CURVE UPDATE ========== #
def update_learning_curve(models_dir="models", output_path="plots/learning_curve.png"):
    versions = sorted([
        d for d in os.listdir(models_dir)
        if d.startswith("v") and os.path.isdir(os.path.join(models_dir, d))
    ], key=lambda v: int(v[1:]))

    scores = []
    labels = []

    for v in versions:
        cfg_path = os.path.join(models_dir, v, "config.json")
        if os.path.exists(cfg_path):
            with open(cfg_path, "r") as f:
                cfg = json.load(f)
            score = cfg.get("f1_macro")
            if score is not None:
                labels.append(v)
                scores.append(score)

    if scores:
        plt.figure(figsize=(10, 5))
        plt.plot(labels, scores, marker='o', linestyle='-', color='blue')
        plt.title("Learning Curve (F1 Macro Score)")
        plt.xlabel("Model Version")
        plt.ylabel("F1 Macro Score")
        plt.ylim(0, 1.05)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"📈 Learning curve updated: {output_path}")
    else:
        print("⚠️ No valid training scores found to plot.")

# Run the updater at the end of training
update_learning_curve()
