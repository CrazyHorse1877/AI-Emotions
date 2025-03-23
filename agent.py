import pygame
import random
import json
import math
from settings import *
from emotion_engine import evaluate_emotion
from policy_engine import evaluate_policy

class Agent:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = 12
        self.colour = TURTLE_COLOUR

        # Internal state
        self.hunger = 0
        self.health = 100
        self.energy = 100
        self.stimulation = 50
        self.fear_level = 0

        # Behaviour
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.speed = 0
        self.emotion = "Idle"
        self.action = "idle"

        # Tracking
        self.prev_emotion = "Idle"
        self.emotion_log = []
        self.action_log = []
        self.frame_count = 0

        self.last_health = self.health
        self.last_energy = self.energy

    def update(self, prey_list, predator_list):
        self.frame_count += 1

        # Internal updates
        self.hunger = min(100, self.hunger + 0.1)
        if self.hunger >= 100:
            self.health -= 0.1

        if self.emotion in ["Hungry", "Fearful", "Curious"]:
            self.energy -= 0.2
        else:
            self.energy += 0.1
        self.energy = max(0, min(100, self.energy))
        self.stimulation = max(0, self.stimulation - 0.05)

        if self.energy <= 0:
            self.health -= 0.1

        if self.hunger >= 50 and self.action in ["idle", "rest"]:
            self.health = min(100, self.health + 0.5)

        if self.health <= 0:
            self.health = 0
            self.emotion = "Dead"
            self.speed = 0
            return

        # Detect predators
        predators_nearby = any(
            pygame.Vector2(self.x, self.y).distance_to(p.get_position()) < 100
            for p in predator_list
        )
        if predators_nearby:
            self.fear_level = 100

        # State and context
        state = {
            "hunger": self.hunger,
            "energy": self.energy,
            "health": self.health,
            "stimulation": self.stimulation,
            "fear_level": self.fear_level
        }
        context = {
            "novelty_trigger": random.random() < 0.005,
            "prey_visible": bool(prey_list),
            "predators_nearby": predators_nearby
        }

        # Step 1: Emotion
        new_emotion = evaluate_emotion(state, context)
        if new_emotion != self.prev_emotion:
            self.emotion_log.append({
                "frame": self.frame_count,
                "from": self.prev_emotion,
                "to": new_emotion,
                "state": state.copy()
            })
            self.prev_emotion = new_emotion
        self.emotion = new_emotion

        # Step 2: Action
        self.action = evaluate_policy(state, context)

        # Step 3: Reward
        reward = 0
        if self.health > self.last_health:
            reward += 1
        if self.health < self.last_health:
            reward -= 1
        if self.energy < self.last_energy:
            reward -= 0.5

        self.last_health = self.health
        self.last_energy = self.energy

        self.action_log.append({
            "frame": self.frame_count,
            "state": state.copy(),
            "emotion": self.emotion,
            "action": self.action,
            "reward": reward
        })

        # Step 4: Speed
        self.speed = {
            "flee": 2.5,
            "seek_food": 2,
            "rest": 0,
            "wander": 1,
            "idle": 0.2,
            "do_nothing": 0
        }.get(self.action, 1)

        # Smarter prey targeting
        def is_safe_prey(prey, predators, radius=80):
            return all(pygame.Vector2(prey.x, prey.y).distance_to(p.get_position()) > radius for p in predators)

        nearest_prey = None
        nearest_distance = float('inf')

        for prey in prey_list:
            if not is_safe_prey(prey, predator_list):
                continue
            distance = pygame.Vector2(self.x, self.y).distance_to(prey.get_position())
            if distance < nearest_distance:
                nearest_prey = prey
                nearest_distance = distance

        # Step 5: Direction logic
        if self.action == "seek_food" and nearest_prey:
            direction = (pygame.Vector2(nearest_prey.x, nearest_prey.y) - pygame.Vector2(self.x, self.y)).normalize()
            jitter = pygame.Vector2(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2))
            self.direction = (direction + jitter).normalize()

        elif self.action == "flee" and predator_list:
            closest = min(predator_list, key=lambda p: pygame.Vector2(self.x, self.y).distance_to(p.get_position()))
            away = pygame.Vector2(self.x, self.y) - closest.get_position()
            self.direction = away.normalize() if away.length() > 0 else self.direction

        elif self.action == "wander" and random.random() < 0.05:
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        elif self.action in ["idle", "rest"] and random.random() < 0.01:
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        # Bounds
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.direction.x *= -1
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.direction.y *= -1

        # Eat prey
        for prey in prey_list[:]:
            if pygame.Vector2(self.x, self.y).distance_to(prey.get_position()) < self.radius + prey.radius:
                if self.hunger >= 50:
                    prey_list.remove(prey)
                    self.hunger = max(0, self.hunger - 20)
                    self.stimulation = min(100, self.stimulation + 10)
                    self.energy = min(100, self.energy + 10)
                    self.action_log[-1]["reward"] += 2
                    break

        # Predator contact
        for predator in predator_list:
            if pygame.Vector2(self.x, self.y).distance_to(predator.get_position()) < self.radius + predator.radius:
                self.health -= 0.5

        self.fear_level = max(0, self.fear_level - 1)

        # Move
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))


        # Colour
        self.colour = EMOTION_COLOURS.get(self.emotion, TURTLE_COLOUR)

    def draw(self, screen, font):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius)
        label = font.render(f"{self.emotion} / {self.action}", True, (255, 255, 255))
        screen.blit(label, (self.x - 20, self.y - 25))

        # Health bar
        bar_width = 40
        bar_height = 6
        health_ratio = self.health / 100
        colour = (0, 255, 0) if self.health > 40 else (255, 165, 0) if self.health > 20 else (255, 0, 0)
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.radius + 6
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, colour, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

    def save_action_log(self, filename="agent_log.json"):
        with open(filename, 'w') as f:
            json.dump(self.action_log, f, indent=2)
        print(f"[LOG] Saved action log with {len(self.action_log)} entries to '{filename}'")
