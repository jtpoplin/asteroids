from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT
from circleshape import CircleShape
from shot import Shot
from laser import Laser
import pygame

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.bomb_cooldown = 0
        self.laser_cooldown = 0
        self.explosion_visual_timer = 0
        self.hellfire_cooldown = 0
        self.hellfire_visual_timer = 0
        self.hellfire_points = []
    
    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 0)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt: float) -> None:
        self.cooldown -= dt
        self.bomb_cooldown -= dt
        self.laser_cooldown -= dt
        self.hellfire_cooldown -= dt
        if self.hellfire_visual_timer > 0:
            self.hellfire_visual_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_l]:
            self.shoot_laser()
        
        if self.explosion_visual_timer > 0:
            self.explosion_visual_timer -= dt

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
    
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    def shoot(self):
        if self.cooldown > 0:
            return
        else:
            self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        forward = pygame.Vector2(0, 1)
        rotated = forward.rotate(self.rotation)
        fast = rotated * PLAYER_SHOOT_SPEED
        shot.velocity = fast
    
    def can_bomb(self):
        return self.bomb_cooldown <= 0
    
    def reset_bomb_timer(self):
        self.bomb_cooldown = 5.0
    
    def shoot_laser(self):
        if self.laser_cooldown > 0:
            return
        self.laser_cooldown = 0.5
        laser = Laser(self.position.x, self.position.y)
        laser.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED * 1.5

    def can_hellfire(self):
        return self.hellfire_cooldown <= 0
    
    def reset_hellfire_timer(self):
        self.hellfire_cooldown = 15.0