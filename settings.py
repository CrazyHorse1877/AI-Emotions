# settings.py

SCREEN_WIDTH = 1280 
SCREEN_HEIGHT = 720
FPS = 60

BG_COLOUR = (30, 30, 30)  # dark background

# Colours
TURTLE_COLOUR = (0, 100, 255)
PREY_COLOUR = (0, 255, 100)
PREDATOR_COLOUR = (255, 50, 50)

# Emotion colours for the agent
EMOTION_COLOURS = {
    "Idle": (0, 100, 255),
    "Hungry": (255, 165, 0),    # orange
    "Sad": (100, 100, 255),     # bluish
    "Curious": (255, 255, 0),   # yellow
    "Fearful": (255, 0, 0),     # red
    "Excited": (0, 255, 255),   # cyan (optional for later)
    "Dead": (100, 100, 100),
    "Exhausted": (150, 0, 255),
    "Bored": (180, 180, 0)
}
