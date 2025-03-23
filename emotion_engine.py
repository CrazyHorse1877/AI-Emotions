#Emotion Engine
#This module is responsible for evaluating the current emotional state of the agent based on its internal state and environment. The evaluate_emotion function takes the current state and context as input and returns the emotional state of the agent. The emotional state can be one of the following: Dead, Fearful, Hungry, Exhausted, Bored, Curious, or Idle. The emotional state is determined based on the following criteria:
#If the agent's health is zero, it is considered Dead.
#If the agent's fear level is greater than 60, it is considered Fearful.
#If the agent's hunger level is greater than 70, it is considered Hungry.
#If the agent's energy level is less than 20, it is considered Exhausted.
#If the agent's stimulation level is less than 20, it is considered Bored.
#If the novelty_trigger flag is set in the context, the agent is considered Curious.
#Otherwise, the agent is considered Idle.

def evaluate_emotion(state, context):
    """
    Determines the current emotional state based on internal state and environment.
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
