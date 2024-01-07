import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants


class Seahorse(pygame.sprite.Sprite):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    OFF_SCREEN_LEFT = -70
    OFF_SCREEN_RIGHT = SCREEN_WIDTH
    MIN_SPAWN_TIME = 1500
    MAX_SPAWN_TIME = 2000

    def __init__(self, allsprites, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["spr_seahorse"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.reset_position()
        self.set_random_spawn_time()

    def update(self):
        self.restart_timer += 1

        if self.restart_timer >= self.random_spawn:
            self.move()
            self.check_bounds_and_reset()

        self.update_image()

    def update_image(self):
        if self.direction == Seahorse.MOVE_RIGHT:
            self.image = pygame.transform.flip(self.images["spr_seahorse"], True, False)
        else:
            self.image = self.images["spr_seahorse"]

    def move(self):
        move_amount = 3 if self.direction == Seahorse.MOVE_RIGHT else -3
        self.rect.topleft = self.rect.topleft[0] + move_amount, self.rect.topleft[1]

    def check_bounds_and_reset(self):
        out_of_bounds_left = self.rect.left < Seahorse.OFF_SCREEN_LEFT and self.direction == Seahorse.MOVE_LEFT
        out_of_bounds_right = self.rect.right > Seahorse.OFF_SCREEN_RIGHT and self.direction == Seahorse.MOVE_RIGHT

        if out_of_bounds_left or out_of_bounds_right:
            self.reset_position()
            self.set_random_spawn_time()

    def reset_position(self):
        self.rect.topleft = (random.choice([Seahorse.OFF_SCREEN_LEFT, Seahorse.OFF_SCREEN_RIGHT]),
                             random.randrange(50, SCREEN_HEIGHT - 200))
        self.direction = Seahorse.MOVE_RIGHT if self.rect.left == Seahorse.OFF_SCREEN_LEFT else Seahorse.MOVE_LEFT
        self.restart_timer = 0  # Reset the timer

    def set_random_spawn_time(self):
        self.random_spawn = random.randrange(Seahorse.MIN_SPAWN_TIME, Seahorse.MAX_SPAWN_TIME)

    def collide_with_player(self):
        self.reset_position()

    def remove_sprite(self):
        self.kill()
