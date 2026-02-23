import pygame
import sys
import time
from src import CircleShape, Menu, Scoreboard
from src import log_state, log_event
from src.constants import *
from entities import Asteroid, AsteroidField, Debris, Player, Shot

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
    current_state = STATE_START
    player_alive = True
    player_death_timer = 3
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    scoreboard = Scoreboard(20, 20)
    start_menu = Menu("Asteroids", "Press SPACE to Start")
    game_over_screen = Menu("GAME OVER", "Press any key to Exit")

    # Game loop
    while True:
        # 1. HANDLE INPUT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if current_state == STATE_START:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    current_state = STATE_PLAYING
            elif current_state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    return
        # 2. UPDATE LOGIC:
        if current_state == STATE_PLAYING:
            log_state()
            for item in updatable:
                item.update(dt)
            if player_alive:
                for asteroid in asteroids:
                    if player.collides_with(asteroid):
                        player.die()
                        player_alive = False
                        current_state = STATE_GAME_OVER
                    for shot in shots:
                        if shot.collides_with(asteroid):
                            log_event("asteroid_shot")
                            shot.kill()
                            asteroid.split()
                            scoreboard.increase_score(100)
                            # Create an explosion effect:
                            for _ in range(10):
                                Debris(asteroid.position.x, asteroid.position.y)
            else:
                player_death_timer -= dt
                if player_death_timer <= 0:
                    sys.exit()
        # 3. DRAWING LOGIC:
        screen.fill("black")
        if current_state == STATE_START:
            start_menu.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif current_state == STATE_PLAYING:
            for item in drawable:
                item.draw(screen)
        elif current_state == STATE_GAME_OVER:
            game_over_screen.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
