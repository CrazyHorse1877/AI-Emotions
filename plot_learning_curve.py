import os
import json
import matplotlib.pyplot as plt

models_dir = "models"
versions = sorted([
    d for d in os.listdir(models_dir)
    if d.startswith("v") and os.path.isdir(os.path.join(models_dir, d))
], key=lambda v: int(v[1:]))

scores = []
labels = []

for v in versions:
    config_path = os.path.join(models_dir, v, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        score = config.get("f1_macro")
        if score is not None:
            scores.append(score)
            labels.append(v)

if scores:
    plt.figure(figsize=(10, 5))
    plt.plot(labels, scores, marker='o', linestyle='-', color='blue')
    plt.title("Learning Curve (F1 Macro Score)")
    plt.xlabel("Model Version")
    plt.ylabel("F1 Macro Score")
    plt.ylim(0, 1.05)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/learning_curve.png")
    plt.show()
    print("📈 Learning curve saved as plots/learning_curve.png")
else:
    print("No training scores found in config.json files.")
