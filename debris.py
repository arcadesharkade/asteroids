import pygame
import random
from constants import *

class Debris(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        # Randomize direction and speed:
        direction = pygame.Vector2(0, 1).rotate(random.uniform(0, 360))
        speed = random.uniform(50, 150)
        self.velocity = direction * speed
        # How long the debris lasts in seconds:
        self.timer = random.uniform(0.2, 0.5)
        self.radius = DEBRIS_RADIUS

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            DEBRIS_RADIUS,
            LINE_WIDTH
        )

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
