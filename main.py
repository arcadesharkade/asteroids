import pygame
import sys
import time
from src import CircleShape, Menu, Scoreboard
from src import log_state, log_event
from src.constants import *
from entities import Asteroid, AsteroidField, Debris, Player, Shot

def main():
    # 1. Initialization
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    print("Starting Asteroids with pygame version: 2.6.1")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # 2. Set up Groups and Entities
    updatable, drawable, asteroids, shots = setup_groups() 
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    scoreboard = Scoreboard(20, 20)
    start_menu = Menu("Asteroids", "Press SPACE to Start")
    game_over_screen = Menu("GAME OVER", "Press any key to Exit")
    game_state = {
        "current": STATE_START,
        "player_alive": True,
        "death_timer": 3,
        "score": 0
    }

    # 3. The Game Loop
    while True:
        # 1. Inputs
        game_state["current"] = handle_events(game_state["current"])
        
        # 2. Logic and Physics
        update_entities(game_state, updatable, dt)
        
        check_collisions(game_state, player, asteroids, shots, scoreboard)
        
        render_screen(screen, drawable, game_state, start_menu, game_over_screen)

        dt = clock.tick(60) / 1000

# --- Helper Functions --- 

def setup_groups():
    # Create containers for the different sprite groups:
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Link groups to classes:
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (drawable, updatable, shots)
    Scoreboard.containers = (drawable, updatable)
    Debris.containers = (drawable, updatable)
    
    return updatable, drawable, asteroids, shots

def handle_events(current_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if current_state == STATE_START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return STATE_PLAYING
        elif current_state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                sys.exit()
    return current_state

def update_entities(game_state, updatable, dt):
    for obj in updatable:
        obj.update(dt)
    if game_state["player_alive"] == False:
        game_state["death_timer"] -= dt
    if game_state["death_timer"] <= 0:
        sys.exit()

def check_collisions(game_state, player, asteroids, shots, scoreboard):
    if not game_state["player_alive"]:
        return
    for asteroid in asteroids:
        if player.collides_with(asteroid):
            handle_player_death(game_state, player)
            return
        for shot in shots:
            if shot.collides_with(asteroid):
                handle_asteroid_destruction(asteroid, shot, scoreboard)

def render_screen(screen, drawable, game_state, start_menu, game_over_screen):
    screen.fill("black")
    if game_state["current"] == STATE_START:
        start_menu.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    elif game_state["current"] == STATE_PLAYING:
        for item in drawable:
            item.draw(screen)
    elif game_state["current"] == STATE_GAME_OVER:
        game_over_screen.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.flip()

def handle_player_death(game_state, player):
    player.die()
    game_state["player_alive"] = False
    game_state["current"] = STATE_GAME_OVER
    log_event("player_died")

def handle_asteroid_destruction(asteroid, shot, scoreboard):
    log_event("asteroid_shot")
    shot.kill()
    asteroid.split()
    scoreboard.increase_score(100)
    # Create an explosion effect:
    for _ in range(10):
        Debris(asteroid.position.x, asteroid.position.y)


if __name__ == "__main__":
    main()
