from constants import LINE_WIDTH, SHOT_RADIUS
from circleshape import CircleShape
import pygame

class Shot(CircleShape):

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)