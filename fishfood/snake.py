import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class Snake(pygame.sprite.Sprite):
    OFF_SCREEN_LEFT = -80
    OFF_SCREEN_RIGHT = SCREEN_WIDTH
    RESPAWN_TIMER = 800
    ANIMATION_CYCLE_LENGTH = 20
    SPEED = 2
    DIRECTION_LEFT = -1
    DIRECTION_RIGHT = 1
    BOTTOM_POSITION_Y_RANGE = (SCREEN_HEIGHT - 110, SCREEN_HEIGHT - 50)

    def __init__(self, allsprites, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_snake_1"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.timer = -Snake.RESPAWN_TIMER
        self.snake_animator = 0
        self.reset_position()

    def update(self):
        if not self.is_in_game_world():
            self.timer += 1

        self.snake_animator = (self.snake_animator + 1) % Snake.ANIMATION_CYCLE_LENGTH
        self.update_animation()

        if self.timer >= 0 and self.timer < Snake.RESPAWN_TIMER:
            self.move()

        if (self.direction == Snake.DIRECTION_LEFT and self.rect.right < Snake.OFF_SCREEN_LEFT) or \
           (self.direction == Snake.DIRECTION_RIGHT and self.rect.left > Snake.OFF_SCREEN_RIGHT):
            self.reset_position()

    def move(self):
        self.rect.x += Snake.SPEED * self.direction

    def reset_position(self):
        self.direction = random.choice([Snake.DIRECTION_LEFT, Snake.DIRECTION_RIGHT])
        if self.direction == Snake.DIRECTION_LEFT:
            self.rect.x = Snake.OFF_SCREEN_RIGHT
        else:
            self.rect.x = Snake.OFF_SCREEN_LEFT - self.rect.width
        self.rect.y = random.randint(*Snake.BOTTOM_POSITION_Y_RANGE)
        self.timer = -Snake.RESPAWN_TIMER

    def update_animation(self):
        frame = (self.snake_animator // 5) % 4 + 1
        if self.direction == Snake.DIRECTION_LEFT:
            self.image = self.images[f"spr_snake_{frame}"]
        else:
            self.image = pygame.transform.flip(self.images[f"spr_snake_{frame}"], True, False)

    def is_in_game_world(self):
        return self.rect.right > Snake.OFF_SCREEN_LEFT and self.rect.left < Snake.OFF_SCREEN_RIGHT

    def collide_with_player(self):
        self.reset_position()
        
    def collide_with_bright_blue_fish(self):
        self.reset_position()

    def remove_sprite(self):
        self.kill()
