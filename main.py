import pygame
import sys
from constants import *
from logger import log_state
from logger import log_event
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from scoreboard import Scoreboard
from debris import Debris

def main():
    print("Starting Asteroids with pygame version: 2.6.1")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    
    # Creating containers for the different sprite groups:
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Setting each sprite group's containers:
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (drawable, updatable, shots)
    Scoreboard.containers = (drawable, updatable)
    Debris.containers = (drawable, updatable)
    
    # Variable initialization and object creation:
    dt = 0  
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    scoreboard = Scoreboard(20, 20)

    # Game loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for item in updatable:
            item.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    scoreboard.increase_score(100)
                    
                    # Create an explosion effect:
                    for _ in range(10):
                        Debris(asteroid.position.x, asteroid.position.y, DEBRIS_RADIUS)

        for item in drawable:
            item.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
