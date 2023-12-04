import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants


class RedFish(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Weakest prey in the game
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["spr_red_fish"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.direction = (random.choice([-2, 2]), random.choice([-2, 0, 2]))
        self.change_dir_timer = 0
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def update(self):
        newpos = (self.rect.topleft[0] + self.direction[0],
                  self.rect.topleft[1] + self.direction[1])
        self.rect.topleft = newpos
        self.change_dir_timer += 1
        if self.direction[0] == -2:
            self.image = pygame.transform.flip(self.images["spr_red_fish"], 1, 0)
        elif self.direction[0] == 2:
            self.image = self.images["spr_red_fish"]
        if self.change_dir_timer > random.randrange(100, 600):
            self.direction = random.choice([(self.direction[0]*-1, self.direction[1]),
                                            (self.direction[0], self.direction[1]*-1),
                                            (self.direction[0]*-1, self.direction[1]*-1)])
            self.change_dir_timer = 0
    def collision_with_wall(self, rect):
        if self.rect.colliderect(rect):
            self.change_dir_timer = 0
            if self.rect.left < 32: # Left walls
                self.direction = (2, random.choice([-2, 0, 2]))
            elif self.rect.top > SCREEN_HEIGHT-64: # Bottom walls
                self.direction = (random.choice([-2, 0, 2]), -2)
            elif self.rect.right > SCREEN_WIDTH-32: # Right walls
                self.direction = (-2, random.choice([-2, 0, 2]))
            elif self.rect.top < 32: # Top walls
                self.direction = (random.choice([-2, 0, 2]), 2)
    def collide_with_player(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def collide_with_bright_blue_fish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def collide_with_green_fish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def remove_sprite(self):
        self.kill()