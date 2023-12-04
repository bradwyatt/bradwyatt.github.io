import asyncio
import pygame
import os
import random
import sys
from pygame.constants import RLEACCEL
import datetime
from utils import IMAGES, SOUNDS, FONTS, load_sound, load_image, load_font, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from shark import Shark
from red_fish import RedFish
from green_fish import GreenFish
from silver_fish import SilverFish
from snake import Snake
from bright_blue_fish import BrightBlueFish
from rainbow_fish import RainbowFish
from seahorse import Seahorse
from jellyfish import Jellyfish
from star_powerup import StarPowerup
from player import Player


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish Food")
gameicon = pygame.image.load("sprites/red_fish_ico.png")
pygame.display.set_icon(gameicon)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def load_all_assets():
    load_image("sprites/coral_reef.png", "spr_wall", True, True)
    load_image("sprites/player_left.png", "player_left", True, True)
    load_image("sprites/player_down_left.png", "player_down_left", True, True)
    load_image("sprites/player_down.png", "player_down", True, True)
    load_image("sprites/player_down_right.png", "player_down_right", True, True)
    load_image("sprites/player_right.png", "player_right", True, True)
    load_image("sprites/player_up_right.png", "player_up_right", True, True)
    load_image("sprites/player_up.png", "player_up", True, True)
    load_image("sprites/player_up_left.png", "player_up_left", True, True)
    load_image("sprites/player_left_gold.png", "player_left_gold", True, True)
    load_image("sprites/player_down_left_gold.png", "player_down_left_gold", True, True)
    load_image("sprites/player_down_gold.png", "player_down_gold", True, True)
    load_image("sprites/player_down_right_gold.png", "player_down_right_gold", True, True)
    load_image("sprites/player_right_gold.png", "player_right_gold", True, True)
    load_image("sprites/player_up_right_gold.png", "player_up_right_gold", True, True)
    load_image("sprites/player_up_gold.png", "player_up_gold", True, True)
    load_image("sprites/player_up_left_gold.png", "player_up_left_gold", True, True)
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
    # arrow keys
    load_image("sprites/pressed_arrow_up.png", "spr_pressed_arrow_up", True, True, 128)
    load_image("sprites/pressed_arrow_up_right.png", "spr_pressed_arrow_up_right", True, True, 128)
    load_image("sprites/pressed_arrow_right.png", "spr_pressed_arrow_right", True, True, 128)
    load_image("sprites/pressed_arrow_down_right.png", "spr_pressed_arrow_down_right", True, True, 128)
    load_image("sprites/pressed_arrow_down.png", "spr_pressed_arrow_down", True, True, 128)
    load_image("sprites/pressed_arrow_down_left.png", "spr_pressed_arrow_down_left", True, True, 128)
    load_image("sprites/pressed_arrow_left.png", "spr_pressed_arrow_left", True, True, 128)
    load_image("sprites/pressed_arrow_up_left.png", "spr_pressed_arrow_up_left", True, True, 128)
    load_image("sprites/unpressed_arrow_up.png", "spr_unpressed_arrow_up", True, True, 64)
    load_image("sprites/unpressed_arrow_up_right.png", "spr_unpressed_arrow_up_right", True, True, 64)
    load_image("sprites/unpressed_arrow_right.png", "spr_unpressed_arrow_right", True, True, 64)
    load_image("sprites/unpressed_arrow_down_right.png", "spr_unpressed_arrow_down_right", True, True, 64)
    load_image("sprites/unpressed_arrow_down.png", "spr_unpressed_arrow_down", True, True, 64)
    load_image("sprites/unpressed_arrow_down_left.png", "spr_unpressed_arrow_down_left", True, True, 64)
    load_image("sprites/unpressed_arrow_left.png", "spr_unpressed_arrow_left", True, True, 64)
    load_image("sprites/unpressed_arrow_up_left.png", "spr_unpressed_arrow_up_left", True, True, 64)
    
    
    #font and texts
    load_font("fonts/ocean_font.ttf", 16, False)
    load_font("fonts/ocean_font.ttf", 48)
    load_font("fonts/ocean_font.ttf", 76)
    load_font("Arial", 32, is_system_font=True)
    #backgrounds
    load_image("sprites/ground.jpg", "ground", False, True).convert()
    load_image("sprites/play_background.jpg", "play_background", False, True).convert()
    #bgwater = pygame.transform.scale(bgwater, (SCREEN_WIDTH, SCREEN_HEIGHT))
    available_prey_layer = load_image("sprites/available_prey_layer.jpg", "available_prey_layer", False, True).convert()
    IMAGES['available_prey_layer'] = pygame.transform.scale(available_prey_layer, (SCREEN_WIDTH, 30))
    start_menu_bg = load_image("sprites/start_menu.png", "start_menu_bg", False, True).convert()
    load_image("sprites/info_screen.jpg", "info_screen_bg", False, True).convert()
    pygame.mouse.set_visible(True)
    load_sound("sounds/snd_eat.wav", "snd_eat")
    SOUNDS["snd_eat"].set_volume(.2)
    load_sound("sounds/eat_shark.wav", "snd_eat_shark")
    SOUNDS["snd_eat_shark"].set_volume(.2)
    load_sound("sounds/size_down.wav", "snd_size_down")
    load_sound("sounds/player_die.wav", "snd_player_die")
    SOUNDS["snd_player_die"].set_volume(.3)
    load_sound("sounds/powerup_timer.wav", "snd_powerup_timer")
    SOUNDS["snd_powerup_timer"].set_volume(.3)
    load_sound("sounds/siren.wav", "snd_siren")
    SOUNDS["snd_siren"].set_volume(.05)
    load_sound("sounds/shark_incoming.wav", "snd_shark_incoming")
    SOUNDS["snd_shark_incoming"].set_volume(.03)
    # Music loop
    #pygame.mixer.music.load("sounds/game_music.mp3")
    #pygame.mixer.music.set_volume(.1)
    #pygame.mixer.music.play(-1)

