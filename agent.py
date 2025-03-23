import pygame
import random
from settings import *
from emotion_engine import evaluate_emotion

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

        # Behavioural state
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.speed = 0
        self.emotion = "Idle"

    def update(self, prey_list, predator_list):
        # Increment internal changes
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
        if self.health <= 0:
            self.health = 0
            self.emotion = "Dead"
            self.speed = 0
            return

        # Detect predators
        for predator in predator_list:
            dist = pygame.Vector2(self.x, self.y).distance_to(predator.get_position())
            if dist < 100:
                self.fear_level = 100
                break

        # Emotion calculation via engine
        state = {
            "hunger": self.hunger,
            "energy": self.energy,
            "health": self.health,
            "stimulation": self.stimulation,
            "fear_level": self.fear_level
        }
        context = {
            "novelty_trigger": random.random() < 0.005
        }
        self.emotion = evaluate_emotion(state, context)

        # Speed by emotion
        self.speed = {
            "Dead": 0,
            "Fearful": 2.5,
            "Hungry": 2,
            "Exhausted": 0.2,
            "Bored": 0.5,
            "Curious": 1,
            "Idle": 0
        }.get(self.emotion, 1)

        # Update colour
        self.colour = EMOTION_COLOURS.get(self.emotion, TURTLE_COLOUR)

        # Direction by emotion
        if self.emotion == "Hungry" and prey_list:
            closest_prey = min(prey_list, key=lambda p: pygame.Vector2(self.x, self.y).distance_to(p.get_position()))
            self.direction = (closest_prey.get_position() - pygame.Vector2(self.x, self.y)).normalize()

        elif self.emotion == "Fearful" and predator_list:
            closest_pred = min(predator_list, key=lambda p: pygame.Vector2(self.x, self.y).distance_to(p.get_position()))
            away = (pygame.Vector2(self.x, self.y) - closest_pred.get_position())
            if away.length() > 0:
                self.direction = away.normalize()

        elif self.emotion == "Curious" and random.random() < 0.05:
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        elif self.emotion in ["Idle", "Sad"] and random.random() < 0.01:
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        # Boundary clamp
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
                    break

        # Take damage from predator
        for predator in predator_list:
            if pygame.Vector2(self.x, self.y).distance_to(predator.get_position()) < self.radius + predator.radius:
                self.health -= 0.5

        # Cool down fear
        self.fear_level = max(0, self.fear_level - 1)

        # Move
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self, screen, font):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius)
        label = font.render(self.emotion, True, (255, 255, 255))
        screen.blit(label, (self.x - 20, self.y - 25))

        bar_width = 40
        bar_height = 6
        health_ratio = self.health / 100
        colour = (0, 255, 0) if self.health > 40 else (255, 165, 0) if self.health > 20 else (255, 0, 0)
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.radius + 6
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, colour, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
