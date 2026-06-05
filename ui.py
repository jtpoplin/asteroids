import pygame
import os
from constants import SCREEN_WIDTH

class UI:
    def __init__(self, font_size=32):
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", font_size)
        self.high_score_file = "highscore.txt"
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if not os.path.exists(self.high_score_file):
            return 0
        with open(self.high_score_file, "r") as f:
            try:
                return int(f.read())
            except:
                return 0

    def save_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            with open(self.high_score_file, "w") as f:
                f.write(str(score))

    def draw(self, screen, score, lives):
        score_surface = self.font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_surface = self.font.render(f"High: {self.high_score}", True, (200, 200, 200))
        lives_surface = self.font.render(f"Lives: {lives}", True, (255, 255, 255))
        
        screen.blit(score_surface, (10, 10))
        screen.blit(high_score_surface, (10, 50)) # Draw below current score
        
        lives_x = SCREEN_WIDTH - lives_surface.get_width() - 10
        screen.blit(lives_surface, (lives_x, 10))