import pygame
from src.circleshape import CircleShape
from src.constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius=SHOT_RADIUS):
        super().__init__(x, y, SHOT_RADIUS)
    
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "red",
            (int(self.position.x), int(self.position.y)),
            SHOT_RADIUS,
            width=LINE_WIDTH
        )
        
    def update(self, dt):
        self.position += self.velocity * dt
