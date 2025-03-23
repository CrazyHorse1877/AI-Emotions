# predator.py

import pygame
import random
from settings import *

class Predator:
    def __init__(self):
        self.radius = 10
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.colour = PREDATOR_COLOUR
        self.speed = 2

        self.target = None
        self.direction = pygame.Vector2(0, 0)

    def update(self, prey_list):
        # If no prey to chase, wander
        if prey_list:
            # Find the closest prey
            closest_prey = min(prey_list, key=lambda prey: pygame.Vector2(self.x, self.y).distance_to(prey.get_position()))
            prey_pos = closest_prey.get_position()
            direction = (prey_pos - pygame.Vector2(self.x, self.y))
            distance = direction.length()

            if distance != 0:
                self.direction = direction.normalize()
        else:
            # No prey — wander
            if random.random() < 0.02:  # occasionally change direction
                self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        # Move
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        # Bounce off walls
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.direction.x *= -1
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.direction.y *= -1


    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius)

    def get_position(self):
        return pygame.Vector2(self.x, self.y)
