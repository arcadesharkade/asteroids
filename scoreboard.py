import pygame

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.x = x
        self.y = y
        self.rebuild_surface()

    def rebuild_surface(self):
        # This creates the image that the 'drawable' group will blit to the screen
        self.image = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        pass

    def increase_score(self, amount):
        self.score += amount
        self.rebuild_surface()
