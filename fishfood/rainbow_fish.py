import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class RainbowFish(pygame.sprite.Sprite):
    MAX_SIZE = [85, 65]  # Maximum size for the RainbowFish
    TURN_TIME_MS = 50
    NUM_OF_TICKS_FOR_ENTRANCE = 1200
    Y_POSITION_SPAWN = -400
    Y_POSITION_TO_START_PLAYING = 125
    NUM_OF_TICKS_FOR_EXIT = 1400
    INITIAL_SIZE_SCORE = 10
    INCREMENTAL_SIZE_SCORE = 10
    MAX_SIZE_SCORE = 50
    MOVE_CHASE_SPEED = 1
    MOVE_AVOID_SPEED = 2
    ASCEND_SPEED = 4
    DESCEND_SPEED = 2
    PLAYER_SCORE_VALUE = 2
    def __init__(self, allsprites, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_rainbow_fish_left"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.is_exiting = False
        self.rainbow_timer = 0
        self.size = [55, 35]
        self.size_score = self.INITIAL_SIZE_SCORE
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), self.Y_POSITION_SPAWN)
        self.rect.topleft = self.pos
        self.is_active = False
        self.initial_descent_complete = False
        
        self.current_direction = "left"  # Default direction
        self.is_turning = False
        self.turning_timer = 0
        self.player_position = (0, 0)  # Initialize player position
        
        # Initialize face and body masks
        self.face_masks = {
            "left": pygame.mask.from_surface(images["spr_rainbow_fish_left_face"]),
            "right": pygame.mask.from_surface(images["spr_rainbow_fish_right_face"])
        }
        self.body_masks = {
            "left": pygame.mask.from_surface(images["spr_rainbow_fish_left"]),
            "right": pygame.mask.from_surface(images["spr_rainbow_fish_right"])
        }
        
        self.face_mask = self.face_masks[self.current_direction]
        self.body_mask = self.body_masks[self.current_direction]
        
        self.game_over = False
        
    def update_player_position(self, player_pos):
        """Update the player's position for the Rainbow Fish."""
        self.player_position = player_pos

    def update(self):
        if self.game_over:
            return
        self.rainbow_timer += 1
        # Scale the image
        self.image = pygame.transform.smoothscale(self.image, (self.size[0], self.size[1]))
        self.update_masks()

        # Handle the descent
        if self.is_active and not self.initial_descent_complete:
            self.descend_to_start_position()

        # Handle the direction change and turning animation
        if self.is_active and self.initial_descent_complete and not self.is_exiting:
            player_on_left = self.player_position[0] < self.rect.centerx
            player_on_right = self.player_position[0] > self.rect.centerx

            if player_on_left and self.current_direction != "left":
                self.animate_turning("left")
            elif player_on_right and self.current_direction != "right":
                self.animate_turning("right")

        # Handle the exiting behavior
        if self.is_exiting:
            self.ascend_and_deactivate()

        self.rect.topleft = self.pos
        
    def animate_turning(self, new_direction):
        if not self.is_turning:
            self.image = self.images["spr_rainbow_fish_turning"]
            self.is_turning = True
            self.turning_timer = pygame.time.get_ticks() + RainbowFish.TURN_TIME_MS
        elif pygame.time.get_ticks() > self.turning_timer:
            # After turning animation, change to the new direction
            self.current_direction = new_direction
            self.is_turning = False
            self.update_image_direction()
            
    def update_image_direction(self):
        self.image = self.images[f"spr_rainbow_fish_{self.current_direction}"]
        self.update_masks()

    def update_masks(self):
        """
        Update the body and face masks based on the current direction and size.
        """
        # Update body mask
        body_image = self.images[f"spr_rainbow_fish_{self.current_direction}"]
        scaled_body_image = pygame.transform.smoothscale(body_image, (self.size[0], self.size[1]))
        self.body_mask = pygame.mask.from_surface(scaled_body_image)

        # Update face mask
        face_image = self.images[f"spr_rainbow_fish_{self.current_direction}_face"]
        scaled_face_image = pygame.transform.smoothscale(face_image, (self.size[0], self.size[1]))
        self.face_mask = pygame.mask.from_surface(scaled_face_image)


    def decide_chase_or_avoid(self, player_size_score, is_player_invincibile, player_pos):
        """
        Determine whether to chase or avoid the player based on the player's state
        and position.
        """
        # Only activate chasing or avoiding behavior if the fish is active and not exiting
        if self.is_active and not self.is_exiting:
            if self.size_score <= player_size_score or is_player_invincibile:
                self.avoid_player(player_pos)
            else:
                self.chase_player(player_pos)

    def manage_spawn_and_exit(self):
        if self.rainbow_timer >= RainbowFish.NUM_OF_TICKS_FOR_EXIT and not self.is_exiting:
            self.is_exiting = True

    def ascend_and_deactivate(self):
        if self.pos[1] > -self.rect.height:
            self.pos = (self.pos[0], self.pos[1] - self.ASCEND_SPEED)
        else:
            self.reinitialize_for_next_spawn()
    
    def descend_to_start_position(self):
        if self.pos[1] < self.Y_POSITION_TO_START_PLAYING:
            # Ensure the image is set to the correct directional image at the start of the descent
            # if not self.is_turning:
            #     self.image = self.images[f"spr_rainbow_fish_{self.current_direction}"]
            #     self.update_masks()
    
            self.pos = (self.pos[0], self.pos[1] + self.DESCEND_SPEED)
        else:
            self.initial_descent_complete = True

    def reinitialize_for_next_spawn(self):
        """
        Restart all variables for the next spawn cycle.
        """
        self.is_active = False
        self.is_exiting = False
        self.initial_descent_complete = False
        self.rainbow_timer = 0
        self.is_active = 0
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), self.Y_POSITION_SPAWN)
        if self.size_score <= self.MAX_SIZE_SCORE:
            self.size[0] += 10
            self.size[1] += 10
            self.size_score += self.INCREMENTAL_SIZE_SCORE
    
    def avoid_player(self, player_pos):
        #Avoid Player
        if self.initial_descent_complete:
            if self.pos[0] > player_pos[0]:
                self.pos = (self.pos[0]+self.MOVE_AVOID_SPEED, self.pos[1])
            elif self.pos[0] < player_pos[0]:
                self.pos = (self.pos[0]-self.MOVE_AVOID_SPEED, self.pos[1])
            if self.pos[1] < player_pos[1]:
                self.pos = (self.pos[0], self.pos[1]-self.MOVE_AVOID_SPEED)
            elif self.pos[1] > player_pos[1]:
                self.pos = (self.pos[0], self.pos[1]+self.MOVE_AVOID_SPEED)
            # Rainbow fish can't go past walls, must go up if stuck
            if(self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH-32):
                self.is_exiting = True
            elif(self.pos[1] < 32 or self.pos[1] > SCREEN_HEIGHT-32):
                self.is_exiting = True
                
    def chase_player(self, player_pos):
        if self.pos[0] > player_pos[0]:
            self.pos = (self.pos[0]-self.MOVE_CHASE_SPEED, self.pos[1])
        elif self.pos[0] < player_pos[0]:
            self.pos = (self.pos[0]+self.MOVE_CHASE_SPEED, self.pos[1])
        if self.pos[1] < player_pos[1]:
            self.pos = (self.pos[0], self.pos[1]+self.MOVE_CHASE_SPEED)
        elif self.pos[1] > player_pos[1]:
            self.pos = (self.pos[0], self.pos[1]-self.MOVE_CHASE_SPEED)
            
    def get_score_value(self):
        return self.PLAYER_SCORE_VALUE

    def collide_with_player(self):
        self.reinitialize_for_next_spawn()
    def collide_with_bright_blue_fish(self):
        self.reinitialize_for_next_spawn()
    def remove_sprite(self):
        self.kill()