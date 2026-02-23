import pygame

class Menu:
    def __init__(self, text, subtext=None):
        self.font_main = pygame.font.Font(None, 72)
        self.font_sub = pygame.font.Font(None, 36)
        self.text = text
        self.subtext = subtext

    def draw(self, screen, width, height):
        # Render and center the main text
        main_surf = self.font_main.render(self.text, True, (255,255,255))
        main_rect = main_surf.get_rect(center=(width // 2, height // 2))
        screen.blit(main_surf, main_rect)
        
        if self.subtext:
            # Render subtext
            sub_surf = self.font_sub.render(self.subtext, True, (200, 200, 200))
            sub_rect = sub_surf.get_rect(center=(width // 2, height // 2 + 60))
            screen.blit(sub_surf, sub_rect)
