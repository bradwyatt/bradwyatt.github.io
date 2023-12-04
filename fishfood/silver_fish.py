import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants


class SilverFish(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Whem eaten, higher amount of points, but shows up infrequently
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_silver_fish"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
        self.restart_timer = 0
        self.direction = random.choice([0, 1]) #right or left
        allsprites.add(self)
    def update(self):
        self.restart_timer += 1
        if self.restart_timer > 250:
            if self.rect.topleft[0] == -50:
                self.direction = 1 # right
            elif self.rect.topleft[0] == SCREEN_WIDTH:
                self.direction = 0 # left
            if self.direction == 1: # right movements
                self.rect.topleft = self.rect.topleft[0]+3, self.rect.topleft[1]
                self.image = self.images["spr_silver_fish"]
            elif self.direction == 0: # left movements
                self.rect.topleft = self.rect.topleft[0]-3, self.rect.topleft[1]
                self.image = pygame.transform.flip(self.images["spr_silver_fish"], 1, 0)
            if(self.rect.topleft[0] < -40 and self.direction == 0): #restarts position
                self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restart_timer = 0
            elif(self.rect.topleft[0] > SCREEN_WIDTH-10 and self.direction == 1): #restarts position
                self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restart_timer = 0
    def collide_with_player(self):
        self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
        self.restart_timer = 0
    def collide_with_bright_blue_fish(self):
        self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
        self.restart_timer = 0
    def remove_sprite(self):
        self.kill()