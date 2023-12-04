import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class GreenFish(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Prey until it eats several red fish, and becomes a big green fish that
        can eat the player (unless the player is bigger)
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_green_fish"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.direction = (random.choice([-4, 4]), random.choice([-4, 0, 4]))
        self.change_dir_timer = 0
        self.big_green_fish_score = 0
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def update(self):
        newpos = (self.rect.topleft[0] + self.direction[0],
                  self.rect.topleft[1] + self.direction[1])
        self.rect.topleft = newpos
        self.change_dir_timer += 1
        if self.big_green_fish_score < 70:
            if self.direction[0] == -4:
                self.image = self.images["spr_green_fish_left"]
            elif self.direction[0] == 4:
                self.image = self.images["spr_green_fish"]
        if self.change_dir_timer > random.randrange(50, 300):
            self.direction = random.choice([(self.direction[0]*-1, self.direction[1]),
                                            (self.direction[0], self.direction[1]*-1),
                                            (self.direction[0]*-1, self.direction[1]*-1)])
            self.change_dir_timer = 0
    def collision_with_wall(self, rect):
        self.change_dir_timer = 0
        if self.rect.colliderect(rect):
            if self.rect.left < 32: # Left walls
                self.direction = (4, random.choice([-4, 4]))
            elif self.rect.top > SCREEN_HEIGHT-64: # Bottom walls
                self.direction = (random.choice([-4, 4]), -4)
            elif self.rect.right > SCREEN_WIDTH-32: # Right walls
                self.direction = (-4, random.choice([-4, 4]))
            elif self.rect.top < 32: # Top walls
                self.direction = (random.choice([-4, 4]), 4)
    def collision_with_redfish(self):
        self.big_green_fish_score += 10
        if self.big_green_fish_score == 70:
            self.image = pygame.transform.smoothscale(self.images["spr_big_green_fish"], (103, 58))
    def small_collision_with_player(self):
        self.image = self.images["spr_green_fish"]
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def remove_sprite(self):
        self.kill()