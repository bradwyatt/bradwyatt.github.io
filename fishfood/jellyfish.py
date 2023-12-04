import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class Jellyfish(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Slows down player temporarily for 5 seconds
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["spr_jellyfish"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.returnback = 0
        self.jellyfishtimer = 0
        self.jellyfishanimatetimer = 0
        self.jellyfishrandom_spawn = random.randrange(700, 900)
        self.newpos = self.rect.topleft[0], self.rect.topleft[1]
        self.jfstring = []
        self.activate = 0
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -50)
    def update(self):
        self.jellyfishanimatetimer += 1
        self.jfstring = [self.images["spr_jellyfish"], 
                         self.images["spr_jellyfish_2"],
                         self.images["spr_jellyfish_3"],
                         self.images["spr_jellyfish_4"], 
                         self.images["spr_jellyfish_5"], 
                         self.images["spr_jellyfish_6"],
                         self.images["spr_jellyfish_7"]]
        for i in range(2, 16, 2): #cycle through first 13 sprite animations
            if self.jellyfishanimatetimer >= i:
                self.image = self.jfstring[(i//2)-1]
        for i in range(18, 28, 2): #cycle through 13 sprite animations backwards
            if self.jellyfishanimatetimer > i:
                self.image = self.jfstring[((28-i)//2)+1]
        if self.jellyfishanimatetimer > 28:
            self.jellyfishanimatetimer = 1
        self.jellyfishtimer += 1
        if self.rect.topleft[1] == -50:
            self.returnback = 0
        if self.rect.topleft[1] > SCREEN_HEIGHT-80:
            #collide with BOTTOM wall
            self.returnback = 1
        if self.returnback == 0 and self.jellyfishtimer > self.jellyfishrandom_spawn:
            if self.activate:
                self.newpos = (self.rect.topleft[0], self.rect.topleft[1]+3)
                self.rect.topleft = self.newpos
        elif self.returnback == 1:
            self.newpos = (self.rect.topleft[0], self.rect.topleft[1]-3)
            self.rect.topleft = self.newpos
            if self.rect.topleft[1] < -32:
                self.jellyfishtimer = 0
                self.jellyfishrandom_spawn = random.randrange(500, 1200)
                self.rect.topleft = random.randrange(100, SCREEN_WIDTH-100), -50
    def collide_with_player(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -50)
        self.jellyfishtimer = 0
    def collide_with_bright_blue_fish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -50)
        self.jellyfishtimer = 0
    def remove_sprite(self):
        self.kill()
