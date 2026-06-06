import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class UI:
    def __init__(self, font_size=32):
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", font_size)
        self.high_score_file = "highscore.txt"
        self.best_time_file = "besttime.txt"
        
        self.high_score = self.load_high_score()
        self.best_time = self.load_best_time()

    def load_high_score(self):
        if not os.path.exists(self.high_score_file):
            return 0
        with open(self.high_score_file, "r") as f:
            try:
                return int(f.read())
            except:
                return 0

    def load_best_time(self):
        if not os.path.exists(self.best_time_file):
            return 0.0
        with open(self.best_time_file, "r") as f:
            try:
                return float(f.read())
            except:
                return 0.0

    def save_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            with open(self.high_score_file, "w") as f:
                f.write(str(score))

    def save_best_time(self, current_time):
        if current_time > self.best_time:
            self.best_time = current_time
            with open(self.best_time_file, "w") as f:
                f.write(str(current_time))

    def draw(self, screen, score, lives, game_time):

        m, s = divmod(int(game_time), 60)
        bm, bs = divmod(int(self.best_time), 60)      

        score_surf = self.font.render(f"Score: {score}", True, "white")
        high_surf = self.font.render(f"High: {self.high_score}", True, (200, 200, 200))
        
        time_surf = self.font.render(f"Time: {m:02}:{s:02}", True, "white")
        best_surf = self.font.render(f"Best: {bm:02}:{bs:02}", True, (200, 200, 200))

        screen.blit(score_surf, (10, 10))
        screen.blit(high_surf, (10, 50))        

        heart_width = 24
        heart_height = 22
        gap = 12
        total_width = (lives * heart_width) + ((lives - 1) * gap)
        start_x = (SCREEN_WIDTH // 2) - (total_width // 2)
        
        for i in range(lives):
            x = start_x + (i * (heart_width + gap))
            y = 20
            
            points = [
                (x, y + heart_height // 2),
                (x + heart_width, y + heart_height // 2),
                (x + heart_width // 2, y + heart_height)
            ]
            pygame.draw.polygon(screen, "white", points)            
 
            circle_radius = heart_width // 4 + 1

            pygame.draw.circle(screen, "white", (x + circle_radius, y + circle_radius), circle_radius)

            pygame.draw.circle(screen, "white", (x + heart_width - circle_radius, y + circle_radius), circle_radius)       

        time_x = SCREEN_WIDTH - time_surf.get_width() - 10
        screen.blit(time_surf, (time_x, 10))
        
        best_x = SCREEN_WIDTH - best_surf.get_width() - 10
        screen.blit(best_surf, (best_x, 50))