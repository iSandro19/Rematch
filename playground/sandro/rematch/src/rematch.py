import pygame
from sys import exit
from random import randint, choice

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load("../img/player/player_walk_1.png").convert_alpha()
        walk2 = pygame.image.load("../img/player/player_walk_2.png").convert_alpha()
        self.jump = pygame.image.load("../img/player/player_jump.png").convert_alpha()
        self.player_walk_index = [walk1, walk2]
        self.player_index = 0
        self.player_gravity = 0

        self.image = self.player_walk_index[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 or keys[pygame.K_w] and self.rect.bottom >= 300:
            self.player_gravity = -20
        if keys[pygame.K_d] and self.rect.right < 800:
            self.rect.x += 5
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= 5

    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            # Animate only if a or d key is pressed
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]:
                self.player_index += 0.2
                if self.player_index >= len(self.player_walk_index):
                    self.player_index = 0
                self.image = self.player_walk_index[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

def display_background():
    screen.fill((192, 232, 236))

# Initialize pygame
pygame.init() 

# Create screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Rematch")

# Game variables
start_time = 0
clock = pygame.time.Clock()

# Background
sky_surface = pygame.image.load("../img/sky.png").convert()
ground_surface = pygame.image.load("../img/ground.png").convert()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

# Game loop
while True:
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Background
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))

    # Player
    player.draw(screen)
    player.update()
        
    # Update screen 60fps
    pygame.display.update()
    clock.tick(60)