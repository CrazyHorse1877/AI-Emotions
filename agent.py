# agent.py

import pygame
import random
from settings import *

class Agent:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = 12
        self.colour = TURTLE_COLOUR

        # Internal state
        self.hunger = 0         # 0 = full, 100 = starving
        self.health = 100
        self.emotion = "Idle"

        # Movement
        self.speed = 2
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        
        # Internal state
        self.hunger = 0         # 0 = full, 100 = starving
        self.health = 100
        self.energy = 100       # drains while moving or afraid
        self.stimulation = 50   # increases with novelty, decreases if doing same thing
        self.fear_level = 0     # 0–100, increases near predators

        # Emotion starts neutral
        self.emotion = "Idle"


    def update(self, prey_list, predator_list):
        # Hunger increases over time
        self.hunger += 0.1
        if self.hunger > 100:
            self.hunger = 100
            self.health -= 0.1  # Starving damages health

        # Energy slowly drains if moving or stressed
        if self.emotion in ["Hungry", "Fearful", "Curious"]:
            self.energy -= 0.2
        else:
            self.energy += 0.1  # Recovers when idle/sad

        self.energy = max(0, min(100, self.energy))

        # Stimulation decay
        self.stimulation -= 0.05
        self.stimulation = max(0, min(100, self.stimulation))

        # If completely drained, health decays slowly
        if self.energy <= 0:
            self.health -= 0.1

        # Determine emotional state (priority-based)
        if self.health <= 0:
            self.health = 0
            self.emotion = "Dead"
            self.speed = 0
            return  # Skip the rest of update logic


        elif self.fear_level > 60:
            self.emotion = "Fearful"

        elif self.hunger > 70:
            self.emotion = "Hungry"

        elif self.energy < 20:
            self.emotion = "Exhausted"

        elif self.stimulation < 20:
            self.emotion = "Bored"

        elif random.random() < 0.005:
            self.emotion = "Curious"

        else:
            self.emotion = "Idle"


            
        # Update colour based on emotion
        from settings import EMOTION_COLOURS
        self.colour = EMOTION_COLOURS.get(self.emotion, TURTLE_COLOUR)


        # Determine movement direction based on emotion
        if self.emotion == "Hungry" and prey_list:
            # Seek closest prey
            closest_prey = min(prey_list, key=lambda prey: pygame.Vector2(self.x, self.y).distance_to(prey.get_position()))
            direction = (closest_prey.get_position() - pygame.Vector2(self.x, self.y)).normalize()
            self.direction = direction

        elif self.emotion == "Fearful" and predator_list:
            # Move away from closest predator
            closest_pred = min(predator_list, key=lambda p: pygame.Vector2(self.x, self.y).distance_to(p.get_position()))
            direction = (pygame.Vector2(self.x, self.y) - closest_pred.get_position())
            if direction.length() > 0:
                self.direction = direction.normalize()

        elif self.emotion == "Curious":
            # Occasionally change direction
            if random.random() < 0.05:
                self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        # Idle/Sad: small random drift (less motivation)
        elif self.emotion in ["Idle", "Sad"]:
            if random.random() < 0.01:
                self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        
        # Bounce off and clamp to screen
        if self.x <= self.radius:
            self.x = self.radius
            self.direction.x *= -1
        elif self.x >= SCREEN_WIDTH - self.radius:
            self.x = SCREEN_WIDTH - self.radius
            self.direction.x *= -1

        if self.y <= self.radius:
            self.y = self.radius
            self.direction.y *= -1
        elif self.y >= SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius
            self.direction.y *= -1
            
        # Eat prey if close enough
        for prey in prey_list[:]:
            dist = pygame.Vector2(self.x, self.y).distance_to(prey.get_position())
            if dist < self.radius + prey.radius:
                # only eat if hungry
                if self.hunger < 50:
                    break
                # Eat the prey
                prey_list.remove(prey)
                self.hunger -= 20
                if self.hunger < 0:
                    self.hunger = 0
                self.stimulation += 10
                self.energy = min(100, self.energy + 10)
                break  # only eat one prey per frame

                    
        # Check for nearby predators
        for predator in predator_list:
            dist = pygame.Vector2(self.x, self.y).distance_to(predator.get_position())
            if dist < 100:
                self.fear_level = 100
                self.emotion = "Fearful"
                # Optional: move away
                direction_away = pygame.Vector2(self.x, self.y) - predator.get_position()
                if direction_away.length() > 0:
                    self.direction = direction_away.normalize()
                break  # no need to check more

        if dist < self.radius + predator.radius:
            self.health -= 0.5  # Predator attacks
        
        # Cool down fear level over time
        self.fear_level = max(0, self.fear_level - 1)


        # Apply movement
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed


    def draw(self, screen, font):
        # Draw agent
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius)

        # Draw emotion label
        label = font.render(self.emotion, True, (255, 255, 255))

        # Draw health bar
        bar_width = 40
        bar_height = 6
        health_ratio = self.health / 100
        health_bar_colour = (0, 255, 0) if self.health > 40 else (255, 165, 0) if self.health > 20 else (255, 0, 0)

        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.radius + 6

        # Background bar
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Health portion
        pygame.draw.rect(screen, health_bar_colour, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

        screen.blit(label, (self.x - 20, self.y - 25))
