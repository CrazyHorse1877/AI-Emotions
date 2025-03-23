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
        self.direction = pygame.Vector2(0, 0)

    def update(self, prey_list, predator_list):
        my_pos = pygame.Vector2(self.x, self.y)

        # Choose prey only if uniquely closest to it
        def is_my_target(prey):
            my_distance = my_pos.distance_to(prey.get_position())
            for other in predator_list:
                if other is self:
                    continue
                other_dist = pygame.Vector2(other.x, other.y).distance_to(prey.get_position())
                if other_dist < my_distance:
                    return False
            return True

        my_targets = [p for p in prey_list if is_my_target(p)]

        if my_targets:
            closest = min(my_targets, key=lambda p: my_pos.distance_to(p.get_position()))
            self.direction = (closest.get_position() - my_pos).normalize()
        else:
            if random.random() < 0.02:
                self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        # Move
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        # Clamp to screen
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
        
        self.current_target = closest if my_targets else None


    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius)

        # Draw targeting line if in debug mode
        if hasattr(self, "current_target") and self.current_target:
            start = (int(self.x), int(self.y))
            end = (int(self.current_target.x), int(self.current_target.y))
            pygame.draw.line(screen, (255, 100, 100), start, end, 1)

    def get_position(self):
        return pygame.Vector2(self.x, self.y)
