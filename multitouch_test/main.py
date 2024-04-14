import pygame
import sys
import random
import asyncio

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
background_color = (30, 30, 30)
button_color = (70, 130, 180)  # Steel Blue
active_color = (144, 238, 144)  # Light Green
text_color = (255, 255, 255)  # White

# Font for scoring
font = pygame.font.Font(None, 74)

# Button rectangles
button_size = (150, 100)  # width, height
button_a = pygame.Rect(random.randint(0, screen_width - button_size[0]),
                       random.randint(0, screen_height - button_size[1]),
                       *button_size)
button_b = pygame.Rect(random.randint(0, screen_width - button_size[0]),
                       random.randint(0, screen_height - button_size[1]),
                       *button_size)

# Score
score = 0

# Converts normalized touch position to screen position
def touch_pos_to_screen(x, y):
    return int(x * screen_width), int(y * screen_height)

async def game_loop():
    global button_a, button_b, score
    running = True
    mouse_pressed = False  # Tracks if the mouse is being held down
    # Flags to track if the button is activated by dragging
    button_a_active = False
    button_b_active = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
                # Deactivate buttons if the mouse is released
                button_a_active = button_b_active = False
            elif event.type == pygame.FINGERDOWN:
                touch_pos = touch_pos_to_screen(event.x, event.y)
                if button_a.collidepoint(touch_pos):
                    button_a_active = True
                if button_b.collidepoint(touch_pos):
                    button_b_active = True
            elif event.type == pygame.MOUSEMOTION:
                if mouse_pressed:
                    # Activate button if dragged onto and deactivate if dragged away
                    button_a_active = button_a.collidepoint(event.pos)
                    button_b_active = button_b.collidepoint(event.pos)

        # Increase score if both buttons are activated
        if button_a_active and button_b_active:
            score += 1
            # Move buttons to new positions
            button_a.topleft = (random.randint(0, screen_width - button_size[0]),
                                random.randint(0, screen_height - button_size[1]))
            button_b.topleft = (random.randint(0, screen_width - button_size[0]),
                                random.randint(0, screen_height - button_size[1]))
            # Reset activation
            button_a_active = button_b_active = False

        # Drawing
        screen.fill(background_color)
        pygame.draw.rect(screen, active_color if button_a_active else button_color, button_a)
        pygame.draw.rect(screen, active_color if button_b_active else button_color, button_b)

        # Display score
        score_text = font.render(str(score), True, text_color)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Yield control to allow other async tasks to run
        await asyncio.sleep(0)

asyncio.run(game_loop())
