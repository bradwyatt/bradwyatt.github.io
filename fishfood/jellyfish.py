import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class Jellyfish(pygame.sprite.Sprite):
    EDGE_PADDING = 50
    MAX_DOWN_Y = SCREEN_HEIGHT - 80
    OFFSCREEN_Y = -50
    MIN_SPAWN_TIME = 200
    MAX_SPAWN_TIME = 300
    MOVE_VERTICAL = 3
    JELLYFISHES_SCORE_TO_SPAWN = [0, 30, 60]

    def __init__(self, all_sprites, images):
        super().__init__()
        self.images = images
        self.image = images["spr_jellyfish_1"]
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.return_back = False
        self.jellyfish_timer = 0
        self.jellyfish_animate_timer = 0
        self.jellyfish_random_spawn = random.randrange(Jellyfish.MIN_SPAWN_TIME,
                                                       Jellyfish.MAX_SPAWN_TIME)
        self.activate = False
        self.rect.topleft = self.random_spawn_position()

    def update(self):
        if self.activate:
            if self.jellyfish_timer > self.jellyfish_random_spawn:
                self.update_animation()
                self.move_jellyfish()
            else:
                self.update_timer()

    def update_animation(self):
        self.jellyfish_animate_timer = (self.jellyfish_animate_timer + 1) % 28
        animation_stage = self.jellyfish_animate_timer // 2
        if animation_stage < 7:
            self.image = self.images[f"spr_jellyfish_{animation_stage + 1}"]
        else:
            self.image = self.images[f"spr_jellyfish_{14 - animation_stage}"]


    def move_jellyfish(self):
        if self.rect.top <= self.OFFSCREEN_Y and self.return_back:
            self.return_back = False
            self.reset_jellyfish()  # Reset for the next cycle
        elif self.rect.top >= self.MAX_DOWN_Y:
            self.return_back = True
    
        if not self.return_back:
            self.rect.move_ip(0, self.MOVE_VERTICAL)
        else:
            self.rect.move_ip(0, -self.MOVE_VERTICAL)
            
    def update_timer(self):
        self.jellyfish_timer += 1

    def reset_jellyfish(self):
        self.jellyfish_random_spawn = random.randrange(Jellyfish.MIN_SPAWN_TIME,
                                                       Jellyfish.MAX_SPAWN_TIME)
        self.rect.topleft = self.random_spawn_position()
        self.jellyfish_timer = 0  # Reset timer for the next cycle

    def random_spawn_position(self):
        x_pos = random.randrange(self.EDGE_PADDING, SCREEN_WIDTH - self.EDGE_PADDING)
        return x_pos, self.OFFSCREEN_Y

    def collide_with_player(self):
        self.reset_jellyfish()

    def collide_with_bright_blue_fish(self):
        self.reset_jellyfish()

    def remove_sprite(self):
        self.kill()
