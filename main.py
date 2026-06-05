import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_SPAWN_RATE_SECONDS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from ui import UI
import sys

def main() -> None:
    pygame.init()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    ui = UI(35)

    score = 0
    lives = 3

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0.0


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                lives -=1
                if lives <= 0:
                    print("Game over!")
                    ui.save_high_score(score)
                    sys.exit()
                else:
                    print(f"Lives left: {lives}")
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    for a in asteroids:
                        a.kill()
                    break 

            
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

                    score += 100

        new_rate = ASTEROID_SPAWN_RATE_SECONDS - (score / 1000 * 0.1)
        asteroid_field.spawn_rate = max(0.3, new_rate)
        
        screen.fill("black")
        for draw in drawable:
            draw.draw(screen) 

        ui.draw(screen, score, lives)

        pygame.display.flip()
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
