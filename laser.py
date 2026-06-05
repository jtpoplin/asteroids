import pygame
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Laser(CircleShape):
    def __init__(self, x, y):
        # Increase the collision radius slightly if you want it to be easier to hit
        super().__init__(x, y, 4)

    def draw(self, screen):
        direction = self.velocity.normalize()
        tail_length = 20
        start_point = self.position
        end_point = self.position - (direction * tail_length)

        pygame.draw.line(screen, (255, 0, 0), start_point, end_point, 5)
        pygame.draw.line(screen, (255, 255, 255), start_point, end_point, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        if (self.position.x > SCREEN_WIDTH or self.position.x < 0 or
            self.position.y > SCREEN_HEIGHT or self.position.y < 0):
            self.kill()