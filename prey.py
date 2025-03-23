# prey.py

import pygame
import random
from settings import *

class Prey:
    def __init__(self):
        self.radius = 6
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.colour = PREY_COLOUR

        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.speed = 1.5
        self.breed_timer = random.randint(300, 600)  # frames (~5–10 sec at 60 FPS)


    def update(self, prey_list):
        # Movement
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        # Bounce off walls
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.direction.x *= -1
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.direction.y *= -1

        # Breeding logic
        self.breed_timer -= 1
        if self.breed_timer <= 0 and len(prey_list) < 100:
            prey_list.append(self.spawn_child())
            self.breed_timer = random.randint(300, 600)

    def spawn_child(self):
        child = Prey()
        # Spawn near current position
        child.x = min(max(self.x + random.randint(-15, 15), child.radius), SCREEN_WIDTH - child.radius)
        child.y = min(max(self.y + random.randint(-15, 15), child.radius), SCREEN_HEIGHT - child.radius)
        return child

    

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius)

    def get_position(self):
        return pygame.Vector2(self.x, self.y)
