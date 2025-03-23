# policy_engine.py

import os
import pickle

MODEL_PATH = "policy_model.pkl"
_policy_model = None

# Load model at module level
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        _policy_model = pickle.load(f)
        print(f"[POLICY] Loaded trained model from {MODEL_PATH}")
else:
    print(f"[POLICY] No model found — using fallback rules.")

def evaluate_policy(state, context):
    """
    Chooses an action based on agent state.
    If model is loaded, use it. Otherwise, fall back to rules.
    """
    if _policy_model:
        features = [[
            state["hunger"],
            state["energy"],
            state["health"],
            state["stimulation"],
            state["fear_level"]
        ]]
        return _policy_model.predict(features)[0]

    # Fallback rule-based policy
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
