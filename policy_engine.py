# policy_engine.py

def evaluate_policy(state, context):
    """
    Basic rule-based action selection from current state.
    """

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
