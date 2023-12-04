import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants


class BrightBlueFish(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Biggest predator in the game, eats everything that comes in contact
        Player can avoid if they have a star powerup
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_bright_blue_fish"]
        self.direction = random.choice([0, 1]) #move left: 0, move right: 1
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.activate = 0
        self.rect.topleft = (random.choice([-1000, SCREEN_WIDTH+1000]),
                             random.randrange(50, SCREEN_HEIGHT-200))
        self.arrow_warning = 0
    def update(self):
        if self.activate == 1:
            self.arrow_warning = 1
            if self.direction == 1:
                self.image = self.images["big_bright_blue_fish"]
            elif self.direction == 0:
                self.image = self.images["big_bright_blue_fish_left"]
            if self.direction == 1 and self.activate == 1: #right movements
                self.rect.topleft = self.rect.topleft[0]+4, self.rect.topleft[1]
                if self.rect.right > -200: # Remove arrow
                    self.arrow_warning = 0
                if self.rect.left > SCREEN_WIDTH: # Past right side of screen
                    self.activate = 0
            elif self.direction == 0 and self.activate == 1: #left movements
                self.rect.topleft = self.rect.topleft[0]-4, self.rect.topleft[1]
                if self.rect.left <= SCREEN_WIDTH:
                    self.arrow_warning = 0
                if self.rect.right < -300: # Past left side of screen
                    self.activate = 0

        else:
            self.image = self.images["spr_bright_blue_fish"]
    def remove_sprite(self):
        self.kill()