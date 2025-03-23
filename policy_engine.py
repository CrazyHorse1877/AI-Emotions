import os
import pickle

def find_latest_model(base_dir="models"):
    if not os.path.exists(base_dir):
        return None

    versions = [d for d in os.listdir(base_dir) if d.startswith("v") and os.path.isdir(os.path.join(base_dir, d))]
    versions.sort(key=lambda v: int(v[1:]), reverse=True)

    for version in versions:
        model_path = os.path.join(base_dir, version, "policy_model.pkl")
        if os.path.exists(model_path):
            return model_path

    return None

# Try to load the latest policy model
_policy_model = None
_model_path = find_latest_model()

if _model_path:
    with open(_model_path, "rb") as f:
        _policy_model = pickle.load(f)
    print(f"[POLICY] Loaded model from {_model_path}")
else:
    print("[POLICY] No trained model found — using fallback rules.")

def evaluate_policy(state, context):
    if _policy_model:
        features = [[
            state["hunger"],
            state["energy"],
            state["health"],
            state["stimulation"],
            state["fear_level"]
        ]]
        return _policy_model.predict(features)[0]

    # Fallback logic
    if state["health"] <= 0:
        return "do_nothing"
    if state["fear_level"] > 60 and context.get("predators_nearby", False):
        return "flee"
    if state["hunger"] > 70 and context.get("prey_visible", False):
        return "seek_food"
    if state["energy"] < 20:
        return "rest"
    if context.get("novelty_trigger", False):
        return "wander"
    return "idle"
