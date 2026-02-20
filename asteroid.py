from circleshape import CircleShape
from constants import *
from logger import log_event
import pygame
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            int(self.radius),
            LINE_WIDTH
        )
    
    def update(self, dt):
        self.position += (self.velocity * dt)
   
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            first_asteroid_vector = self.velocity.rotate(angle)
            second_asteroid_vector = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(
                int(self.position.x),
                int(self.position.y),
                int(new_radius)
            )
            asteroid2 = Asteroid(
                int(self.position.x),
                int(self.position.y),
                int(new_radius)
            )
            asteroid1.velocity = first_asteroid_vector * 1.2
            asteroid2.velocity = second_asteroid_vector * 1.2

