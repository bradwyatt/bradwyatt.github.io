import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class Shark(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Most frequently-seen predator in the game.
        Starts coming from above and then bounces around the room
        Only time player can avoid:
        When player has a star powerup, shark respawns
        When player has mini shark powerup, they can eat sharks
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["spr_shark"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.direction = (random.choice([-3, 3]), random.choice([-3, 3]))
        self.mini_shark = 0
        self.activate = 0
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -400)
        self.arrow_warning = 0
    def update(self):
        if self.rect.topleft[1] < 0:
            if self.activate == 1:
                self.rect.topleft = (self.rect.topleft[0], self.rect.topleft[1]+3)
                self.arrow_warning = 1
        else:
            self.arrow_warning = 0
            newpos = (self.rect.topleft[0] + self.direction[0],
                      self.rect.topleft[1] + self.direction[1])
            self.rect.topleft = newpos
        if self.mini_shark == 1:
            self.image = pygame.transform.smoothscale(self.image, (60, 30))
        else:
            self.image = self.images["spr_shark"]
    def collision_with_wall(self, rect):
        if self.rect.colliderect(rect):
            if self.rect.left < 32: #left walls
                self.direction = (3, random.choice([-3, 3]))
            elif self.rect.top > SCREEN_HEIGHT-64: #bottom walls
                self.direction = (random.choice([-3, 3]), -3)
            elif self.rect.right > SCREEN_WIDTH-32: #right walls
                self.direction = (-3, random.choice([-3, 3]))
            elif self.rect.top < 32: #top walls
                self.direction = (random.choice([-3, 3]), 3)
    def collide_with_bright_blue_fish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -100)
    def collide_with_player(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -100)
    def remove_sprite(self):
        self.kill()