def draw_text_button(screen, text, font, color, rect):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    pygame.draw.rect(screen, (0, 0, 0), rect)  # Draw button rectangle
    screen.blit(text_surf, text_rect)
    return rect.collidepoint(pygame.mouse.get_pos())

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
        
class GameState:
    START_SCREEN = 0
    PLAY_SCREEN = 1
    GAME_OVER_SCREEN = 2
    INFO_SCREEN = 3

    def __init__(self, images, start_screen_bg=None, info_screen_bg=None, joystick=None):
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
        self.one_powerup_sound = 0
        self.score_disappear_timer = 0
        self.initialize_entities()
        self.start_screen_bg = start_screen_bg
        self.info_screen_bg = info_screen_bg
        self.is_paused = False
        self.joystick = joystick

    def initialize_entities(self):
        # Initialize all your entities here
        self.player = Player(self.allsprites, IMAGES)
        self.walls = []
        self.seaweeds = []
        for x_top in range(29):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (x_top*32, 0) #top walls
            self.walls.append(self.wall)
        for x_bottom in range(32, SCREEN_WIDTH-32, 32):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (x_bottom, SCREEN_HEIGHT-32) #bottom walls
            self.walls.append(self.wall)
        for y_left in range(0, SCREEN_HEIGHT-32, 32):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (0, y_left) #left walls
            self.walls.append(self.wall)
        for y_right in range(0, SCREEN_HEIGHT-32, 32):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (SCREEN_WIDTH-32, y_right) #right walls
            self.walls.append(self.wall)
        for x_pos in range(5, SCREEN_WIDTH-15, 60):
            self.seaweed = Seaweed(self.allsprites, x_pos, SCREEN_HEIGHT-200)
            self.seaweeds.append(self.seaweed)
        self.red_fishes = [RedFish(self.allsprites, IMAGES) for i in range(6)]
        self.green_fishes = [GreenFish(self.allsprites, IMAGES) for i in range(3)]
        self.silver_fish = SilverFish(self.allsprites, IMAGES)
        self.snake = Snake(self.allsprites, IMAGES)
        self.seahorse = Seahorse(self.allsprites, IMAGES)
        self.jellyfishes = [Jellyfish(self.allsprites, IMAGES) for i in range(3)]
        self.sharks = [Shark(self.allsprites, IMAGES) for i in range(4)]
        self.bright_blue_fish = BrightBlueFish(self.allsprites, IMAGES)
        self.star = StarPowerup(self.allsprites, IMAGES)
        self.rainbow_fish = RainbowFish(self.allsprites, IMAGES)
        
    def reset_game(self, images):
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
        if self.rainbow_fish.rainbow_timer >= 200:
            self.rainbow_fish.activate = 1
        if self.rainbow_fish.activate == 1 and self.rainbow_fish.score_exit == 0:
            if self.rainbow_fish.arrow_warning == 1 and self.rainbow_fish.rect.top < 0:
                screen.blit(IMAGES["arrow_warning_red"], (self.rainbow_fish.rect.topleft[0], 40))
                SOUNDS["snd_shark_incoming"].play()
            self.rainbow_fish.chase_player(self.player.size_score, self.player.star_power, self.player.pos)
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
        if(self.bright_blue_fish.activate == 0 and (self.score % 50 >= 0 and self.score % 50 <= 2) and self.score >= 50):
            self.bright_blue_fish.direction = random.choice([0, 1])
            self.bright_blue_fish.activate = 1
            if self.bright_blue_fish.direction == 1: # MOVING RIGHT
                self.bright_blue_fish.rect.topright = (-500, random.randrange(50, SCREEN_HEIGHT-200))
            elif self.bright_blue_fish.direction == 0: # MOVING LEFT
                self.bright_blue_fish.rect.topleft = (SCREEN_WIDTH+500, random.randrange(50, SCREEN_HEIGHT-200))
        # Arrow Warning for Bright Blue Fish
        if self.bright_blue_fish.arrow_warning == 1:
            if self.bright_blue_fish.direction == 1 and self.bright_blue_fish.rect.topleft[0] < 0: # MOVING RIGHT
                screen.blit(IMAGES["arrow_warning_blue"], (20, self.bright_blue_fish.rect.midright[1]+40))
                SOUNDS["snd_siren"].play()
            elif self.bright_blue_fish.direction == 0 and self.bright_blue_fish.rect.topleft[0] > SCREEN_WIDTH: # MOVING LEFT
                screen.blit(pygame.transform.flip(IMAGES["arrow_warning_blue"], 1, 0),
                            (SCREEN_WIDTH-70, self.bright_blue_fish.rect.midright[1]+40))
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
                self.score, self.score_blit = self.player.collide_with_red_fish(self.score, self.score_blit)
                SOUNDS["snd_eat"].play()
            for green_fish in self.green_fishes:
                if red_fish.rect.colliderect(green_fish):
                    green_fish.collision_with_redfish()
                    if green_fish.image != IMAGES["spr_big_green_fish"]:
                        red_fish.collide_with_green_fish()
            if pygame.sprite.collide_mask(red_fish, self.bright_blue_fish):
                red_fish.collide_with_bright_blue_fish()
            for wall in self.walls:
                if red_fish.rect.colliderect(wall.rect):
                    red_fish.collision_with_wall(wall.rect)
        for green_fish in self.green_fishes:
            if pygame.sprite.collide_mask(green_fish, self.player):
                if(green_fish.image == IMAGES["spr_green_fish"] or 
                   green_fish.image == IMAGES["spr_green_fish_left"] or 
                   self.player.size_score >= 40 or 
                   self.player.star_power == 1):
                    SOUNDS["snd_eat"].play()
                    self.score, self.score_blit = self.player.collide_with_green_fish(self.score, self.score_blit)
                    green_fish.small_collision_with_player()
                    green_fish.big_green_fish_score = 0
                else: # When it transforms to big green fish, player dies
                    self.current_state = GameState.GAME_OVER_SCREEN
            if pygame.sprite.collide_mask(green_fish, self.bright_blue_fish):
                green_fish.big_green_fish_score = 0
                green_fish.image = IMAGES["spr_green_fish"]
                green_fish.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), random.randrange(100, SCREEN_HEIGHT-100))
            for wall in self.walls:
                if green_fish.rect.colliderect(wall.rect):
                    green_fish.collision_with_wall(wall.rect)
        if pygame.sprite.collide_mask(self.silver_fish, self.player):
            SOUNDS["snd_eat"].play()
            self.score, self.score_blit = self.player.collide_with_silver_fish(self.score, self.score_blit)
            self.silver_fish.collide_with_player()
        if pygame.sprite.collide_mask(self.silver_fish, self.bright_blue_fish):
            SOUNDS["snd_eat"].play()
            self.silver_fish.collide_with_bright_blue_fish()
        for shark in self.sharks:
            if pygame.sprite.collide_mask(shark, self.player):
                self.score, self.score_blit = self.player.collide_with_shark(self.score, self.score_blit)
                shark.collide_with_player()
                if self.player.star_power != 0:
                    SOUNDS["snd_eat_shark"].play()
                else:
                    self.current_state = GameState.GAME_OVER_SCREEN
            if pygame.sprite.collide_mask(shark, self.bright_blue_fish):
                shark.collide_with_bright_blue_fish()
                SOUNDS["snd_eat"].play()
            for wall in self.walls:
                if shark.rect.colliderect(wall.rect):
                    shark.collision_with_wall(wall.rect)
            if self.player.star_power == 2:
                shark.mini_shark = 1
            else:
                shark.mini_shark = 0
        if pygame.sprite.collide_mask(self.rainbow_fish, self.player):
            # Player eats rainbow_fish only when appears bigger (arbitrary)
            if (self.rainbow_fish.size[0]-45 <= self.player.size_score) or (self.player.star_power == 1):
                SOUNDS["snd_eat"].play()
                self.score_blit = 2
                self.score += 2
                self.player.size_score += 2
                self.rainbow_fish.collide_with_player()
            else:
                if self.player.star_power != 1:
                    self.current_state = GameState.GAME_OVER_SCREEN
        if pygame.sprite.collide_mask(self.rainbow_fish, self.bright_blue_fish):
            SOUNDS["snd_eat"].play()
            self.rainbow_fish.collide_with_bright_blue_fish()
        if pygame.sprite.collide_mask(self.snake, self.player):
            self.snake.collide_with_player()
            if self.player.star_power != 1:
                self.player.collide_with_snake()
                SOUNDS["snd_size_down"].play()
            else:
                SOUNDS["snd_eat"].play()
        if pygame.sprite.collide_mask(self.snake, self.bright_blue_fish):
            self.snake.collide_with_bright_blue_fish()
        if pygame.sprite.collide_mask(self.seahorse, self.player):
            self.player.collide_with_seahorse()
            self.seahorse.collide_with_player()
            SOUNDS["snd_eat"].play()
            self.one_powerup_sound += 1
            if self.one_powerup_sound > 1:
                SOUNDS["snd_powerup_timer"].stop()
            for i in range(0, len(SOUNDS)):
                sounds_list = list(SOUNDS.keys()) #returns list of keys in sounds
                SOUNDS[sounds_list[i]].stop() #stops all sounds
            SOUNDS["snd_powerup_timer"].play()
        for jellyfish in self.jellyfishes:
            if pygame.sprite.collide_mask(jellyfish, self.player):
                jellyfish.collide_with_player()
                if self.player.star_power == 1:
                    SOUNDS["snd_eat"].play()
                else:
                    self.player.collide_with_jellyfish()
                    SOUNDS["snd_size_down"].play()
                    self.one_powerup_sound += 1
                    if self.one_powerup_sound > 1:
                        SOUNDS["snd_powerup_timer"].stop()
                    for i in range(0, len(SOUNDS)):
                        sounds_list = list(SOUNDS.keys()) # Returns list of keys in sounds
                        SOUNDS[sounds_list[i]].stop() # Stops all sounds
                    SOUNDS["snd_powerup_timer"].play()
            if pygame.sprite.collide_mask(jellyfish, self.bright_blue_fish):
                jellyfish.collide_with_bright_blue_fish()
                SOUNDS["snd_eat"].play()
        if self.player.rect.colliderect(self.star):
            self.player.collide_with_star()
            self.star.collide_with_player()
            SOUNDS["snd_eat"].play()
            self.one_powerup_sound += 1
            if self.one_powerup_sound > 1:
                SOUNDS["snd_powerup_timer"].stop()
            for i in range(0, len(SOUNDS)):
                sounds_list = list(SOUNDS.keys()) # Returns list of keys in sounds
                SOUNDS[sounds_list[i]].stop() # Stops all sounds
            SOUNDS["snd_powerup_timer"].play()
        if pygame.sprite.collide_mask(self.bright_blue_fish, self.player):
            if self.player.star_power != 1:
                self.current_state = GameState.GAME_OVER_SCREEN
                
    def handle_input(self, pause_button_rect):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_states:
                    self.key_states[event.key] = True
    
            if event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False
                    
            if self.current_state == GameState.GAME_OVER_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game(IMAGES)
            elif self.current_state == GameState.START_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    info_button_rect = pygame.Rect(500, 400, 200, 50)
                    start_button_rect = pygame.Rect(500, 250, 200, 50)
                    if info_button_rect.collidepoint(event.pos):
                        self.change_state(GameState.INFO_SCREEN)
                    elif start_button_rect.collidepoint(event.pos):
                        self.change_state(GameState.PLAY_SCREEN)
            elif self.current_state == GameState.INFO_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clicking anywhere on the Info screen returns to the Start screen
                    self.change_state(GameState.START_SCREEN)
            elif self.current_state == GameState.PLAY_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Reset key_states here when the mouse button is pressed
                    for key in self.key_states:
                        self.key_states[key] = False
            
                    direction = self.joystick.handle_click(event.pos)
                    if pause_button_rect.collidepoint(event.pos):
                        self.is_paused = not self.is_paused
                    else:
                        for key in self.map_direction_to_key(direction):
                            self.key_states[key] = True
        
                if event.type == pygame.MOUSEMOTION:
                    if self.joystick.mouse_is_pressed:
                        new_direction = self.joystick.handle_mouse_move(event.pos)
                        if new_direction:
                            for key in self.key_states:
                                self.key_states[key] = False
                            for key in self.map_direction_to_key(new_direction):
                                self.key_states[key] = True


            
                if event.type == pygame.MOUSEBUTTONUP:
                    self.joystick.handle_mouse_up()
                    self.joystick.pressed_direction = None
                    for key in self.key_states:
                        self.key_states[key] = False
                        
    def map_direction_to_key(self, direction):
        mapping = {
            "up": [pygame.K_UP],
            "up_right": [pygame.K_UP, pygame.K_RIGHT],
            "right": [pygame.K_RIGHT],
            "down_right": [pygame.K_DOWN, pygame.K_RIGHT],
            "down": [pygame.K_DOWN],
            "down_left": [pygame.K_DOWN, pygame.K_LEFT],
            "left": [pygame.K_LEFT],
            "up_left": [pygame.K_UP, pygame.K_LEFT]
        }
        return mapping.get(direction, [])


                    
    def show_start_screen(self, screen):
        if self.start_screen_bg:
            # Draw the background image
            screen.blit(self.start_screen_bg, (0, 0))
        else:
            # Fallback to a black screen if no image is provided
            screen.fill((0, 0, 0))

        # Draw the "Click to Start" button
        start_button_rect = pygame.Rect(500, 250, 200, 50)  # Adjust position and size as needed
        if draw_text_button(screen, "Click to Start", pygame.font.SysFont(None, 36), (255, 255, 255), start_button_rect):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        self.change_state(GameState.PLAY_SCREEN)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def show_info_screen(self, screen):
        if self.info_screen_bg:
            screen.blit(self.info_screen_bg, (0, 0))
        else:
            screen.fill((0, 0, 0))

    def show_game_over_screen(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)
        text = font.render("Game Over. Click to restart", True, (255, 255, 255))
        
        # Center the text
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        screen.blit(text, text_rect)

    def update(self):
        self.handle_collisions()
        self.activate_game_objects()
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
    
    def draw(self, screen):
        # Draw game entities
        self.allsprites.draw(screen)

