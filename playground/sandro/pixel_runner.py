import pygame
from sys import exit
from random import randint

""" ToDo LIST
- Create options screen (select resolution and difficulty).
- Make nail and fly hitboxes smaller.
- Animation for entities.
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

def obstacles_movement(obstacles_list):
    if len(obstacles_list) > 0:
        for obstacle in obstacles_list:
            obstacle.x -= 5
            # Obtacle snail
            if obstacle.bottom == 300:
                screen.blit(snail_surface, obstacle)
            # Obstacle fly
            else:
                screen.blit(fly_surface, obstacle)
        obstacles_list = [obstacle for obstacle in obstacles_list if obstacle.x > -100]
        return obstacles_list
    else:
        return []

def collision_detection(player, obstacles_list):
    if len(obstacles_list) > 0:
        for obstacle in obstacles_list:
            if player.colliderect(obstacle): return 2
    return 1

def player_animation():
    global player_surface, player_index
    if player_rectangle.bottom < 300:
        player_surface = player_jump_surface
    else:
        player_index += 0.1
        if player_index >= len(player_walk_surface): player_index = 0
        player_surface = player_walk_surface[int(player_index)]

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

# Background graphics
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Obstacles
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
fly_surface = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
obstacles_rectangle_list = []

# Player
player_walk1_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk2_surface = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk_surface = [player_walk1_surface, player_walk2_surface]
player_index = 0
player_jump_surface = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_surface = player_walk_surface[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80, 300))

# Player stand
player_stand_surface = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 1.5)
player_stand_rectangle = player_stand_surface.get_rect(center = (400, 200))

# Load fonts
text_font = pygame.font.Font("font/Pixeltype.ttf", 40)
name_font = pygame.font.Font("font/Pixeltype.ttf", 80)

# Game name
game_name = name_font.render("Pixel Runner", False, (0, 0, 0))
game_name_rectangle = game_name.get_rect(center = (400, 75))

# Game message
game_message = text_font.render("Press space to start", False, (10, 10, 10))
game_message_rectangle = game_message.get_rect(center = (400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

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
                # Random obstacle
                if randint(0, 2) == 0:
                    obstacles_rectangle_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 200)))
                else:
                    obstacles_rectangle_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
        # Game over screen
        elif game_state == 2:
            # Go to game screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = 1
                # Reset variables
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

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300: player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rectangle)

        # Obstacles
        obstacles_rectangle_list = obstacles_movement(obstacles_rectangle_list)

        # Collision detection
        game_state = collision_detection(player_rectangle, obstacles_rectangle_list)
    
    # State 2: Game Over
    elif game_state == 2:
        display_background()
        obstacles_rectangle_list.clear()
        # Score
        score_message = text_font.render(f"Your score: {score}", False, (0, 0, 0))
        score_message_rectangle = score_message.get_rect(center = (400, 320))
        screen.blit(score_message, score_message_rectangle)
        
    # Update screen 60fps
    pygame.display.update()
    clock.tick(60)