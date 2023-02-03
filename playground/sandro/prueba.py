import pygame
from sys import exit

""" ToDo LIST
- Create options screen (select resolution and difficulty).
- Make nail and fly hitboxes smaller.
- Add sound effects.
"""

# Functions
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render(f'{current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time

def display_background():
    screen.fill((192, 232, 236))
    screen.blit(game_name, game_name_rectangle)
    screen.blit(player_stand_surface, player_stand_rectangle)

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")

# Game variables
game_state = 0
score = 0
start_time = 0
player_gravity = 0
clock = pygame.time.Clock()

# Load graphics
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80, 300))

player_stand_surface = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 1.5)
player_stand_rectangle = player_stand_surface.get_rect(center = (400, 200))

# Load text
text_font = pygame.font.Font("font/Pixeltype.ttf", 40)
name_font = pygame.font.Font("font/Pixeltype.ttf", 80)

game_name = name_font.render("Pixel Runner", False, (0, 0, 0))
game_name_rectangle = game_name.get_rect(center = (400, 75))

game_message = text_font.render("Press space to start", False, (10, 10, 10))
game_message_rectangle = game_message.get_rect(center = (400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

# Game loop
while True:
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Main screen
        if game_state == 0:
            # Main screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = 1
        # Game screen
        elif game_state == 1:
            if event.type == pygame.KEYDOWN:
                # Go to main screen
                if event.key == pygame.K_ESCAPE:
                    game_state = 0
                # Jump
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
            # Obstacle timer
            if event.type == obstacle_timer:
                print("Obstacle timer")
        # Game over screen
        elif game_state == 2:
            # Go to game screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = 1
                # Reset variables
                snail_rectangle.x = 600
                player_rectangle.x = 80
                player_rectangle.bottom = 300
                player_gravity = 0
                start_time = int(pygame.time.get_ticks() / 1000)

    # State 0: Start Screen
    if game_state == 0:
        display_background()
        # Game message
        if int(pygame.time.get_ticks() / 800) % 2 == 0:
            screen.blit(game_message, game_message_rectangle)

    # State 1: Game
    elif game_state == 1:
        # Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Snail
        snail_rectangle.x -= 4
        if snail_rectangle.right <= 0: snail_rectangle.left = 800
        screen.blit(snail_surface, snail_rectangle)

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300: player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        # Colision
        if player_rectangle.colliderect(snail_rectangle): game_state = 2
    
    # State 2: Game Over
    elif game_state == 2:
        display_background()
        # Score
        score_message = text_font.render(f"Your score: {score}", False, (0, 0, 0))
        score_message_rectangle = score_message.get_rect(center = (400, 320))
        screen.blit(score_message, score_message_rectangle)
        
    # Update screen 60fps
    pygame.display.update()
    clock.tick(60)