class Joystick:
    def __init__(self, images, screen):
        self.images = images
        self.screen = screen
        self.pressed_direction = None  # To track the currently pressed direction
        # Define the positions and sizes of the arrows
        self.arrows = {
            "up_left": self.images["spr_unpressed_arrow_up_left"].get_rect(topleft=(20, SCREEN_HEIGHT - 280)),
            "up_right": self.images["spr_unpressed_arrow_up_right"].get_rect(topleft=(200, SCREEN_HEIGHT - 280)),
            "down_left": self.images["spr_unpressed_arrow_down_left"].get_rect(topleft=(20, SCREEN_HEIGHT - 100)),
            "down_right": self.images["spr_unpressed_arrow_down_right"].get_rect(topleft=(200, SCREEN_HEIGHT - 100)),
            "up": self.images["spr_unpressed_arrow_up"].get_rect(topleft=(110, SCREEN_HEIGHT - 280)),
            "down": self.images["spr_unpressed_arrow_down"].get_rect(topleft=(110, SCREEN_HEIGHT - 100)),
            "left": self.images["spr_unpressed_arrow_left"].get_rect(topleft=(20, SCREEN_HEIGHT - 190)),
            "right": self.images["spr_unpressed_arrow_right"].get_rect(topleft=(200, SCREEN_HEIGHT - 190))
        }
        
        # Mapping of keyboard keys to joystick directions
        self.key_to_direction = {
             (pygame.K_UP,): "up",
             (pygame.K_DOWN,): "down",
             (pygame.K_LEFT,): "left",
             (pygame.K_RIGHT,): "right",
             (pygame.K_UP, pygame.K_RIGHT): "up_right",
             (pygame.K_UP, pygame.K_LEFT): "up_left",
             (pygame.K_DOWN, pygame.K_RIGHT): "down_right",
             (pygame.K_DOWN, pygame.K_LEFT): "down_left",
         }
        self.mouse_is_pressed = False
    
    def draw(self, key_states):
        diagonals_active = set()

        # Check and draw diagonals first
        for keys, direction in self.key_to_direction.items():
            if len(keys) > 1:  # Diagonal direction
                is_pressed = all(key_states.get(key, False) for key in keys)
                if is_pressed:
                    diagonals_active.add(direction)
                self.blit_arrow(direction, is_pressed)

        # Draw individual directions
        for keys, direction in self.key_to_direction.items():
            if len(keys) == 1:  # Individual direction
                # Check if diagonal is active
                diagonal_active = any(direction in diag for diag in diagonals_active)
                is_pressed = key_states.get(keys[0], False) and not diagonal_active
                self.blit_arrow(direction, is_pressed)

    def blit_arrow(self, direction, is_pressed):
        image_key = "spr_pressed_arrow_" if is_pressed else "spr_unpressed_arrow_"
        image_key += direction
        rect = self.arrows[direction]
        self.screen.blit(self.images[image_key], rect.topleft)

    def handle_click(self, mouse_pos):
        for direction, rect in self.arrows.items():
            if rect.collidepoint(mouse_pos):
                self.pressed_direction = direction
                self.mouse_is_pressed = True
                return direction
        return None
    
    def handle_mouse_up(self):
        self.mouse_is_pressed = False
        
    def handle_mouse_move(self, mouse_pos):
        if not self.mouse_is_pressed:
            return None
    
        for direction, rect in self.arrows.items():
            if rect.collidepoint(mouse_pos):
                if self.pressed_direction != direction:
                    self.pressed_direction = direction
                    return direction # Return the new direction
        return None # Return None if no new direction is detected


