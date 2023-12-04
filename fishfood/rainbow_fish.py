import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class RainbowFish(pygame.sprite.Sprite):
    def __init__(self, allsprites, images):
        """
        Starts from above, then begins to chase player if player is smaller
        Will run away if player is bigger
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_rainbow_fish"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.score_exit = 0
        self.rainbow_timer = 0
        self.size = [55, 35]
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), -400)
        self.rect.topleft = self.pos
        self.arrow_warning = 0
        self.activate = 0
        self.chase = 0
    def update(self):
        self.rect.topleft = (self.pos[0], self.pos[1])
        self.rainbow_timer += 1
        if self.activate == 1:
            if self.rainbow_timer >= 2000 or self.score_exit == 1: #return; go off screen
                self.chase = 0
                # RETURN TO TOP OF SCREEN
                if self.pos[1] > -100:
                    self.score_exit = 1
                    self.pos = (self.pos[0], self.pos[1]-3) # slightly faster running away
                else:
                    # RESET EVERYTHING
                    self.activate = 0
                    self.pos = (random.randrange(100, SCREEN_WIDTH-100), -100)
                    self.rainbow_timer, self.score_exit = 0, 0
                    if self.size[0]-20 <= 55: #one check on [0], so 85 width is max size
                        self.size[0] += 10
                        self.size[1] += 10
                    self.image = self.images["spr_rainbow_fish"]
            # Move down at start
            elif self.rainbow_timer >= 300 and self.pos[1] < 200 and self.chase == 0 and self.score_exit == 0: 
                self.arrow_warning = 1
                if self.size[0]-30 == 55: #so it doesn't get more blurry each time at max size
                    self.pos = (self.pos[0], self.pos[1]+2)
                else:
                    self.image = pygame.transform.smoothscale(self.image, (self.size[0], self.size[1]))
                    self.pos = (self.pos[0], self.pos[1]+2)
            if self.pos[1] >= 100:
                self.arrow_warning = 0
            if self.pos[1] >= 200 and self.score_exit == 0:
                self.chase = 1
                
    def chase_player(self, player_size_score, player_star_power, player_pos):
        if self.score_exit == 0 and self.chase == 1:
            if(self.size[0]-45 <= player_size_score or player_star_power == 1):
                #Avoid Player
                if self.pos[0] > player_pos[0]:
                    self.pos = (self.pos[0]+2, self.pos[1])
                elif self.pos[0] < player_pos[0]:
                    self.pos = (self.pos[0]-2, self.pos[1])
                if self.pos[1] < player_pos[1]:
                    self.pos = (self.pos[0], self.pos[1]-2)
                elif self.pos[1] > player_pos[1]:
                    self.pos = (self.pos[0], self.pos[1]+2)
                # Rainbow fish can't go past walls, must go up if stuck
                if(self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH-32):
                    self.score_exit = 1
                    self.chase = 0
                elif(self.pos[1] < 32 or self.pos[1] > SCREEN_HEIGHT-32):
                    self.score_exit = 1
                    self.chase = 0
            else:
                #Chase Player
                if self.pos[0] > player_pos[0]:
                    self.pos = (self.pos[0]-1, self.pos[1])
                elif self.pos[0] < player_pos[0]:
                    self.pos = (self.pos[0]+1, self.pos[1])
                if self.pos[1] < player_pos[1]:
                    self.pos = (self.pos[0], self.pos[1]+1)
                elif self.pos[1] > player_pos[1]:
                    self.pos = (self.pos[0], self.pos[1]-1)
    def collide_with_player(self):
        self.rainbow_timer = 0
        self.activate = 0
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), -100)
        if self.size[0]-20 <= 55: #increases till max size
            self.size[0] += 10
            self.size[1] += 10
    def collide_with_bright_blue_fish(self):
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), -100)
        self.rainbow_timer = 0
    def remove_sprite(self):
        self.kill()