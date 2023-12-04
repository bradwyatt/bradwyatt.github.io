import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class Player(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
    
        # Store original images for each direction
        self.original_images = {
            "left": self.images["player_left"],
            "right": self.images["player_right"],
            "up": self.images["player_up"],
            "down": self.images["player_down"],
            "up_left": self.images["player_up_left"],
            "up_right": self.images["player_up_right"],
            "down_left": self.images["player_down_left"],
            "down_right": self.images["player_down_right"],
        }
    
        self.current_direction = "left"  # Default direction
        self.original_image = self.original_images[self.current_direction]
        self.original_width, self.original_height = self.original_image.get_size()
    
        # Initialize size_score and other properties
        self.size_score = 0
        self.speed_power = 0
        self.speed_x, self.speed_y = 6, 6
        self.powerup_time_left, self.speed_time_left = 500, 500
        self.star_power, self.player_animate_timer = 0, 0
        self.pos = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100]
    
        # Initialize self.rect and self.image
        self.image = self.original_image  # Set initial image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
        # Resize the player image based on the initial image
        self.resize_player_image(self.image)
    
        # Add the player to the allsprites group
        allsprites.add(self)
    
        # Set initial position
        self.rect.topleft = (self.pos[0], self.pos[1])
    
        self.last_pressed = 0

        
    def update(self):
        # Update the position of the player
        self.rect = self.image.get_rect()
        newpos = (self.pos[0], self.pos[1])
        self.rect.topleft = newpos
    
        # Handle star power animation for invincibility
        if self.star_power == 1:
            self.player_animate_timer += 1
    
            # Determine the image to use based on the animate timer
            if self.player_animate_timer % 10 < 5:  # Adjust for animation speed
                # Use gold image
                animated_image_key = "player_" + self.current_direction + "_gold"
            else:
                # Use normal image
                animated_image_key = "player_" + self.current_direction
    
            # Reset the animation timer if it reaches the end of the cycle
            if self.player_animate_timer >= 20:  # Adjust for animation cycle length
                self.player_animate_timer = 0
    
            # Set the image for animation
            self.animated_image = self.images[animated_image_key]
        else:
            # If not in star power, use the normal image
            self.animated_image = self.images["player_" + self.current_direction]
        
        # Resize the player image based on the animated image
        self.resize_player_image(self.animated_image)
    
        # Decrement powerup timer and reset if over for both star_power 1 and 2
        if self.star_power > 0:
            self.powerup_time_left -= 1
            if self.powerup_time_left < 0:  # Powerup is over
                self.star_power = 0
                self.powerup_time_left = 500  # Reset timer for the next powerup
    
        # Handle speed powerups/defects
        if self.speed_power > 0:
            self.speed_time_left -= 1
            if self.speed_time_left < 0:  # Speed change is over
                self.speed_power = 0
                self.speed_x, self.speed_y = 6, 6  # Reset to default speed
                self.speed_time_left = 500  # Reset timer for the next speed change

    


    def resize_player_image(self, base_image):
        # Scale the base image
        new_width = base_image.get_width() + self.size_score * 2
        new_height = base_image.get_height() + self.size_score * 2
        self.image = pygame.transform.smoothscale(base_image, (new_width, new_height))
    
        # Update the rect
        self.rect = self.image.get_rect(center=self.rect.center)

    def stop_movement(self):
        if self.speed_power == 1:  # Seahorse speed powerup
            self.speed_x, self.speed_y = 9, 9
        elif self.speed_power == 2:  # Jellyfish speed defect
            self.speed_x, self.speed_y = 2, 2
        else:
            self.speed_x, self.speed_y = 6, 6  # Default speed
    def move_up(self):
        self.current_direction = "up"
        if self.pos[1] > 50: # Boundary, 32 is block, added a few extra pixels to make it look nicer
            self.pos[1] -= self.speed_y
    def move_down(self):
        self.current_direction = "down"
        if self.pos[1] < SCREEN_HEIGHT-75:
            self.pos[1] += self.speed_y
    def move_left(self):
        self.current_direction = "left"
        if self.pos[0] > 32:
            self.pos[0] -= self.speed_x
    def move_right(self):
        self.current_direction = "right"
        if self.pos[0] < SCREEN_WIDTH-75:
            self.pos[0] += self.speed_x
    def move_up_left(self):
        self.current_direction = "up_left"
                
        # Update position for diagonal movement
        if self.pos[1] > 50 and self.pos[0] > 32:
            self.pos[0] -= self.speed_x
            self.pos[1] -= self.speed_y
    def move_up_right(self):
        self.current_direction = "up_right"
                
        # Update position for diagonal movement
        if self.pos[1] > 50 and self.pos[0] < SCREEN_WIDTH-75:
            self.pos[0] += self.speed_x
            self.pos[1] -= self.speed_y
    def move_down_left(self):
        self.current_direction = "down_left"
        
        # Update position for diagonal movement
        if self.pos[1] < SCREEN_HEIGHT-75 and self.pos[0] > 32:
            self.pos[0] -= self.speed_x
            self.pos[1] += self.speed_y
    def move_down_right(self):
        self.current_direction = "down_right"
                
        # Update position for diagonal movement
        if self.pos[1] < SCREEN_HEIGHT-75 and self.pos[0] < SCREEN_WIDTH-75:
            self.pos[0] += self.speed_x
            self.pos[1] += self.speed_y
    def collide_with_red_fish(self, score, score_blit):
        score_blit = 1
        score += 1
        self.size_score += 1
        return score, score_blit
    def collide_with_green_fish(self, score, score_blit):
        score_blit = 2
        score += 2
        self.size_score += 2
        return score, score_blit
    def collide_with_silver_fish(self, score, score_blit):
        score_blit = 3
        score += 3
        self.size_score += 3
        return score, score_blit
    def collide_with_shark(self, score, score_blit):
        if self.star_power == 2: # Mini-sharks
            score_blit = 1
            score += 1
            self.size_score += 1
            return score, score_blit
        else:
            return score, score_blit
    def collide_with_seahorse(self):
        self.speed_power = 1
        self.speed_x, self.speed_y = 9, 9
        self.speed_time_left = 500
    def collide_with_jellyfish(self):
        self.speed_power = 2
        self.size_score = 0
        self.speed_x, self.speed_y = 2, 2
        self.speed_time_left = 500
    def collide_with_snake(self):
        self.size_score = 0
    def collide_with_star(self):
        self.star_power = random.choice([0, 1])+1
    def get_powerup_timer_text(self, font):
        if self.star_power != 0:
            return font.render("Powerup Timer: " + str((self.powerup_time_left//100)+1), 1, (255, 255, 255))
        return font.render("", 1, (0, 0, 0))
    def get_speed_timer_text(self, font):
        if self.speed_power == 1:
            return font.render("Speed Timer: " + str((self.speed_time_left//100)+1), 1, (255, 255, 255))
        elif self.speed_power == 2:
            return font.render("Sting Timer: " + str((self.speed_time_left//100)+1), 1, (255, 255, 255))
        else:
            return font.render("", 1, (0, 0, 0))
    def remove_sprite(self):
        self.kill()