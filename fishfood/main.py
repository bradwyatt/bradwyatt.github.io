import asyncio
import pygame
import os
import random
from pygame.constants import RLEACCEL

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
IMAGES = {}
SOUNDS = {}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("More Complex Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def load_image(file, name, transparent, alpha):
    new_image = pygame.image.load(file)
    if alpha:
        new_image = new_image.convert_alpha()
    else:
        new_image = new_image.convert()
    if transparent:
        colorkey = new_image.get_at((0, 0))
        new_image.set_colorkey(colorkey, RLEACCEL)
    IMAGES[name] = new_image

def load_sound(file, name):
    sound = pygame.mixer.Sound(file)
    SOUNDS[name] = sound

class Wall(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_wall"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
    def remove_sprite(self):
        self.kill()

class Seaweed(pygame.sprite.Sprite):
    def __init__(self, allsprites, x_pos, y_pos):
        """
        Animated seaweed
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_seaweed"]
        self.rect = self.image.get_rect()
        self.rect.topleft = x_pos, y_pos
        allsprites.add(self)
        self.seaweed_animate_timer = random.randint(0, 30)
    def update(self):
        self.seaweed_animate_timer += 1
        seaweed_images = [IMAGES["spr_seaweed"], IMAGES["spr_seaweed_left"], IMAGES["spr_seaweed_right"]]
        if self.seaweed_animate_timer > 15 and self.seaweed_animate_timer < 30:
            self.image = seaweed_images[1]
        if self.seaweed_animate_timer >= 30:
            self.image = seaweed_images[2]
        if self.seaweed_animate_timer > 45:
            self.seaweed_animate_timer = 0
            self.image = seaweed_images[0]
    def remove_sprite(self):
        self.kill()

class RedFish(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Weakest prey in the game
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_red_fish"]
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
            self.image = pygame.transform.flip(IMAGES["spr_red_fish"], 1, 0)
        elif self.direction[0] == 2:
            self.image = IMAGES["spr_red_fish"]
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
    def collide_with_brightbluefish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def collide_with_greenfish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def remove_sprite(self):
        self.kill()

class GreenFish(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Prey until it eats several red fish, and becomes a big green fish that
        can eat the player (unless the player is bigger)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_green_fish"]
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
                self.image = IMAGES["spr_green_fish_left"]
            elif self.direction[0] == 4:
                self.image = IMAGES["spr_green_fish"]
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
            self.image = pygame.transform.smoothscale(IMAGES["spr_big_green_fish"], (103, 58))
    def small_collision_with_player(self):
        self.image = IMAGES["spr_green_fish"]
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
    def remove_sprite(self):
        self.kill()

class SilverFish(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Whem eaten, higher amount of points, but shows up infrequently
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_silver_fish"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
        self.restarttimer = 0
        self.direction = random.choice([0, 1]) #right or left
        allsprites.add(self)
    def update(self):
        self.restarttimer += 1
        if self.restarttimer > 250:
            if self.rect.topleft[0] == -50:
                self.direction = 1 # right
            elif self.rect.topleft[0] == SCREEN_WIDTH:
                self.direction = 0 # left
            if self.direction == 1: # right movements
                self.rect.topleft = self.rect.topleft[0]+3, self.rect.topleft[1]
                self.image = IMAGES["spr_silver_fish"]
            elif self.direction == 0: # left movements
                self.rect.topleft = self.rect.topleft[0]-3, self.rect.topleft[1]
                self.image = pygame.transform.flip(IMAGES["spr_silver_fish"], 1, 0)
            if(self.rect.topleft[0] < -40 and self.direction == 0): #restarts position
                self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restarttimer = 0
            elif(self.rect.topleft[0] > SCREEN_WIDTH-10 and self.direction == 1): #restarts position
                self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restarttimer = 0
    def collide_with_player(self):
        self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
        self.restarttimer = 0
    def collide_with_brightbluefish(self):
        self.rect.topleft = (random.choice([-50, SCREEN_WIDTH]), random.randrange(50, 150))
        self.restarttimer = 0
    def remove_sprite(self):
        self.kill()

class Shark(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Most frequently-seen predator in the game.
        Starts coming from above and then bounces around the room
        Only time player can avoid:
        When player has a star powerup, shark respawns
        When player has mini shark powerup, they can eat sharks
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_shark"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.direction = (random.choice([-3, 3]), random.choice([-3, 3]))
        self.mini_shark = 0
        self.activate = 0
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -400)
        self.arrow_warning = 0
    def update(self):
        if self.rect.topleft[1] < 0:
            if self.activate == 1:
                self.rect.topleft = (self.rect.topleft[0], self.rect.topleft[1]+3)
                self.arrow_warning = 1
        else:
            self.arrow_warning = 0
            newpos = (self.rect.topleft[0] + self.direction[0],
                      self.rect.topleft[1] + self.direction[1])
            self.rect.topleft = newpos
        if self.mini_shark == 1:
            self.image = pygame.transform.smoothscale(self.image, (60, 30))
        else:
            self.image = IMAGES["spr_shark"]
    def collision_with_wall(self, rect):
        if self.rect.colliderect(rect):
            if self.rect.left < 32: #left walls
                self.direction = (3, random.choice([-3, 3]))
            elif self.rect.top > SCREEN_HEIGHT-64: #bottom walls
                self.direction = (random.choice([-3, 3]), -3)
            elif self.rect.right > SCREEN_WIDTH-32: #right walls
                self.direction = (-3, random.choice([-3, 3]))
            elif self.rect.top < 32: #top walls
                self.direction = (random.choice([-3, 3]), 3)
    def collide_with_brightbluefish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -100)
    def collide_with_player(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -100)
    def remove_sprite(self):
        self.kill()

class BrightBlueFish(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Biggest predator in the game, eats everything that comes in contact
        Player can avoid if they have a star powerup
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_bright_blue_fish"]
        self.direction = random.choice([0, 1]) #move left: 0, move right: 1
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.activate = 0
        self.rect.topleft = (random.choice([-1000, SCREEN_WIDTH+1000]),
                             random.randrange(50, SCREEN_HEIGHT-200))
        self.arrow_warning = 0
    def update(self):
        if self.activate == 1:
            self.arrow_warning = 1
            if self.direction == 1:
                self.image = IMAGES["big_bright_blue_fish"]
            elif self.direction == 0:
                self.image = IMAGES["big_bright_blue_fish_left"]
            if self.direction == 1 and self.activate == 1: #right movements
                self.rect.topleft = self.rect.topleft[0]+4, self.rect.topleft[1]
                if self.rect.right > -200: # Remove arrow
                    self.arrow_warning = 0
                if self.rect.left > SCREEN_WIDTH: # Past right side of screen
                    self.activate = 0
            elif self.direction == 0 and self.activate == 1: #left movements
                self.rect.topleft = self.rect.topleft[0]-4, self.rect.topleft[1]
                if self.rect.left <= SCREEN_WIDTH:
                    self.arrow_warning = 0
                if self.rect.right < -300: # Past left side of screen
                    self.activate = 0

        else:
            self.image = IMAGES["spr_bright_blue_fish"]
    def remove_sprite(self):
        self.kill()

class RainbowFish(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Starts from above, then begins to chase player if player is smaller
        Will run away if player is bigger
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_rainbow_fish"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.score_exit = 0
        self.rainbowtimer = 0
        self.size = [55, 35]
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), -400)
        self.rect.topleft = self.pos
        self.arrow_warning = 0
        self.activate = 0
        self.chase = 0
    def update(self):
        self.rect.topleft = (self.pos[0], self.pos[1])
        self.rainbowtimer += 1
        if self.activate == 1:
            if self.rainbowtimer >= 2000 or self.score_exit == 1: #return; go off screen
                self.chase = 0
                # RETURN TO TOP OF SCREEN
                if self.pos[1] > -100:
                    self.score_exit = 1
                    self.pos = (self.pos[0], self.pos[1]-3) # slightly faster running away
                else:
                    # RESET EVERYTHING
                    self.activate = 0
                    self.pos = (random.randrange(100, SCREEN_WIDTH-100), -100)
                    self.rainbowtimer, self.score_exit = 0, 0
                    if self.size[0]-20 <= 55: #one check on [0], so 85 width is max size
                        self.size[0] += 10
                        self.size[1] += 10
                    self.image = IMAGES["spr_rainbow_fish"]
            # Move down at start
            elif self.rainbowtimer >= 300 and self.pos[1] < 200 and self.chase == 0 and self.score_exit == 0: 
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
                
    def chase_player(self, player_sizescore, player_starpower, player_pos):
        if self.score_exit == 0 and self.chase == 1:
            if(self.size[0]-45 <= player_sizescore or player_starpower == 1):
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
        self.rainbowtimer = 0
        self.activate = 0
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), -100)
        if self.size[0]-20 <= 55: #increases till max size
            self.size[0] += 10
            self.size[1] += 10
    def collide_with_brightbluefish(self):
        self.pos = (random.randrange(100, SCREEN_WIDTH-100), -100)
        self.rainbowtimer = 0
    def remove_sprite(self):
        self.kill()

class Snake(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Snake bite causes player to downsize to the original size
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_snake"]
        self.restarttimer = 0
        self.direction = random.choice([0, 1]) #move left: 0, move right: 1
        self.rect = self.image.get_rect()
        self.snakeplayeranimatetimer = 0
        self.randomspawn = random.randrange(200, 400)
        allsprites.add(self)
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
    def update(self):
        self.snakeplayeranimatetimer += 1
        if self.direction == 0: #go left
            if self.snakeplayeranimatetimer > 5:
                self.image = IMAGES["spr_snake_2"]
            if self.snakeplayeranimatetimer > 10:
                self.image = IMAGES["spr_snake_3"]
            if self.snakeplayeranimatetimer > 15:
                self.image = IMAGES["spr_snake_4"]
            if self.snakeplayeranimatetimer > 20:
                self.image = IMAGES["spr_snake"]
                self.snakeplayeranimatetimer = 0
        elif self.direction == 1: #go right
            if self.snakeplayeranimatetimer > 5:
                self.image = pygame.transform.flip(IMAGES["spr_snake_2"], 1, 0)
            if self.snakeplayeranimatetimer > 10:
                self.image = pygame.transform.flip(IMAGES["spr_snake_3"], 1, 0)
            if self.snakeplayeranimatetimer > 15:
                self.image = pygame.transform.flip(IMAGES["spr_snake_4"], 1, 0)
            if self.snakeplayeranimatetimer > 20:
                self.image = pygame.transform.flip(IMAGES["spr_snake"], 1, 0)
                self.snakeplayeranimatetimer = 0
        self.restarttimer += 1
        if self.restarttimer > self.randomspawn:
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
                self.restarttimer = 0
            elif(self.rect.topleft[0] > SCREEN_WIDTH-10 and self.direction == 1): #restarts position
                self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                                     random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restarttimer = 0
    def collide_with_brightbluefish(self):
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
        self.restarttimer = 0
    def collide_with_player(self):
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                             random.randrange(SCREEN_HEIGHT-110, SCREEN_HEIGHT-50))
        self.restarttimer = 0
    def remove_sprite(self):
        self.kill()

class SeaHorse(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Speed powerup for player
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_seahorse"]
        self.restarttimer = 0
        self.direction = random.choice([0, 1]) #move left: 0, move right: 1
        self.randomspawn = random.randrange(200, 500) #timer
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(50, SCREEN_HEIGHT-200))
    def update(self):
        self.restarttimer += 1
        if self.direction == 1:
            self.image = pygame.transform.flip(IMAGES["spr_seahorse"], 1, 0)
        else:
            self.image = IMAGES["spr_seahorse"]
        if self.restarttimer > self.randomspawn:
            if self.rect.topleft[0] == -70:
                self.direction = 1 #right
            elif self.rect.topleft[0] == SCREEN_WIDTH:
                self.direction = 0 #left
            if self.direction == 1: #right movements
                self.rect.topleft = self.rect.topleft[0]+3, self.rect.topleft[1]
            elif self.direction == 0: #left movements
                self.rect.topleft = self.rect.topleft[0]-3, self.rect.topleft[1]
            if(self.rect.topleft[0] < -60 and self.direction == 0): #restarts position
                self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                                     random.randrange(50, SCREEN_HEIGHT-200))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restarttimer = 0
                self.randomspawn = random.randrange(1500, 2000)
            elif(self.rect.topleft[0] > SCREEN_WIDTH-10 and self.direction == 1): #restarts position
                self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]),
                                     random.randrange(50, SCREEN_HEIGHT-200))
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1]
                self.restarttimer = 0
                self.randomspawn = random.randrange(1500, 2000)
    def collide_with_player(self):
        self.rect.topleft = (random.choice([-70, SCREEN_WIDTH]), random.randrange(50, SCREEN_HEIGHT-200))
        self.restarttimer = 0
    def remove_sprite(self):
        self.kill()

class JellyFish(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Slows down player temporarily for 5 seconds
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_jellyfish"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.returnback = 0
        self.jellyfishtimer = 0
        self.jellyfishanimatetimer = 0
        self.jellyfishrandomspawn = random.randrange(700, 900)
        self.newpos = self.rect.topleft[0], self.rect.topleft[1]
        self.jfstring = []
        self.activate = 0
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -50)
    def update(self):
        self.jellyfishanimatetimer += 1
        self.jfstring = [IMAGES["spr_jellyfish"], IMAGES["spr_jellyfish_2"], IMAGES["spr_jellyfish_3"],
                         IMAGES["spr_jellyfish_4"], IMAGES["spr_jellyfish_5"], IMAGES["spr_jellyfish_6"],
                         IMAGES["spr_jellyfish_7"]]
        for i in range(2, 16, 2): #cycle through first 13 sprite animations
            if self.jellyfishanimatetimer >= i:
                self.image = self.jfstring[(i//2)-1]
        for i in range(18, 28, 2): #cycle through 13 sprite animations backwards
            if self.jellyfishanimatetimer > i:
                self.image = self.jfstring[((28-i)//2)+1]
        if self.jellyfishanimatetimer > 28:
            self.jellyfishanimatetimer = 1
        self.jellyfishtimer += 1
        if self.rect.topleft[1] == -50:
            self.returnback = 0
        if self.rect.topleft[1] > SCREEN_HEIGHT-80:
            #collide with BOTTOM wall
            self.returnback = 1
        if self.returnback == 0 and self.jellyfishtimer > self.jellyfishrandomspawn:
            if self.activate:
                self.newpos = (self.rect.topleft[0], self.rect.topleft[1]+3)
                self.rect.topleft = self.newpos
        elif self.returnback == 1:
            self.newpos = (self.rect.topleft[0], self.rect.topleft[1]-3)
            self.rect.topleft = self.newpos
            if self.rect.topleft[1] < -32:
                self.jellyfishtimer = 0
                self.jellyfishrandomspawn = random.randrange(500, 1200)
                self.rect.topleft = random.randrange(100, SCREEN_WIDTH-100), -50
    def collide_with_player(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -50)
        self.jellyfishtimer = 0
    def collide_with_brightbluefish(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), -50)
        self.jellyfishtimer = 0
    def remove_sprite(self):
        self.kill()

class StarPowerup(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Player becomes invincible for period of time
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_star"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.staranimator = 0
        self.spawntimer = 0
        self.pos = (SCREEN_WIDTH, SCREEN_HEIGHT-80) # Out of screen
        self.rect.topleft = self.pos
    def update(self):
        self.spawntimer += 1
        self.staranimator += 1
        self.rect.topleft = (self.pos[0], self.pos[1])
        if self.spawntimer == 2600: # Reset position, timer to 0
            self.pos = (SCREEN_WIDTH, SCREEN_HEIGHT-80)
            self.spawntimer = 0
        elif self.spawntimer > 1500: # Respawn
            self.pos = (self.pos[0]-5, SCREEN_HEIGHT-80)
            if self.staranimator > 0:
                self.image = IMAGES["spr_star"]
            if self.staranimator > 10:
                self.image = IMAGES["spr_star_2"]
            if self.staranimator > 20:
                self.image = IMAGES["spr_star_3"]
            if self.staranimator > 30:
                self.image = IMAGES["spr_star_2"]
            if self.staranimator > 40:
                self.staranimator = 0
    def collide_with_player(self):
        self.pos = (SCREEN_WIDTH, SCREEN_HEIGHT-80)
        self.spawntimer = 0
    def remove_sprite(self):
        self.kill()
        
class Player(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        """
        Main fish that player controls in the game
        Ability to grow to eat smaller fish (prey)
        """
        pygame.sprite.Sprite.__init__(self, allsprites)
        self.image = IMAGES["player_left"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.player_width, self.player_height = (41, 19)
        self.sizescore = 0
        self.speedpower = 0
        self.speed_x, self.speed_y = 6, 6
        self.powerup_time_left, self.speed_time_left = 500, 500
        self.starpower, self.playeranimatetimer = 0, 0
        self.pos = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2+100]
        self.rect.topleft = (self.pos[0], self.pos[1])
        self.last_pressed = 0
    def update(self):
        self.rect = self.image.get_rect()
        newpos = (self.pos[0], self.pos[1])
        self.rect.topleft = newpos
        # GROW
        if self.sizescore < 0:
            self.sizescore = 0
        if self.sizescore > 40:
            self.sizescore = 40
        self.image = pygame.transform.smoothscale(self.image, (self.player_width+self.sizescore, self.player_height+self.sizescore))
        self.rect.inflate_ip(self.sizescore, self.sizescore)
        # STAR POWERUPS
        if self.starpower == 0: #no star power
            self.powerup_time_left = 500 #restart to 5 seconds
        elif self.starpower == 1: #star powerup
            self.playeranimatetimer += 1
            if self.playeranimatetimer > 6:
                self.playeranimatetimer = 0
            self.powerup_time_left -= 1
        elif self.starpower == 2: #mini sharks
            self.powerup_time_left -= 1
        # SPEED POWERUPS/DEFECTS
        if self.speedpower == 0:
            self.speed_x, self.speed_y = 6, 6
            self.speed_time_left = 500
        elif (self.speedpower == 1 or self.speedpower == 2): # Seahorse & jellyfish
            self.speed_time_left -= 1
        # RESET TIMERS
        if self.powerup_time_left < 0: # Powerup is over on the player
            self.starpower = 0
            self.powerup_time_left = 500
        if self.speed_time_left < 0:
            self.speedpower = 0
            self.speed_time_left = 500
    def stop_movement(self):
        self.speed_x, self.speed_y = 0, 0
        self.player_width, self.player_height = (41, 19)
        if self.last_pressed == 0:
            if self.starpower == 1:
                if self.playeranimatetimer > 2:
                    self.image = IMAGES["player_left_gold"]
                if self.playeranimatetimer > 4:
                    self.image = IMAGES["player_left"]
            else:
                self.image = IMAGES["player_left"]
        else:
            if self.starpower == 1:
                if self.playeranimatetimer > 2:
                    self.image = pygame.transform.rotate(IMAGES["player_left_gold"], 180)
                    self.image = pygame.transform.flip(self.image, 0, 1)
                if self.playeranimatetimer > 4:
                    self.image = pygame.transform.rotate(IMAGES["player_left"], 180)
                    self.image = pygame.transform.flip(self.image, 0, 1)
            else:
                self.image = pygame.transform.rotate(IMAGES["player_left"], 180)
                self.image = pygame.transform.flip(self.image, 0, 1)
    def move_up(self):
        self.player_width, self.player_height = (21, 42)
        self.image = pygame.transform.flip(IMAGES["player_down"], 1, 1)
        if self.pos[1] > 50: # Boundary, 32 is block, added a few extra pixels to make it look nicer
            self.pos[1] -= self.speed_y
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = pygame.transform.flip(IMAGES["player_down_gold"], 1, 1)
            if self.playeranimatetimer > 4:
                self.image = pygame.transform.flip(IMAGES["player_down"], 1, 1)
    def move_down(self):
        self.player_width, self.player_height = (21, 42)
        self.image = IMAGES["player_down"]
        if self.pos[1] < SCREEN_HEIGHT-75:
            self.pos[1] += self.speed_y
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = IMAGES["player_down_gold"]
            if self.playeranimatetimer > 4:
                self.image = IMAGES["player_down"]
    def move_left(self):
        self.player_width, self.player_height = (41, 19)
        self.image = IMAGES["player_left"]
        if self.pos[0] > 32:
            self.pos[0] -= self.speed_x
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = IMAGES["player_left_gold"]
            if self.playeranimatetimer > 4:
                self.image = IMAGES["player_left"]
    def move_right(self):
        self.player_width, self.player_height = (41, 19)
        self.image = pygame.transform.rotate(IMAGES["player_left"], 180)
        self.image = pygame.transform.flip(self.image, 0, 1)
        if self.pos[0] < SCREEN_WIDTH-75:
            self.pos[0] += self.speed_x
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = pygame.transform.rotate(IMAGES["player_left_gold"], 180)
                self.image = pygame.transform.flip(self.image, 0, 1)
            if self.playeranimatetimer > 4:
                self.image = pygame.transform.rotate(IMAGES["player_left"], 180)
                self.image = pygame.transform.flip(self.image, 0, 1)
    def move_up_left(self):
        self.player_width, self.player_height = (34, 34)
        self.image = pygame.transform.flip(IMAGES["player_down_right"], 0, 1)
        self.image = pygame.transform.rotate(self.image, 90)
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = pygame.transform.flip(IMAGES["player_down_right"], 0, 1)
                self.image = pygame.transform.rotate(self.image, 90)
            if self.playeranimatetimer > 4:
                self.image = pygame.transform.flip(IMAGES["player_down_right_gold"], 0, 1)
                self.image = pygame.transform.rotate(self.image, 90)
                
        # Update position for diagonal movement
        if self.pos[1] > 50 and self.pos[0] > 32:
            self.pos[0] -= self.speed_x
            self.pos[1] -= self.speed_y
            
    def move_up_right(self):
        self.player_width, self.player_height = (34, 34)
        self.image = pygame.transform.rotate(IMAGES["player_down_right"], 90)
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = pygame.transform.rotate(IMAGES["player_down_right"], 90)
            if self.playeranimatetimer > 4:
                self.image = pygame.transform.rotate(IMAGES["player_down_right_gold"], 90)
                
        # Update position for diagonal movement
        if self.pos[1] > 50 and self.pos[0] < SCREEN_WIDTH-75:
            self.pos[0] += self.speed_x
            self.pos[1] -= self.speed_y  
            
    def move_down_left(self):
        self.player_width, self.player_height = (34, 34)
        self.image = pygame.transform.flip(IMAGES["player_down_right"], 1, 0)
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = pygame.transform.flip(IMAGES["player_down_right_gold"], 1, 0)
            if self.playeranimatetimer > 4:
                self.image = pygame.transform.flip(IMAGES["player_down_right"], 1, 0)
        
        # Update position for diagonal movement
        if self.pos[1] < SCREEN_HEIGHT-75 and self.pos[0] > 32:
            self.pos[0] -= self.speed_x
            self.pos[1] += self.speed_y
            
    def move_down_right(self):
        self.player_width, self.player_height = (34, 34)
        self.image = IMAGES["player_down_right"]
        if self.starpower == 1:
            if self.playeranimatetimer > 2:
                self.image = IMAGES["player_down_right_gold"]
            if self.playeranimatetimer > 4:
                self.image = IMAGES["player_down_right"]
                
        # Update position for diagonal movement
        if self.pos[1] < SCREEN_HEIGHT-75 and self.pos[0] < SCREEN_WIDTH-75:
            self.pos[0] += self.speed_x
            self.pos[1] += self.speed_y
            
    def collide_with_redfish(self, score, score_blit):
        score_blit = 1
        score += 1
        self.sizescore += 1
        return score, score_blit
    def collide_with_greenfish(self, score, score_blit):
        score_blit = 2
        score += 2
        self.sizescore += 2
        return score, score_blit
    def collide_with_silverfish(self, score, score_blit):
        score_blit = 3
        score += 3
        self.sizescore += 3
        return score, score_blit
    def collide_with_shark(self, score, score_blit):
        if self.starpower == 2:
            score_blit = 1
            score += 1
            self.sizescore += 1
            return score, score_blit
        elif self.starpower == 0: # Player die
            self.game_over()
            return score, score_blit
        else:
            return score, score_blit
    def collide_with_seahorse(self):
        self.speedpower = 1
        self.speed_x, self.speed_y = 9, 9
        self.speed_time_left = 500
    def collide_with_jellyfish(self):
        self.speedpower = 2
        self.sizescore = 0
        self.speed_x, self.speed_y = 2, 2
        self.speed_time_left = 500
    def collide_with_snake(self):
        self.sizescore = 0
    def collide_with_star(self):
        self.starpower = random.choice([0, 1])+1
    def game_over(self):
        pass
        #global menu_selection
        #menu_selection = GAMEOVER_SCREEN
    def get_powerup_timer_text(self, ocean_font):
        if self.starpower != 0:
            return ocean_font.render("Powerup Timer: " + str((self.powerup_time_left//100)+1), 1, (255, 255, 255))
        return ocean_font.render("", 1, (0, 0, 0))
    def get_speed_timer_text(self, ocean_font):
        if self.speedpower == 1:
            return ocean_font.render("Speed Timer: " + str((self.speed_time_left//100)+1), 1, (255, 255, 255))
        elif self.speedpower == 2:
            return ocean_font.render("Sting Timer: " + str((self.speed_time_left//100)+1), 1, (255, 255, 255))
        else:
            return ocean_font.render("", 1, (0, 0, 0))
    def remove_sprite(self):
        self.kill()

        
class GameState:
    START_SCREEN = 0
    PLAY_SCREEN = 1
    GAME_OVER_SCREEN = 2

    def __init__(self):
        self.allsprites = pygame.sprite.Group()
        self.score = 0
        self.score_blit = 0
        self.key_states = {
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_DOWN: False,
            pygame.K_RIGHT: False
        }
        self.current_state = GameState.START_SCREEN
        self.onepowerupsound = 0
        self.score_disappear_timer = 0
        self.initialize_entities()

    def initialize_entities(self):
        # Initialize all your entities here
        self.player = Player(self.allsprites)
        self.walls = []
        self.seaweeds = []
        for x_top in range(29):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (x_top*32, 0) #top walls
            self.walls.append(self.wall)
        for x_bottom in range(29):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (x_bottom*32, SCREEN_HEIGHT-32) #bottom walls
            self.walls.append(self.wall)
        for y_left in range(17):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (0, (y_left*32)+32) #left walls
            self.walls.append(self.wall)
        for y_right in range(17):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (SCREEN_WIDTH-32, (y_right*32)+32) #right walls
            self.walls.append(self.wall)
        for x_pos in range(5, SCREEN_WIDTH-15, 60):
            self.seaweed = Seaweed(self.allsprites, x_pos, SCREEN_HEIGHT-120)
            self.seaweeds.append(self.seaweed)
        self.red_fishes = [RedFish(self.allsprites) for i in range(6)]
        self.green_fishes = [GreenFish(self.allsprites) for i in range(3)]
        self.silverfish = SilverFish(self.allsprites)
        self.snake = Snake(self.allsprites)
        self.seahorse = SeaHorse(self.allsprites)
        self.jellyfishes = [JellyFish(self.allsprites) for i in range(3)]
        self.sharks = [Shark(self.allsprites) for i in range(4)]
        self.brightbluefish = BrightBlueFish(self.allsprites)
        self.star = StarPowerup(self.allsprites)
        self.rainbow_fish = RainbowFish(self.allsprites)
        
    def reset_game(self):
        self.allsprites.empty()
        self.current_state = GameState.PLAY_SCREEN
        self.score = 0
        self.initialize_entities()
        self.player.last_pressed = 0
        self.key_states = {
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_DOWN: False,
            pygame.K_RIGHT: False
        }
    
    def change_state(self, new_state):
        self.current_state = new_state
        
    def activate_game_objects(self):
        # Rainbow Fish
        if self.rainbow_fish.rainbowtimer >= 200:
            self.rainbow_fish.activate = 1
        if self.rainbow_fish.activate == 1 and self.rainbow_fish.score_exit == 0:
            if self.rainbow_fish.arrow_warning == 1 and self.rainbow_fish.rect.top < 0:
                screen.blit(IMAGES["arrow_warning_red"], (self.rainbow_fish.rect.topleft[0], 40))
                SOUNDS["snd_shark_incoming"].play()
            self.rainbow_fish.chase_player(self.player.sizescore, self.player.starpower, self.player.pos)
        # Sharks
        if self.score >= 5:
            self.sharks[0].activate = 1
            if self.sharks[0].arrow_warning == 1:
                screen.blit(IMAGES["arrow_warning_silver"], (self.sharks[0].rect.topleft[0], 40))
                SOUNDS["snd_shark_incoming"].play()
        if self.score >= 20:
            self.sharks[1].activate = 1
            if self.sharks[1].arrow_warning == 1:
                screen.blit(IMAGES["arrow_warning_silver"], (self.sharks[1].rect.topleft[0], 40))
                SOUNDS["snd_shark_incoming"].play()
        if self.score >= 45:
            self.sharks[2].activate = 1
            if self.sharks[2].arrow_warning == 1:
                screen.blit(IMAGES["arrow_warning_silver"], (self.sharks[2].rect.topleft[0], 40))
                SOUNDS["snd_shark_incoming"].play()
        if self.score >= 75:
            self.sharks[3].activate = 1
            if self.sharks[3].arrow_warning == 1:
                screen.blit(IMAGES["arrow_warning_silver"], (self.sharks[3].rect.topleft[0], 40))
                SOUNDS["snd_shark_incoming"].play()
        # Bright Blue Fish
        # Starts moving when you have a certain score
        if(self.brightbluefish.activate == 0 and (self.score % 50 >= 0 and self.score % 50 <= 2) and self.score >= 50):
            self.brightbluefish.direction = random.choice([0, 1])
            self.brightbluefish.activate = 1
            if self.brightbluefish.direction == 1: # MOVING RIGHT
                self.brightbluefish.rect.topright = (-500, random.randrange(50, SCREEN_HEIGHT-200))
            elif self.brightbluefish.direction == 0: # MOVING LEFT
                self.brightbluefish.rect.topleft = (SCREEN_WIDTH+500, random.randrange(50, SCREEN_HEIGHT-200))
        # Arrow Warning for Bright Blue Fish
        if self.brightbluefish.arrow_warning == 1:
            if self.brightbluefish.direction == 1 and self.brightbluefish.rect.topleft[0] < 0: # MOVING RIGHT
                screen.blit(IMAGES["arrow_warning_blue"], (20, self.brightbluefish.rect.midright[1]+40))
                SOUNDS["snd_siren"].play()
            elif self.brightbluefish.direction == 0 and self.brightbluefish.rect.topleft[0] > SCREEN_WIDTH: # MOVING LEFT
                screen.blit(pygame.transform.flip(IMAGES["arrow_warning_blue"], 1, 0),
                            (SCREEN_WIDTH-70, self.brightbluefish.rect.midright[1]+40))
                SOUNDS["snd_shark_incoming"].stop()
                SOUNDS["snd_siren"].play()
        # Jellyfish
        if self.score >= 0:
            self.jellyfishes[0].activate = 1
        if self.score >= 30:
            self.jellyfishes[1].activate = 1    
        if self.score == 60:
            self.jellyfishes[2].activate = 1
    def handle_collisions(self):
        ##################
        # COLLISIONS
        ##################
        for red_fish in self.red_fishes:
            if pygame.sprite.collide_mask(red_fish, self.player):
                red_fish.collide_with_player()
                self.score, self.score_blit = self.player.collide_with_redfish(self.score, self.score_blit)
                SOUNDS["snd_eat"].play()
            for greenfish in self.green_fishes:
                if red_fish.rect.colliderect(greenfish):
                    greenfish.collision_with_redfish()
                    if greenfish.image != IMAGES["spr_big_green_fish"]:
                        red_fish.collide_with_greenfish()
            if pygame.sprite.collide_mask(red_fish, self.brightbluefish):
                red_fish.collide_with_brightbluefish()
            for wall in self.walls:
                if red_fish.rect.colliderect(wall.rect):
                    red_fish.collision_with_wall(wall.rect)
        for greenfish in self.green_fishes:
            if pygame.sprite.collide_mask(greenfish, self.player):
                if(greenfish.image == IMAGES["spr_green_fish"] or 
                   greenfish.image == IMAGES["spr_green_fish_left"] or 
                   self.player.sizescore >= 40 or 
                   self.player.starpower == 1):
                    SOUNDS["snd_eat"].play()
                    self.score, self.score_blit = self.player.collide_with_greenfish(self.score, self.score_blit)
                    greenfish.small_collision_with_player()
                    greenfish.big_green_fish_score = 0
                else: # When it transforms to big green fish, player dies
                    self.current_state = GameState.GAME_OVER_SCREEN
            if pygame.sprite.collide_mask(greenfish, self.brightbluefish):
                greenfish.big_green_fish_score = 0
                greenfish.image = IMAGES["spr_green_fish"]
                greenfish.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
            for wall in self.walls:
                if greenfish.rect.colliderect(wall.rect):
                    greenfish.collision_with_wall(wall.rect)
        if pygame.sprite.collide_mask(self.silverfish, self.player):
            SOUNDS["snd_eat"].play()
            self.score, self.score_blit = self.player.collide_with_silverfish(self.score, self.score_blit)
            self.silverfish.collide_with_player()
        if pygame.sprite.collide_mask(self.silverfish, self.brightbluefish):
            SOUNDS["snd_eat"].play()
            self.silverfish.collide_with_brightbluefish()
        for shark in self.sharks:
            if pygame.sprite.collide_mask(shark, self.player):
                self.score, self.score_blit = self.player.collide_with_shark(self.score, self.score_blit)
                shark.collide_with_player()
                if self.player.starpower != 0:
                    SOUNDS["snd_eat_shark"].play()
            if pygame.sprite.collide_mask(shark, self.brightbluefish):
                shark.collide_with_brightbluefish()
                SOUNDS["snd_eat"].play()
            for wall in self.walls:
                if shark.rect.colliderect(wall.rect):
                    shark.collision_with_wall(wall.rect)
            if self.player.starpower == 2:
                shark.mini_shark = 1
            else:
                shark.mini_shark = 0
        if pygame.sprite.collide_mask(self.rainbow_fish, self.player):
            # Player eats rainbow_fish only when appears bigger (arbitrary)
            if (self.rainbow_fish.size[0]-45 <= self.player.sizescore) or (self.player.starpower == 1):
                SOUNDS["snd_eat"].play()
                self.score_blit = 2
                self.score += 2
                self.player.sizescore += 2
                self.rainbow_fish.collide_with_player()
            else:
                if self.player.starpower != 1:
                    self.current_state = GameState.GAME_OVER_SCREEN
        if pygame.sprite.collide_mask(self.rainbow_fish, self.brightbluefish):
            SOUNDS["snd_eat"].play()
            self.rainbow_fish.collide_with_brightbluefish()
        if pygame.sprite.collide_mask(self.snake, self.player):
            self.snake.collide_with_player()
            if self.player.starpower != 1:
                self.player.collide_with_snake()
                SOUNDS["snd_size_down"].play()
            else:
                SOUNDS["snd_eat"].play()
        if pygame.sprite.collide_mask(self.snake, self.brightbluefish):
            self.snake.collide_with_brightbluefish()
        if pygame.sprite.collide_mask(self.seahorse, self.player):
            self.player.collide_with_seahorse()
            self.seahorse.collide_with_player()
            SOUNDS["snd_eat"].play()
            self.onepowerupsound += 1
            if self.onepowerupsound > 1:
                SOUNDS["snd_power_up_timer"].stop()
            for i in range(0, len(SOUNDS)):
                soundslist = list(SOUNDS.keys()) #returns list of keys in sounds
                SOUNDS[soundslist[i]].stop() #stops all sounds
            SOUNDS["snd_power_up_timer"].play()
        for jellyfish in self.jellyfishes:
            if pygame.sprite.collide_mask(jellyfish, self.player):
                jellyfish.collide_with_player()
                if self.player.starpower == 1:
                    SOUNDS["snd_eat"].play()
                else:
                    self.player.collide_with_jellyfish()
                    SOUNDS["snd_size_down"].play()
                    self.onepowerupsound += 1
                    if self.onepowerupsound > 1:
                        SOUNDS["snd_power_up_timer"].stop()
                    for i in range(0, len(SOUNDS)):
                        soundslist = list(SOUNDS.keys()) # Returns list of keys in sounds
                        SOUNDS[soundslist[i]].stop() # Stops all sounds
                    SOUNDS["snd_power_up_timer"].play()
            if pygame.sprite.collide_mask(jellyfish, self.brightbluefish):
                jellyfish.collide_with_brightbluefish()
                SOUNDS["snd_eat"].play()
        if self.player.rect.colliderect(self.star):
            self.player.collide_with_star()
            self.star.collide_with_player()
            SOUNDS["snd_eat"].play()
            self.onepowerupsound += 1
            if self.onepowerupsound > 1:
                SOUNDS["snd_power_up_timer"].stop()
            for i in range(0, len(SOUNDS)):
                soundslist = list(SOUNDS.keys()) # Returns list of keys in sounds
                SOUNDS[soundslist[i]].stop() # Stops all sounds
            SOUNDS["snd_power_up_timer"].play()
        if pygame.sprite.collide_mask(self.brightbluefish, self.player):
            if self.player.starpower != 1:
                self.current_state = GameState.GAME_OVER_SCREEN
                
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.current_state != GameState.PLAY_SCREEN:
                    self.reset_game()
                if event.key in self.key_states:
                    self.key_states[event.key] = True
            if event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False

    def update(self):
        # Diagonal Movements
        if self.key_states[pygame.K_UP] and self.key_states[pygame.K_RIGHT]:
            self.player.move_up_right()
        elif self.key_states[pygame.K_UP] and self.key_states[pygame.K_LEFT]:
            self.player.move_up_left()
        elif self.key_states[pygame.K_DOWN] and self.key_states[pygame.K_RIGHT]:
            self.player.move_down_right()
        elif self.key_states[pygame.K_DOWN] and self.key_states[pygame.K_LEFT]:
            self.player.move_down_left()
    
        # Single direction movements
        elif self.key_states[pygame.K_UP]:
            self.player.move_up()
        elif self.key_states[pygame.K_DOWN]:
            self.player.move_down()
        elif self.key_states[pygame.K_LEFT]:
            self.player.move_left()
        elif self.key_states[pygame.K_RIGHT]:
            self.player.move_right()
    
        # Stop movement if no arrow keys are pressed
        if not any(self.key_states.values()):
            self.player.stop_movement()
            
        self.handle_collisions()
        self.activate_game_objects()
    
    def draw(self, screen):
        # Draw game entities
        self.allsprites.draw(screen)

# Main game loop
def main():
    
    debug_message = 0
    
    (x_first, y_first) = (0, 0)
    (x_second, y_second) = (0, -SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    
    load_image("sprites/wall.bmp", "spr_wall", True, False)
    load_image("sprites/player_left.png", "player_left", True, True)
    load_image("sprites/player_down_right.png", "player_down_right", True, True)
    load_image("sprites/player_down.png", "player_down", True, True)
    load_image("sprites/player_left_gold.png", "player_left_gold", True, True)
    load_image("sprites/player_down_right_gold.png", "player_down_right_gold", True, True)
    load_image("sprites/player_down_gold.png", "player_down_gold", True, True)
    load_image("sprites/red_fish.png", "spr_red_fish", True, True)
    load_image("sprites/green_fish.png", "spr_green_fish", True, True)
    IMAGES["spr_green_fish_left"] = pygame.transform.flip(IMAGES["spr_green_fish"], 1, 0)
    load_image("sprites/big_green_fish.png", "spr_big_green_fish", True, True)
    load_image("sprites/silver_fish.png", "spr_silver_fish", True, True)
    load_image("sprites/snake_1.png", "spr_snake", True, True)
    load_image("sprites/snake_2.png", "spr_snake_2", True, True)
    load_image("sprites/snake_3.png", "spr_snake_3", True, True)
    load_image("sprites/snake_4.png", "spr_snake_4", True, True)
    load_image("sprites/seahorse.png", "spr_seahorse", True, True)
    load_image("sprites/jellyfish_1.png", "spr_jellyfish", True, True)
    load_image("sprites/jellyfish_2.png", "spr_jellyfish_2", True, True)
    load_image("sprites/jellyfish_3.png", "spr_jellyfish_3", True, True)
    load_image("sprites/jellyfish_4.png", "spr_jellyfish_4", True, True)
    load_image("sprites/jellyfish_5.png", "spr_jellyfish_5", True, True)
    load_image("sprites/jellyfish_6.png", "spr_jellyfish_6", True, True)
    load_image("sprites/jellyfish_7.png", "spr_jellyfish_7", True, True)
    load_image("sprites/shark.png", "spr_shark", True, True)
    load_image("sprites/bright_blue_fish.png", "spr_bright_blue_fish", True, True)
    IMAGES["big_bright_blue_fish"] = pygame.transform.smoothscale(IMAGES["spr_bright_blue_fish"], (300, 200))
    IMAGES["big_bright_blue_fish_left"] = pygame.transform.flip(IMAGES["big_bright_blue_fish"], 1, 0)
    load_image("sprites/starfish_1.png", "spr_star", True, True)
    load_image("sprites/starfish_2.png", "spr_star_2", True, True)
    load_image("sprites/starfish_3.png", "spr_star_3", True, True)
    load_image("sprites/arrow_warning_red.png", "arrow_warning_red", True, True)
    load_image("sprites/arrow_warning_silver.png", "arrow_warning_silver", True, True)
    load_image("sprites/arrow_warning_blue.png", "arrow_warning_blue", True, True)
    load_image("sprites/seaweed_middle.png", "spr_seaweed", True, True)
    load_image("sprites/seaweed_left.png", "spr_seaweed_left", True, True)
    load_image("sprites/seaweed_right.png", "spr_seaweed_right", True, True)
    load_image("sprites/rainbow_fish.png", "spr_rainbow_fish", True, True)
    #font and texts
    ocean_font = pygame.font.Font("fonts/ocean_font.ttf", 16)
    ocean_font_main = pygame.font.Font("fonts/ocean_font.ttf", 48)
    font_ocean_gameover = pygame.font.Font("fonts/ocean_font.ttf", 76)
    font_arial = pygame.font.SysFont('Arial', 32)
    #backgrounds
    ground = pygame.image.load("sprites/ground.bmp").convert()
    ground = pygame.transform.scale(ground, (SCREEN_WIDTH, 100))
    bgwater = pygame.image.load("sprites/background.bmp").convert()
    bgwater = pygame.transform.scale(bgwater, (SCREEN_WIDTH, SCREEN_HEIGHT))
    blackbg = pygame.image.load("sprites/black_bg.jpg").convert()
    blackbg = pygame.transform.scale(blackbg, (SCREEN_WIDTH, 30))
    gameicon = pygame.image.load("sprites/red_fish_ico.png")
    pygame.display.set_icon(gameicon)
    pygame.display.set_caption('Fish Food')
    pygame.mouse.set_visible(0)
    load_sound("sounds/snd_eat.wav", "snd_eat")
    SOUNDS["snd_eat"].set_volume(.2)
    load_sound("sounds/eat_shark.wav", "snd_eat_shark")
    SOUNDS["snd_eat_shark"].set_volume(.2)
    load_sound("sounds/size_down.wav", "snd_size_down")
    load_sound("sounds/player_die.wav", "snd_player_die")
    SOUNDS["snd_player_die"].set_volume(.3)
    load_sound("sounds/power_up_timer.wav", "snd_power_up_timer")
    SOUNDS["snd_power_up_timer"].set_volume(.3)
    load_sound("sounds/siren.wav", "snd_siren")
    SOUNDS["snd_siren"].set_volume(.05)
    load_sound("sounds/shark_incoming.wav", "snd_shark_incoming")
    SOUNDS["snd_shark_incoming"].set_volume(.03)
    # Music loop
    pygame.mixer.music.load("sounds/game_music.mp3")
    pygame.mixer.music.set_volume(.1)
    pygame.mixer.music.play(-1)

    running = True
    game_state_manager = GameState()
    while running:
        game_state_manager.handle_input()
        if game_state_manager.current_state == GameState.PLAY_SCREEN:
            # Update
            game_state_manager.update()
            game_state_manager.allsprites.update()
            
            ##################
            # Draw menus for in-game
            ##################
            # Water background movement
            y_first += 10
            y_second += 10
            screen.blit(bgwater, (x_first, y_first))
            screen.blit(bgwater, (x_second, y_second))
            if y_second > SCREEN_HEIGHT:
                y_second = -SCREEN_HEIGHT
            if y_first > SCREEN_HEIGHT:
                y_first = -SCREEN_HEIGHT
            screen.blit(ground, (0, SCREEN_HEIGHT-100))

            # Check for collisions
            if pygame.sprite.spritecollideany(game_state_manager.player, game_state_manager.sharks):
                game_state_manager.current_state = GameState.GAME_OVER_SCREEN

            # Draw
            # screen.fill((0, 0, 0))  # Fill screen with black
            game_state_manager.allsprites.draw(screen)
            
            # Menu Design
            screen.blit(blackbg, (0, 0))
            menu_text = ocean_font.render("Menu:", 1, (255, 255, 255))
            screen.blit(menu_text, (10, 5))
            screen.blit(IMAGES["spr_red_fish"], (65, 11))
            screen.blit(IMAGES["spr_green_fish"], (90, 11))
            screen.blit(IMAGES["spr_silver_fish"], (120, 9))
            if game_state_manager.rainbow_fish.size[0]-45 <= game_state_manager.player.sizescore: #55 is orig size
                blitted_rainbow_fish = pygame.transform.smoothscale(IMAGES["spr_rainbow_fish"], (24, 17))
                screen.blit(blitted_rainbow_fish, (158, 6))
            else:
                screen.blit(ocean_font.render("", 1, (0, 0, 0)), (158, 6))
            if game_state_manager.player.sizescore >= 40:
                blitted_Big_Green_Fish = pygame.transform.smoothscale(IMAGES["spr_big_green_fish"], (24, 15))
                screen.blit(blitted_Big_Green_Fish, (189, 7))
            else:
                screen.blit(ocean_font.render("", 1, (0, 0, 0)), (189, 7))
            if game_state_manager.player.starpower == 2:
                blittedshark = pygame.transform.smoothscale(IMAGES["spr_shark"], (24, 15))
                screen.blit(blittedshark, (220, 7))
            else:
                screen.blit(ocean_font.render("", 1, (0, 0, 0)), (220, 7))

            # Font On Top of Playing Screen
            score_text = ocean_font.render("Score: " + str(game_state_manager.score), 1, (255, 255, 255))
            screen.blit(score_text, ((SCREEN_WIDTH/2)-32, 5))
            game_state_manager.player.get_powerup_timer_text(ocean_font)
            game_state_manager.player.get_speed_timer_text(ocean_font)
            screen.blit(game_state_manager.player.get_powerup_timer_text(ocean_font), (732, 5))
            screen.blit(game_state_manager.player.get_speed_timer_text(ocean_font), (550, 5))
            if game_state_manager.score_blit == 0:
                SCORE_BLIT_TEXT = ocean_font.render("", 1, (255, 255, 255))
            else:
                SCORE_BLIT_TEXT = ocean_font.render("+" + str(game_state_manager.score_blit), 1, (255, 255, 255))
                if game_state_manager.score_disappear_timer > 10:
                    game_state_manager.score_blit = 0
                    game_state_manager.score_disappear_timer = 0
            screen.blit(SCORE_BLIT_TEXT, (game_state_manager.player.pos[0]+13, 
                                          game_state_manager.player.pos[1]-25-(game_state_manager.player.sizescore/2)))
            
            if game_state_manager.score_blit > 0: # Score Timer above player sprite
                game_state_manager.score_disappear_timer += 1
            ##################
            # Sound Checks
            ##################
            if game_state_manager.player.starpower == 0: # Powerup is over on the player
                game_state_manager.onepowerupsound -= 1
                SOUNDS["snd_power_up_timer"].stop()
            if game_state_manager.player.speed_time_left < 0:
                game_state_manager.onepowerupsound -= 1
                SOUNDS["snd_power_up_timer"].stop()

        elif game_state_manager.current_state == GameState.START_SCREEN:
            screen.fill((0, 0, 0))
            start_text = font.render("Press SPACE to start", True, (255, 255, 255))
            screen.blit(start_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        elif game_state_manager.current_state == GameState.GAME_OVER_SCREEN:
            screen.fill((0, 0, 0))
            game_over_text = font.render("Game Over. Press SPACE to restart", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

        # Yield control to the asyncio event loop
        # asyncio.sleep(0)

    pygame.quit()

# Run the game
#asyncio.run(main())
main()