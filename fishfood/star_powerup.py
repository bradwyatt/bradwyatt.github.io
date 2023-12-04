import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants


class StarPowerup(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Player becomes invincible for period of time
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_star"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.star_animator = 0
        self.spawn_timer = 0
        self.pos = (SCREEN_WIDTH, SCREEN_HEIGHT-80) # Out of screen
        self.rect.topleft = self.pos
    def update(self):
        self.spawn_timer += 1
        self.star_animator += 1
        self.rect.topleft = (self.pos[0], self.pos[1])
        if self.spawn_timer == 2600: # Reset position, timer to 0
            self.pos = (SCREEN_WIDTH, SCREEN_HEIGHT-80)
            self.spawn_timer = 0
        elif self.spawn_timer > 1500: # Respawn
            self.pos = (self.pos[0]-5, SCREEN_HEIGHT-80)
            if self.star_animator > 0:
                self.image = self.images["spr_star"]
            if self.star_animator > 10:
                self.image = self.images["spr_star_2"]
            if self.star_animator > 20:
                self.image = self.images["spr_star_3"]
            if self.star_animator > 30:
                self.image = self.images["spr_star_2"]
            if self.star_animator > 40:
                self.star_animator = 0
    def collide_with_player(self):
        self.pos = (SCREEN_WIDTH, SCREEN_HEIGHT-80)
        self.spawn_timer = 0
    def remove_sprite(self):
        self.kill()