# emotion_engine.py

def evaluate_emotion(state, context):
    """
    Determines the agent's current emotional state based on internal state and context.

    Args:
        state (dict): {
            "hunger": float (0-100),
            "energy": float (0-100),
            "health": float (0-100),
            "stimulation": float (0-100),
            "fear_level": float (0-100)
        }
        context (dict): {
            "novelty_trigger": bool
        }

    Returns:
        str: Emotion label
    """

    if state["health"] <= 0:
        return "Dead"

    if state["fear_level"] > 60:
        return "Fearful"

    if state["hunger"] > 70:
        return "Hungry"

    if state["energy"] < 20:
        return "Exhausted"

    if state["stimulation"] < 20:
        return "Bored"

    if context.get("novelty_trigger", False):
        return "Curious"

    return "Idle"
