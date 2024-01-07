import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class StarPowerup(pygame.sprite.Sprite):
    OFF_SCREEN_RIGHT = SCREEN_WIDTH
    OFF_SCREEN_LEFT = -80  # Assuming the width of the sprite is less than 80
    BOTTOM_POSITION_Y = SCREEN_HEIGHT - 80  # Y-position near the bottom of the screen
    RESPAWN_TIMER = 1000  # Total interval before moving again
    ANIMATION_CYCLE_LENGTH = 30
    SPEED = 5
    DIRECTION_LEFT = -1
    DIRECTION_RIGHT = 1

    def __init__(self, allsprites, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["spr_star_1"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.timer = -StarPowerup.RESPAWN_TIMER
        self.star_animator = 0
        self.reset_position()

    def update(self):
        if not self.is_in_game_world():
            self.timer += 1

        self.star_animator = (self.star_animator + 1) % StarPowerup.ANIMATION_CYCLE_LENGTH
        self.update_animation()

        if self.timer >= 0 and self.timer < StarPowerup.RESPAWN_TIMER:
            self.move()

        if (self.direction == StarPowerup.DIRECTION_LEFT and self.rect.right < StarPowerup.OFF_SCREEN_LEFT) or \
           (self.direction == StarPowerup.DIRECTION_RIGHT and self.rect.left > StarPowerup.OFF_SCREEN_RIGHT):
            self.reset_position()
            
    def move(self):
        self.rect.x += StarPowerup.SPEED * self.direction

    def reset_position(self):
        self.direction = random.choice([StarPowerup.DIRECTION_LEFT, StarPowerup.DIRECTION_RIGHT])
        if self.direction == StarPowerup.DIRECTION_LEFT:
            self.rect.x = StarPowerup.OFF_SCREEN_RIGHT
        else:
            self.rect.x = StarPowerup.OFF_SCREEN_LEFT - self.rect.width  # Adjust for sprite width
        self.rect.y = StarPowerup.BOTTOM_POSITION_Y
        self.timer = -StarPowerup.RESPAWN_TIMER

    def update_animation(self):
        # Determine which frame of the animation to show
        frame = (self.star_animator // 10) % 3 + 1  # Cycles through frames 1-2-3
        self.image = self.images[f"spr_star_{frame}"]


    def collide_with_player(self):
        self.reset_position()
        
    def is_in_game_world(self):
        return self.rect.right > StarPowerup.OFF_SCREEN_LEFT and self.rect.left < StarPowerup.OFF_SCREEN_RIGHT

    def remove_sprite(self):
        self.kill()
