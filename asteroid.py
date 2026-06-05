from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from circleshape import CircleShape
from logger import log_event
import pygame, random

class Asteroid(CircleShape):

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.points_count = random.randint(8, 12)
        self.offsets = []
        for _ in range(self.points_count):
            self.offsets.append(random.uniform(0.7, 1.0))
    
    def draw(self, screen):
        polygon_points = []
        for i in range(self.points_count):
            angle = (i / self.points_count) * 360
            point_dist = self.radius * self.offsets[i]
            vector = pygame.Vector2(0, point_dist).rotate(angle)
            polygon_points.append(self.position + vector)
        pygame.draw.polygon(screen, "white", polygon_points, 2)
 
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)

        # Check the Right edge
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        # Check the Left edge
        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius

        # Check the Bottom edge
        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

        # Check the Top edge
        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)
        new_radius = (self.radius - ASTEROID_MIN_RADIUS)
        new_asteroid_one = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_one.velocity = new_velocity1 * 1.2
        new_asteroid_two = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_two.velocity = new_velocity2 * 1.2