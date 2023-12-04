import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants


class Seahorse(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Speed powerup for player
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_seahorse"]
        self.restart_timer = 0
        self.direction = random.choice([0, 1]) #move left: 0, move right: 1
        self.random_spawn = random.randrange(200, 500) #timer
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(50, SCREEN_HEIGHT-200))
    def update(self):
        self.restart_timer += 1
        if self.direction == 1:
            self.image = pygame.transform.flip(self.images["spr_seahorse"], 1, 0)
        else:
            self.image = self.images["spr_seahorse"]
        if self.restart_timer > self.random_spawn:
            if self.rect.topleft[0] == -70:
                self.direction = 1 #right
            elif self.rect.topleft[0] == SCREEN_WIDTH:
                self.direction = 0 #left
            if self.direction == 1: #right movements
                self.rect.topleft = self.rect.topleft[0]+3, self.rect.topleft[1]
            elif self.direction == 0: #left movements
                self.rect.topleft = self.rect.topleft[0]-3, self.rect.topleft[1]
            if(self.rect.topleft[0] < -60 and self.direction == 0): #restarts position
                self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                                     random.randrange(50, SCREEN_HEIGHT-200))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restart_timer = 0
                self.random_spawn = random.randrange(1500, 2000)
            elif(self.rect.topleft[0] > SCREEN_WIDTH-10 and self.direction == 1): #restarts position
                self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                                     random.randrange(50, SCREEN_HEIGHT-200))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restart_timer = 0
                self.random_spawn = random.randrange(1500, 2000)
    def collide_with_player(self):
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(50, SCREEN_HEIGHT-200))
        self.restart_timer = 0
    def remove_sprite(self):
        self.kill()