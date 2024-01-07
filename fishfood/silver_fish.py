import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class SilverFish(pygame.sprite.Sprite):
    OFFSCREEN_LEFT = -50
    OFFSCREEN_RIGHT = SCREEN_WIDTH
    MOVE_SPEED = 3
    SPAWN_Y_RANGE = (50, 150)
    RESET_TIMER_THRESHOLD = 100
    RESET_POSITION_LEFT = -40
    RESET_POSITION_RIGHT = SCREEN_WIDTH - 10
    PLAYER_SCORE_VALUE = 3

    def __init__(self, allsprites, images):
        super().__init__()
        self.images = images
        self.image = images["spr_silver_fish"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.OFFSCREEN_LEFT, random.randrange(*self.SPAWN_Y_RANGE))  # Initially offscreen
        self.restart_timer = 0
        self.direction = random.choice([0, 1])  # 0: left, 1: right
        allsprites.add(self)
        self.in_game_world = False  # Track if fish is in game world

    def update(self):
        if not self.in_game_world:
            self.restart_timer += 1
            if self.restart_timer > self.RESET_TIMER_THRESHOLD:
                self.reset_position()
                self.in_game_world = True
        else:
            self.move_fish()
            self.check_bounds_and_reset()

    def move_fish(self):
        if self.direction == 1:  # Moving right
            self.rect.move_ip(self.MOVE_SPEED, 0)
            self.image = self.images["spr_silver_fish"]
        elif self.direction == 0:  # Moving left
            self.rect.move_ip(-self.MOVE_SPEED, 0)
            self.image = pygame.transform.flip(self.images["spr_silver_fish"], True, False)

    def check_bounds_and_reset(self):
        if (self.rect.left > SCREEN_WIDTH and self.direction == 1) or \
           (self.rect.right < 0 and self.direction == 0):
            self.in_game_world = False
            self.restart_timer = 0


    def reset_position(self):
        x_position = random.choice([self.OFFSCREEN_LEFT, self.OFFSCREEN_RIGHT])
        y_position = random.randrange(*self.SPAWN_Y_RANGE)
        self.rect.topleft = (x_position, y_position)
        self.direction = random.choice([0, 1])

    def collide_with_player(self):
        self.in_game_world = False
        self.restart_timer = 0
        self.reset_position()
        
    def get_score_value(self):
        return self.PLAYER_SCORE_VALUE

    def collide_with_bright_blue_fish(self):
        self.in_game_world = False
        self.restart_timer = 0
        self.reset_position()

    def remove_sprite(self):
        self.kill()
