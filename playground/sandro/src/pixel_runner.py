import pygame
from sys import exit
from random import randint, choice

# Player class
class Player(pygame.sprite.Sprite):
    global game_state
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load("../img/player/player_walk_1.png").convert_alpha()
        walk2 = pygame.image.load("../img/player/player_walk_2.png").convert_alpha()
        self.jump = pygame.image.load("../img/player/player_jump.png").convert_alpha()
        self.playesr_walk_index = [walk1, walk2]
        self.player_index = 0
        self.player_gravity = 0
        self.jumps = 0

        self.image = self.player_walk_index[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        
    def player_input(self):
        # Get event and check if it is a key press (space down)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game_state == 1 and self.rect.bottom >= 300:
            self.player_gravity = -20
            jump_sound.play()

    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_index): self.player_index = 0
            self.image = self.player_walk_index[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly1 = pygame.image.load("../img/fly/fly1.png").convert_alpha()
            fly2 = pygame.image.load("../img/fly/fly2.png").convert_alpha()
            self.frames = [fly1, fly2]
            y = 200
        elif type == "snail":
            snail1 = pygame.image.load("../img/snail/snail1.png").convert_alpha()
            snail2 = pygame.image.load("../img/snail/snail2.png").convert_alpha()
            self.frames = [snail1, snail2]
            y = 300
        else:
            print("Error: Invalid obstacle type.")
            exit()

        x = randint(900, 1100)
        self.obstacle_index = 0
        self.image = self.frames[self.obstacle_index]
        self.rect = self.image.get_rect(midbottom = (x, y))
        
    def obstacle_animation(self):
        self.obstacle_index += 0.1
        if self.obstacle_index >= len(self.frames): self.obstacle_index = 0
        self.image = self.frames[int(self.obstacle_index)]
    
    def destroy(self):
        if self.rect.x < -100:
            self.kill()
    
    def update(self):
        self.obstacle_animation()
        self.rect.x -= 5
        self.destroy()

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

def collision():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        game_over_sound.play()
        obstacles.empty()
        return 2
    else:
        return 1

# Initialize pygame
pygame.init() 

# Create screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")

# Game variables
game_state = 0
score = 0
start_time = 0
clock = pygame.time.Clock()

# Load sounds
background_music = pygame.mixer.Sound("../audio/music.wav")
background_music.set_volume(0.1)
game_over_sound = pygame.mixer.Sound("../audio/game_over.wav")
game_over_sound.set_volume(0.4)
start_sound = pygame.mixer.Sound("../audio/start.wav")
start_sound.set_volume(0.8)
jump_sound = pygame.mixer.Sound("../audio/jump.wav")
jump_sound.set_volume(0.2)

# Background
sky_surface = pygame.image.load("../img/sky.png").convert()
ground_surface = pygame.image.load("../img/ground.png").convert()
background_music.play(-1)

# Groups
player = pygame.sprite.GroupSingle(); player.add(Player())
obstacles = pygame.sprite.Group()

# Player stand
player_stand_surface = pygame.image.load("../img/player/player_stand.png").convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 1.5)
player_stand_rectangle = player_stand_surface.get_rect(center = (400, 200))

# Load fonts
text_font = pygame.font.Font("../font/Pixeltype.ttf", 40)
name_font = pygame.font.Font("../font/Pixeltype.ttf", 80)

# Game name
game_name = name_font.render("Pixel Runner", False, (0, 0, 0))
game_name_rectangle = game_name.get_rect(center = (400, 75))

# Game message
game_message = text_font.render("Press space to start", False, (10, 10, 10))
game_message_rectangle = game_message.get_rect(center = (400, 320))

# Timers
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
                start_sound.play()
                start_time = int(pygame.time.get_ticks() / 1000)
                game_state = 1
        # Game screen
        elif game_state == 1:
            if event.type == pygame.KEYDOWN:
                # Go to main screen
                if event.key == pygame.K_ESCAPE:
                    game_state = 0
            # Obstacle timer
            if event.type == obstacle_timer:
                # Random obstacle
                obstacles.add(Obstacle(choice(["snail", "snail", "snail", "fly"])))
        # Game over screen
        elif game_state == 2:
            # Go to game screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = 1
                start_sound.play()
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
        player.draw(screen)
        player.update()

        # Obstacles
        obstacles.draw(screen)
        obstacles.update()

        # Check for collision
        game_state = collision()
    
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