# Main game loop
async def main():
    # Define Pause Button Properties
    pause_button_size = (75, 25)  # Width and height
    pause_button_color = (255, 255, 255)  # White color
    pause_button_position = (SCREEN_WIDTH - 80, 3)  # Top right
    pause_button_rect = pygame.Rect(pause_button_position, pause_button_size)
    pause_text_surface = pygame.font.SysFont('Arial', 16).render("Pause", True, (0, 0, 0))  # Black text.render(pause_text, True, (0, 0, 0))  # Black text
    # Calculate position to center the text in the button
    pause_text_x = pause_button_rect.x + (pause_button_rect.width - pause_text_surface.get_width()) // 2
    pause_text_y = pause_button_rect.y + (pause_button_rect.height - pause_text_surface.get_height()) // 2
    
    debug_message = 0
    
    (x_first, y_first) = (0, 0)
    (x_second, y_second) = (0, -SCREEN_HEIGHT)
    load_all_assets()

    running = True
    joystick = Joystick(IMAGES, screen)
    game_state_manager = GameState(IMAGES, IMAGES['start_menu_bg'], IMAGES['info_screen_bg'], joystick)
    while running:
        clock.tick(FPS)
        game_state_manager.handle_input(pause_button_rect)
        # Clear the screen (fill with a background color or image)
        screen.fill((0, 0, 0))
        if game_state_manager.current_state == GameState.INFO_SCREEN:
            game_state_manager.show_info_screen(screen)
        elif game_state_manager.current_state == GameState.START_SCREEN:
            game_state_manager.show_start_screen(screen)
            # Draw the info button and check for hover
            info_button_rect = pygame.Rect(500, 400, 200, 50)  # Adjust as needed
            if draw_text_button(screen, "Info", pygame.font.SysFont(None, 36), (255, 255, 255), info_button_rect):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if info_button_rect.collidepoint(event.pos):
                            game_state_manager.change_state(GameState.INFO_SCREEN)
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
        elif game_state_manager.current_state == GameState.GAME_OVER_SCREEN:
            game_state_manager.show_game_over_screen(screen)
        elif game_state_manager.current_state == GameState.PLAY_SCREEN:
            
            
            ##################
            # Draw menus for in-game
            ##################
            # Water background movement
            y_first += 10
            y_second += 10

            if y_first >= SCREEN_HEIGHT:
                y_first = -SCREEN_HEIGHT
            if y_second >= SCREEN_HEIGHT:
                y_second = -SCREEN_HEIGHT
                
            screen.blit(IMAGES['play_background'], (0, y_first))
            screen.blit(IMAGES['play_background'], (0, y_second))

            screen.blit(IMAGES['ground'], (0, SCREEN_HEIGHT-100))

            # Update game state only if the game is not paused
            if not game_state_manager.is_paused:
                game_state_manager.allsprites.update()
                game_state_manager.update()
                
            # Draw sprites and game elements regardless of pause state
            game_state_manager.allsprites.draw(screen)
            joystick.draw(game_state_manager.key_states)
            

                
            # Menu Design
            screen.blit(IMAGES['available_prey_layer'], (0, 0))
            
            # Render and blit the "Available Prey:" text
            available_prey_text = FONTS['ocean_font_16'].render("Available Prey:", True, (255, 255, 255))
            text_rect = available_prey_text.get_rect(topleft=(10, 5))  # topleft position of the text
            screen.blit(available_prey_text, text_rect)
            
            # Draw Pause Button
            pygame.draw.rect(screen, pause_button_color, pause_button_rect)
            screen.blit(pause_text_surface, (pause_text_x, pause_text_y))
            
            # Starting position for the first icon
            icon_x = text_rect.right + 10  # 10 is a buffer; adjust as needed
            icon_y = 10  # Y position for icons
            
            # Blit each icon with a buffer space in between
            icon_buffer = 10  # Space between icons
            
            # Blit standard icons
            standard_icons = ['spr_red_fish', 'spr_green_fish', 'spr_silver_fish']
            for icon_key in standard_icons:
                icon = IMAGES[icon_key]
                screen.blit(icon, (icon_x, icon_y))
                icon_x += icon.get_width() + icon_buffer
            
            # Blit scaled icons conditionally
            scaled_icon_size = (24, 15)  # Adjust the size as needed
            
            if game_state_manager.rainbow_fish.size[0]-45 <= game_state_manager.player.size_score:
                blitted_rainbow_fish = pygame.transform.smoothscale(IMAGES["spr_rainbow_fish"], scaled_icon_size)
                screen.blit(blitted_rainbow_fish, (icon_x, icon_y))
                icon_x += blitted_rainbow_fish.get_width() + icon_buffer
            
            if game_state_manager.player.size_score >= 40:
                blitted_big_green_fish = pygame.transform.smoothscale(IMAGES["spr_big_green_fish"], scaled_icon_size)
                screen.blit(blitted_big_green_fish, (icon_x, icon_y))
                icon_x += blitted_big_green_fish.get_width() + icon_buffer
            
            if game_state_manager.player.star_power == 2:
                blitted_shark = pygame.transform.smoothscale(IMAGES["spr_shark"], scaled_icon_size)
                screen.blit(blitted_shark, (icon_x, icon_y))
                icon_x += blitted_shark.get_width() + icon_buffer


            # Font On Top of Playing Screen
            score_text = FONTS['ocean_font_16'].render("Score: " + str(game_state_manager.score), 1, (255, 255, 255))
            screen.blit(score_text, ((SCREEN_WIDTH/2)-32, 5))
            game_state_manager.player.get_powerup_timer_text(FONTS['ocean_font_16'])
            game_state_manager.player.get_speed_timer_text(FONTS['ocean_font_16'])
            screen_width_percentage = 0.75  # 75% of screen width
            x_position_powerup_timer = SCREEN_WIDTH * screen_width_percentage
            screen.blit(game_state_manager.player.get_powerup_timer_text(FONTS['ocean_font_16']), (x_position_powerup_timer, 5))
            screen_width_percentage = 0.6  # 60% of screen width
            x_position_speed_timer = SCREEN_WIDTH * screen_width_percentage
            screen.blit(game_state_manager.player.get_speed_timer_text(FONTS['ocean_font_16']), (x_position_speed_timer, 5))
            if game_state_manager.score_blit == 0:
                SCORE_BLIT_TEXT = FONTS['ocean_font_16'].render("", 1, (255, 255, 255))
            else:
                SCORE_BLIT_TEXT = FONTS['ocean_font_16'].render("+" + str(game_state_manager.score_blit), 1, (255, 255, 255))
                if game_state_manager.score_disappear_timer > 10:
                    game_state_manager.score_blit = 0
                    game_state_manager.score_disappear_timer = 0
            screen.blit(SCORE_BLIT_TEXT, (game_state_manager.player.pos[0]+13, 
                                          game_state_manager.player.pos[1]-25-(game_state_manager.player.size_score/2)))
            
            if game_state_manager.score_blit > 0: # Score Timer above player sprite
                game_state_manager.score_disappear_timer += 1
                
            
            
            
            ##################
            # Sound Checks
            ##################
            if game_state_manager.player.star_power == 0: # Powerup is over on the player
                game_state_manager.one_powerup_sound -= 1
                SOUNDS["snd_powerup_timer"].stop()
            if game_state_manager.player.speed_time_left < 0:
                game_state_manager.one_powerup_sound -= 1
                SOUNDS["snd_powerup_timer"].stop()

        # Update the display
        pygame.display.flip()
        
        await asyncio.sleep(0)

    pygame.quit()

# Run the game
asyncio.run(main())