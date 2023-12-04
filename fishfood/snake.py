import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants


class Snake(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Snake bite causes player to downsize to the original size
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_snake"]
        self.restart_timer = 0
        self.direction = random.choice([0, 1]) #move left: 0, move right: 1
        self.rect = self.image.get_rect()
        self.snake_player_animate_timer = 0
        self.random_spawn = random.randrange(200, 400)
        allsprites.add(self)
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
    def update(self):
        self.snake_player_animate_timer += 1
        if self.direction == 0: #go left
            if self.snake_player_animate_timer > 5:
                self.image = self.images["spr_snake_2"]
            if self.snake_player_animate_timer > 10:
                self.image = self.images["spr_snake_3"]
            if self.snake_player_animate_timer > 15:
                self.image = self.images["spr_snake_4"]
            if self.snake_player_animate_timer > 20:
                self.image = self.images["spr_snake"]
                self.snake_player_animate_timer = 0
        elif self.direction == 1: #go right
            if self.snake_player_animate_timer > 5:
                self.image = pygame.transform.flip(self.images["spr_snake_2"], 1, 0)
            if self.snake_player_animate_timer > 10:
                self.image = pygame.transform.flip(self.images["spr_snake_3"], 1, 0)
            if self.snake_player_animate_timer > 15:
                self.image = pygame.transform.flip(self.images["spr_snake_4"], 1, 0)
            if self.snake_player_animate_timer > 20:
                self.image = pygame.transform.flip(self.images["spr_snake"], 1, 0)
                self.snake_player_animate_timer = 0
        self.restart_timer += 1
        if self.restart_timer > self.random_spawn:
            if self.rect.topleft[0] == -70:
                self.direction = 1 #right
            elif self.rect.topleft[0] == SCREEN_WIDTH:
                self.direction = 0 #left
            if self.direction == 1: #right movements
                self.rect.topleft = self.rect.topleft[0]+2, self.rect.topleft[1]
            elif self.direction == 0: #left movements
                self.rect.topleft = self.rect.topleft[0]-2, self.rect.topleft[1]
            if(self.rect.topleft[0] < -60 and self.direction == 0): #restarts position
                self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                                     random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restart_timer = 0
            elif(self.rect.topleft[0] > SCREEN_WIDTH-10 and self.direction == 1): #restarts position
                self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                                     random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restart_timer = 0
    def collide_with_bright_blue_fish(self):
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
        self.restart_timer = 0
    def collide_with_player(self):
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                             random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
        self.restart_timer = 0
    def remove_sprite(self):
        self.kill()