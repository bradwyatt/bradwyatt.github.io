import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class GreenFish(pygame.sprite.Sprite):
    EDGE_PADDING = 100
    WALL_PADDING = 32
    BOTTOM_WALL_Y = SCREEN_HEIGHT - 64
    RIGHT_WALL_X = SCREEN_WIDTH - 32
    MOVE_SPEED = 4
    INCREMENTAL_SCORE = 10
    BIG_FISH_SCORE_THRESHOLD = 40
    CHANGE_DIR_RANGE = (300, 400)
    TURN_TIME_MS = 50  # Duration in milliseconds for the turning animation
    PLAYER_SCORE_VALUE = 2


    def __init__(self, allsprites, images):
        super().__init__()
        self.images = images
        self.image = self.images["spr_green_fish_right"]
        self.original_image = self.image  # Set the initial image as the original
        self.rect = self.image.get_rect()
        
        self.direction = (random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]), 
                          random.choice([-self.MOVE_SPEED, 0, self.MOVE_SPEED]))
        self.change_dir_timer = 0
        self.big_green_fish_score = 0
        self.is_big = False
        self.stop_timer = 0  # Timer for turning animation

        allsprites.add(self)
        
        self.body_mask = None
        self.face_mask = None
        
        self.visible = False  # Initially invisible
        # Initialize the alpha surface here
        self.alpha_surface = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
        self.alpha_surface.blit(self.original_image, (0, 0))

        self.reset_position()
        self.init_fade_in()
        self.reset_position()

        self.game_over = False
    def update(self):
        if self.game_over:
            return
        
        current_time = pygame.time.get_ticks()

        if self.stop_timer > current_time and self.is_big:
            # During the turning time, keep the turning sprite
            self.image = self.images["spr_big_green_fish_turning"]
        else:
            # Regular image update
            self.update_image()

        self.rect.move_ip(*self.direction)
        self.change_dir_timer += 1
        if self.change_dir_timer > random.randrange(*self.CHANGE_DIR_RANGE):
            self.change_direction()
            self.change_dir_timer = 0
            
        # Fade in logic
        if self.fading_in:
            self.visible = True  # Make sprite visible when fade-in starts
            if self.alpha < self.max_alpha:
                self.alpha += self.fade_rate
                self.alpha_surface.set_alpha(self.alpha)
            else:
                self.fading_in = False

        if self.visible:
            self.image = self.alpha_surface
            
    def init_fade_in(self):
        self.alpha = 0
        self.fading_in = True
        self.max_alpha = 255
        self.fade_rate = 2
        self.alpha_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.alpha_surface.blit(self.image, (0, 0))
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)  # Delay in milliseconds


    def update_image(self):
        if self.is_big:
            if self.direction[0] < 0:  # Moving left
                self.image = self.images["spr_big_green_fish_left"]
                self.body_mask = pygame.mask.from_surface(self.images["spr_big_green_fish_left"])
                self.face_mask = pygame.mask.from_surface(self.images["spr_big_green_fish_left_face"])
            else:  # Moving right
                self.image = self.images["spr_big_green_fish_right"]
                self.body_mask = pygame.mask.from_surface(self.images["spr_big_green_fish_right"])
                self.face_mask = pygame.mask.from_surface(self.images["spr_big_green_fish_right_face"])
        else:
            if self.direction[0] < 0:  # Moving left
                self.image = self.images["spr_green_fish_left"]
                self.body_mask = pygame.mask.from_surface(self.images["spr_green_fish_left"])
            else:  # Moving right
                self.image = self.images["spr_green_fish_right"]
                self.body_mask = pygame.mask.from_surface(self.images["spr_green_fish_right"])
                
        self.alpha_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.alpha_surface.blit(self.image, (0, 0))
        self.alpha_surface.set_alpha(self.alpha)


    def change_direction(self):
        new_directions = [(-self.direction[0], self.direction[1]),
                          (self.direction[0], -self.direction[1]),
                          (-self.direction[0], -self.direction[1])]
        self.direction = random.choice(new_directions)

        if self.is_big:
            self.stop_timer = pygame.time.get_ticks() + self.TURN_TIME_MS


    def collision_with_wall(self, rect):
        if self.rect.colliderect(rect):
            self.change_direction()
            self.move_away_from_wall(rect)

    def move_away_from_wall(self, rect):
        if self.rect.left < self.WALL_PADDING:  # Left wall
            self.rect.left = self.WALL_PADDING
        elif self.rect.right > self.RIGHT_WALL_X:  # Right wall
            self.rect.right = self.RIGHT_WALL_X
        if self.rect.top < self.WALL_PADDING:  # Top wall
            self.rect.top = self.WALL_PADDING
        elif self.rect.bottom > self.BOTTOM_WALL_Y:  # Bottom wall
            self.rect.bottom = self.BOTTOM_WALL_Y

    def collision_with_red_fish(self):
        self.big_green_fish_score += self.INCREMENTAL_SCORE
        if self.big_green_fish_score >= self.BIG_FISH_SCORE_THRESHOLD and not self.is_big:
            self.is_big = True
            # Update image based on current direction
            self.update_image()
            
    def reset_position(self):
        # Set the sprite to be fully transparent (invisible)
        self.alpha = 0
        self.alpha_surface.set_alpha(self.alpha)
        self.visible = False

        # Reposition the sprite
        self.rect.topleft = (random.randrange(self.EDGE_PADDING, SCREEN_WIDTH - self.EDGE_PADDING),
                             random.randrange(self.EDGE_PADDING, SCREEN_HEIGHT - self.EDGE_PADDING))

        # Initialize the fade-in process
        self.fading_in = True
        
    def handle_user_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer
            self.fading_in = True  # Start the fade-in process


    def collide_with_player(self):
        # When eaten by the player, the fish should become small again
        self.is_big = False
        self.big_green_fish_score = 0  # Reset the score that tracks progress to becoming big

        # Update the image to the small fish image
        self.update_to_small_fish_image()

        # Reset the fish's position and reinitialize the fade-in effect
        self.reset_position()
        
    def update_to_small_fish_image(self):
        # Set the image to the small green fish and update the alpha surface
        self.original_image = self.images["spr_green_fish_right"]  # Assuming this is the default small fish image
        self.image = self.original_image

        # Update the alpha surface with the new small fish image
        self.alpha_surface = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
        self.alpha_surface.blit(self.original_image, (0, 0))
        self.alpha_surface.set_alpha(self.alpha)
        
    def get_score_value(self):
        return self.PLAYER_SCORE_VALUE

    def remove_sprite(self):
        self.kill()
