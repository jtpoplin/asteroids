import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_SPAWN_RATE_SECONDS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from ui import UI
from laser import Laser
import sys
import random

def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    bg_image = pygame.image.load("asteroidslogo.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    dimmer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dimmer.set_alpha(200) 
    dimmer.fill((0, 0, 0))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Laser.containers = (shots, updatable, drawable)

    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    ui = UI(35)
    game_time = 0.0
    score = 0
    lives = 3
    dt = 0.0
    clock = pygame.time.Clock()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)
        game_time += dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_k] and player.can_bomb():
            player.reset_bomb_timer()
            player.explosion_visual_timer = 0.3
            explosion_radius = 200
            for asteroid in list(asteroids):
                if player.position.distance_to(asteroid.position) < explosion_radius + asteroid.radius:
                    asteroid.kill()
                    score += 50

        if keys[pygame.K_j] and player.can_hellfire():
            player.reset_hellfire_timer()
            player.hellfire_visual_timer = 0.5
            player.hellfire_points = []
            for _ in range(4):                
                rand_x = random.randint(0, SCREEN_WIDTH)
                rand_y = random.randint(0, SCREEN_HEIGHT)
                point = pygame.Vector2(rand_x, rand_y)
                player.hellfire_points.append(point)
                explosion_radius = 250 # Even bigger than the bomb!
                for asteroid in list(asteroids):
                    if point.distance_to(asteroid.position) < explosion_radius + asteroid.radius:
                        asteroid.kill() # Total destruction
                        score += 25 
        
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                lives -=1
                if lives <= 0:
                    print("Game over!")
                    ui.save_high_score(score)
                    ui.save_best_time(game_time)
                    sys.exit()
                else:
                    print(f"Lives left: {lives}")
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    for a in asteroids:
                        a.kill()
                    break 

            
            for shot in shots:
                if shot.collides_with(asteroid):
                    if shot.alive():
                        log_event("asteroid_shot")
                        if not isinstance(shot, Laser):
                            shot.kill()
                        asteroid.split()
                        score += 100

        new_rate = ASTEROID_SPAWN_RATE_SECONDS - (score / 1000 * 0.1)
        asteroid_field.spawn_rate = max(0.3, new_rate)
        
        screen.blit(bg_image, (0, 0))
        screen.blit(dimmer, (0, 0))

        for draw in drawable:
            draw.draw(screen)
        

        if player.explosion_visual_timer > 0:
            if int(player.explosion_visual_timer * 50) % 2 == 0:
                pygame.draw.circle(screen, (255, 255, 0), player.position, 200, 4)
                pygame.draw.circle(screen, (255, 165, 0), player.position, 100, 2)

        if player.hellfire_visual_timer > 0:
            if int(player.hellfire_visual_timer * 40) % 2 == 0:
                for point in player.hellfire_points:
                    pygame.draw.circle(screen, (255, 0, 0), point, 250, 5)
                    pygame.draw.circle(screen, (255, 69, 0), point, 125, 3)
        
        ui.draw(screen, score, lives, game_time)

        pygame.display.flip()
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
