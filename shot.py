from constants import LINE_WIDTH, SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from circleshape import CircleShape
import pygame

class Shot(CircleShape):

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
    
        # Clean up shots that leave the screen
        if (self.position.x > SCREEN_WIDTH or self.position.x < 0 or
            self.position.y > SCREEN_HEIGHT or self.position.y < 0):
            self.kill()