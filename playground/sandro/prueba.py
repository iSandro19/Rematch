import pygame
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'{current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Prueba")

# Game variables
game_active = True
start_time = 0
text = "Prueba"
clock = pygame.time.Clock()

# Load graphics
test_font = pygame.font.Font("font/Pixeltype.ttf", 40)
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

score_surface = test_font.render("Prueba", False, (0, 0, 0))
score_rectangle = score_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# Game loop
while True:
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            # Check for escape key
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            # Check for space key and game state
            if game_active:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
            else:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rectangle.x = 600
                    player_rectangle.x = 80
                    player_rectangle.bottom = 300
                    player_gravity = 0
                    start_time = int(pygame.time.get_ticks() / 1000)

    # State 1: Game Active
    if game_active:
        # Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        display_score()

        # Snail
        screen.blit(snail_surface, snail_rectangle)
        snail_rectangle.x -= 4
        if snail_rectangle.right <= 0: snail_rectangle.left = 800

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300: player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        # Colision
        if player_rectangle.colliderect(snail_rectangle):
            game_active = False
            text = "Game Over"
    
    # State 2: Game Over
    else:
        screen.fill((175, 215, 70))
        score_surface = test_font.render(text, False, (0, 0, 0))
        score_rectangle = score_surface.get_rect(center = (400, 50))
        screen.blit(score_surface, score_rectangle)

    pygame.display.update()
    clock.tick(60)